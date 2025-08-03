#!/usr/bin/env python3
"""
Codeforces README.md Auto-Updater
Automatically updates your README.md with latest problem statistics
"""

import os
import json
import requests
from datetime import datetime
import re
from pathlib import Path
import glob

class CodeforcesReadmeUpdater:
    def __init__(self, username, repo_path="."):
        self.username = username
        self.repo_path = Path(repo_path)
        self.readme_path = self.repo_path / "README.md"
        self.problems_data = []
        
    def fetch_user_submissions(self):
        """Fetch user's accepted submissions from Codeforces API"""
        try:
            url = f"https://codeforces.com/api/user.status?handle={self.username}"
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if data['status'] != 'OK':
                print(f"API Error: {data.get('comment', 'Unknown error')}")
                return []
                
            accepted_problems = []
            seen_problems = set()
            
            for submission in data['result']:
                if submission['verdict'] == 'OK':  # Accepted
                    problem = submission['problem']
                    problem_key = f"{problem['contestId']}{problem['index']}"
                    
                    if problem_key not in seen_problems:
                        seen_problems.add(problem_key)
                        accepted_problems.append({
                            'name': problem['name'],
                            'contest_id': problem['contestId'],
                            'index': problem['index'],
                            'rating': problem.get('rating', 'Unrated'),
                            'tags': problem.get('tags', []),
                            'url': f"https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"
                        })
            
            return sorted(accepted_problems, key=lambda x: x.get('rating', 9999))
            
        except Exception as e:
            print(f"Error fetching submissions: {e}")
            return []
    
    def scan_local_solutions(self):
        """Scan local directories for solution files"""
        solutions = {}
        
        # Scan all rating directories
        for rating_dir in self.repo_path.glob("*_rated"):
            rating = rating_dir.name.split('_')[0]
            solutions[rating] = []
            
            # Look for C++, Python, and Java files
            for ext in ['*.cpp', '*.py', '*.java']:
                for solution_file in rating_dir.glob(ext):
                    # Extract problem info from filename (e.g., "4A_Watermelon.cpp")
                    match = re.match(r'(\d+)([A-Z])_(.+)\.(cpp|py|java)', solution_file.name)
                    if match:
                        contest_id, index, name, file_ext = match.groups()
                        solutions[rating].append({
                            'contest_id': contest_id,
                            'index': index,
                            'name': name.replace('_', ' '),
                            'file_path': str(solution_file.relative_to(self.repo_path)),
                            'extension': file_ext
                        })
        
        return solutions
    
    def generate_progress_stats(self, local_solutions):
        """Generate statistics from local solutions"""
        total = sum(len(problems) for problems in local_solutions.values())
        
        stats = {
            'total': total,
            'by_rating': {},
            'current_streak': min(total, 7),  # Simplified streak calculation
            'tags': {}
        }
        
        for rating, problems in local_solutions.items():
            stats['by_rating'][rating] = len(problems)
        
        return stats
    
    def generate_progress_bar(self, count, max_bars=5):
        """Generate visual progress bar"""
        filled = min(max_bars, count)
        empty = max(0, max_bars - filled)
        return '🟩' * filled + '⬜' * empty
    
    def generate_repository_structure(self, local_solutions):
        """Generate repository structure tree"""
        structure_lines = [
            "```",
            "📁 Codeforces/",
            "├── 📂 .github/",
            "│   └── 📂 workflows/",
            "│       └── 📄 update-readme.yml"
        ]
        
        # Add rating directories
        rating_dirs = sorted(local_solutions.keys(), key=int)
        for i, rating in enumerate(rating_dirs):
            is_last_dir = (i == len(rating_dirs) - 1)
            prefix = "└──" if is_last_dir else "├──"
            structure_lines.append(f"{prefix} 📂 {rating}_rated/")
            
            # Add files in directory
            for j, solution in enumerate(local_solutions[rating]):
                is_last_file = (j == len(local_solutions[rating]) - 1)
                if is_last_dir:
                    file_prefix = "    └──" if is_last_file else "    ├──"
                else:
                    file_prefix = "│   └──" if is_last_file else "│   ├──"
                filename = Path(solution['file_path']).name
                structure_lines.append(f"{file_prefix} 📄 {filename}")
        
        # Add root files
        structure_lines.extend([
            "├── 📄 update_readme.py",
            "└── 📄 README.md",
            "```"
        ])
        
        return "\n".join(structure_lines)
    
    def generate_problem_table(self, problems_api, local_solutions, rating):
        """Generate markdown table for problems of specific rating"""
        if rating not in local_solutions or not local_solutions[rating]:
            return "*Coming soon...*"
        
        table_lines = [
            "| # | Problem | Difficulty | Status | Solution | Tags |",
            "|---|---------|------------|--------|----------|------|"
        ]
        
        for i, solution in enumerate(local_solutions[rating], 1):
            # Find matching problem from API data
            matching_problem = None
            for problem in problems_api:
                if (str(problem['contest_id']) == solution['contest_id'] and 
                    problem['index'] == solution['index']):
                    matching_problem = problem
                    break
            
            # Use default values if API data not available
            if matching_problem:
                tags_str = ", ".join([f"`{tag}`" for tag in matching_problem['tags'][:3]])
                problem_name = matching_problem['name']
                problem_url = matching_problem['url']
            else:
                tags_str = "`implementation`"
                problem_name = solution['name']
                problem_url = f"https://codeforces.com/problemset/problem/{solution['contest_id']}/{solution['index']}"
            
            problem_link = f"[{solution['contest_id']}{solution['index']} - {problem_name}]({problem_url})"
            solution_link = f"[📝 Code](./{solution['file_path']})"
            
            table_lines.append(
                f"| {i} | {problem_link} | {rating} | ✅ Solved | {solution_link} | {tags_str} |"
            )
        
        return "\n".join(table_lines)
    
    def update_readme(self):
        """Main function to update README.md"""
        print("🔍 Fetching Codeforces data...")
        problems_api = self.fetch_user_submissions()
        
        print("📂 Scanning local solutions...")
        local_solutions = self.scan_local_solutions()
        
        print("📊 Generating statistics...")
        stats = self.generate_progress_stats(local_solutions)
        
        # Read current README
        if not self.readme_path.exists():
            print("❌ README.md not found. Please create it first.")
            return None
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Update problems solved badge
        readme_content = re.sub(
            r'Problems%20Solved-\d+',
            f"Problems%20Solved-{stats['total']}",
            readme_content
        )
        
        # Update statistics dashboard - FIXED REGEX PATTERN
        stats_section = f"""<div align="center">

### 🏆 Statistics Dashboard

| Metric | Count | Progress |
|--------|-------|----------|
| **Total Problems** | {stats['total']} | {self.generate_progress_bar(stats['total'])} |
| **800-Rated** | {stats['by_rating'].get('800', 0)} | {'✅' if stats['by_rating'].get('800', 0) > 0 else '⏳'} |
| **900-Rated** | {stats['by_rating'].get('900', 0)} | {'✅' if stats['by_rating'].get('900', 0) > 0 else '⏳'} |
| **1000-Rated** | {stats['by_rating'].get('1000', 0)} | {'✅' if stats['by_rating'].get('1000', 0) > 0 else '⏳'} |
| **1100-Rated** | {stats['by_rating'].get('1100', 0)} | {'✅' if stats['by_rating'].get('1100', 0) > 0 else '⏳'} |
| **Current Streak** | {stats['current_streak']} days | 🔥 |

</div>"""
        
        # Replace the entire statistics section - FIXED PATTERN
        readme_content = re.sub(
            r'<div align="center">\s*### 🏆 Statistics Dashboard.*?</div>',
            stats_section,
            readme_content,
            flags=re.DOTALL
        )
        
        # Remove Learning Journey section entirely
        readme_content = re.sub(
            r'## 📈 Learning Journey.*?(?=## |---\n\n## |\Z)',
            '',
            readme_content,
            flags=re.DOTALL
        )
        
        # Update repository structure
        repo_structure = self.generate_repository_structure(local_solutions)
        readme_content = re.sub(
            r'```\n📁 Codeforces/.*?```',
            repo_structure,
            readme_content,
            flags=re.DOTALL
        )
        
        # Update problem tables for each rating
        ratings_to_update = ['800', '900', '1000']
        
        for rating in ratings_to_update:
            table = self.generate_problem_table(problems_api, local_solutions, rating)
            
            # Find and replace the specific rating section
            pattern = f'### 🟢 {rating}-Rated Problems.*?(?=### |## |$)'
            if rating == '900':
                pattern = f'### 🔵 {rating}-Rated Problems.*?(?=### |## |$)'
            elif rating == '1000':
                pattern = f'### 🟡 {rating}-Rated Problems.*?(?=### |## |$)'
            
            replacement = f"""### {'🟢' if rating == '800' else '🔵' if rating == '900' else '🟡'} {rating}-Rated Problems

{table}"""
            
            readme_content = re.sub(
                pattern,
                replacement,
                readme_content,
                flags=re.DOTALL
            )
        
        # Update last updated date
        current_date = datetime.now().strftime("%B %Y")
        readme_content = re.sub(
            r'Last updated: <strong>.*?</strong>',
            f'Last updated: <strong>{current_date}</strong>',
            readme_content
        )
        
        # Clean up any extra blank lines
        readme_content = re.sub(r'\n{3,}', '\n\n', readme_content)
        
        # Write updated README
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ README.md updated successfully!")
        print(f"📊 Total problems: {stats['total']}")
        print(f"📈 Rating breakdown: {dict(stats['by_rating'])}")
        
        return stats

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Codeforces README.md automatically')
    parser.add_argument('username', help='Your Codeforces username')
    parser.add_argument('--repo-path', default='.', help='Path to your repository (default: current directory)')
    
    args = parser.parse_args()
    
    print(f"🚀 Starting README update for user: {args.username}")
    
    updater = CodeforcesReadmeUpdater(args.username, args.repo_path)
    stats = updater.update_readme()
    
    if stats:
        print("\n🎉 Update completed successfully!")
        print(f"📈 Your progress: {stats['total']} problems solved")
        print(f"🏆 Keep up the great work!")
    else:
        print("\n❌ Update failed. Please check the logs above.")
        exit(1)

if __name__ == "__main__":
    main()