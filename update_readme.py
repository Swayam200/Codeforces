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
        
        # Scan all rating directories, only if they are directories
        for rating_dir in self.repo_path.glob("*_rated"):
            if not rating_dir.is_dir():
                continue
            rating = rating_dir.name.split('_')[0]
            solutions[rating] = []
            
            # Look for C++, Python, and Java files
            for ext in ['*.cpp', '*.py', '*.java']:
                for solution_file in rating_dir.glob(ext):
                    # Enhanced regex to handle various naming patterns
                    file_name = solution_file.name
                    
                    # Pattern 1: Standard format (e.g., 133A-HQ9.py, 318A-Even-Odds.cpp)
                    match = re.match(r'(\d+)([A-Z])[-_](.+)\.(cpp|py|java)', file_name)
                    if not match:
                        # Pattern 2: With underscores (e.g., 344A_Magnets.cpp)
                        match = re.match(r'(\d+)([A-Z])_(.+)\.(cpp|py|java)', file_name)
                    if not match:
                        # Pattern 3: Simple format (e.g., 4A_Watermelon.cpp)
                        match = re.match(r'(\d+)([A-Z])_(.+)\.(cpp|py|java)', file_name)
                    
                    if match:
                        contest_id, index, name, file_ext = match.groups()
                        # Clean up the name
                        clean_name = name.replace('_', ' ').replace('-', ' ').strip()
                        solutions[rating].append({
                            'contest_id': contest_id,
                            'index': index,
                            'name': clean_name,
                            'file_path': str(solution_file.relative_to(self.repo_path)),
                            'extension': file_ext,
                            'full_filename': file_name
                        })
                    else:
                        print(f"Warning: Could not parse filename: {file_name}")
        
        # Sort solutions within each rating by contest_id and index
        for rating in solutions:
            solutions[rating].sort(key=lambda x: (int(x['contest_id']), x['index']))
        
        # Ensure common ratings are present even if empty
        for rating in ['800', '900', '1000', '1100']:
            if rating not in solutions:
                solutions[rating] = []
        
        print(f"Debug: Found solutions: {[(rating, len(probs)) for rating, probs in solutions.items()]}")
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
        
        # Add rating directories with files (only non-empty directories)
        rating_dirs = sorted([r for r in local_solutions.keys() if local_solutions[r]], key=int)
        
        for i, rating in enumerate(rating_dirs):
            is_last_dir = (i == len(rating_dirs) - 1)
            prefix = "└──" if is_last_dir else "├──"
            structure_lines.append(f"{prefix} 📂 {rating}_rated/")
            
            # Add files in directory (limit to first few files to keep structure readable)
            solutions = local_solutions[rating][:10]  # Limit to first 10 files
            for j, solution in enumerate(solutions):
                is_last_file = (j == len(solutions) - 1)
                if is_last_dir:
                    file_prefix = "    └──" if is_last_file else "    ├──"
                else:
                    file_prefix = "│   └──" if is_last_file else "│   ├──"
                filename = solution['full_filename']
                structure_lines.append(f"{file_prefix} 📄 {filename}")
            
            # Add "..." if there are more files
            if len(local_solutions[rating]) > 10:
                if is_last_dir:
                    structure_lines.append("    └── ...")
                else:
                    structure_lines.append("│   └── ...")
        
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
                if not tags_str:  # If no tags available
                    tags_str = "`implementation`"
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
        
        # Update statistics dashboard
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
        
        # Replace the entire statistics section
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
            if rating == '800':
                pattern = f'### 🟢 {rating}-Rated Problems.*?(?=### |## |$)'
                replacement = f"""### 🟢 {rating}-Rated Problems

{table}"""
            elif rating == '900':
                pattern = f'### 🔵 {rating}-Rated Problems.*?(?=### |## |$)'
                replacement = f"""### 🔵 {rating}-Rated Problems

{table}"""
            elif rating == '1000':
                pattern = f'### 🟡 {rating}-Rated Problems.*?(?=### |## |$)'
                replacement = f"""### 🟡 {rating}-Rated Problems

{table}"""
            
            readme_content = re.sub(
                pattern,
                replacement,
                readme_content,
                flags=re.DOTALL
            )
        
        # Add 900-rated section if it doesn't exist
        if '### 🔵 900-Rated Problems' not in readme_content:
            # Find where to insert the 900-rated section (after 800-rated)
            pattern = r'(### 🟢 800-Rated Problems.*?)(\n### |\n## |\Z)'
            table_900 = self.generate_problem_table(problems_api, local_solutions, '900')
            section_900 = f"""

### 🔵 900-Rated Problems

{table_900}"""
            
            readme_content = re.sub(
                pattern,
                r'\1' + section_900 + r'\2',
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