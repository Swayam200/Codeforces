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
            response = requests.get(url)
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
        
        # Look for 800_Rated directory only
        rating_dir = self.repo_path / "800_Rated"
        if rating_dir.exists():
            solutions["800"] = []
            
            for cpp_file in rating_dir.glob("*.cpp"):
                # Extract problem info from filename (e.g., "4A_Watermelon.cpp")
                match = re.match(r'(\d+)([A-Z])_(.+)\.cpp', cpp_file.name)
                if match:
                    contest_id, index, name = match.groups()
                    solutions["800"].append({
                        'contest_id': contest_id,
                        'index': index,
                        'name': name.replace('_', ' '),
                        'file_path': str(cpp_file.relative_to(self.repo_path))
                    })
        
        return solutions
    
    def generate_progress_stats(self, problems):
        """Generate statistics from problems list"""
        stats = {
            'total': len(problems),
            'by_rating': {},
            'current_streak': 1,  # You'd need to implement streak calculation
            'tags': {}
        }
        
        for problem in problems:
            rating = str(problem.get('rating', 'Unrated'))
            if rating not in stats['by_rating']:
                stats['by_rating'][rating] = 0
            stats['by_rating'][rating] += 1
            
            # Count tags
            for tag in problem.get('tags', []):
                stats['tags'][tag] = stats['tags'].get(tag, 0) + 1
        
        return stats
    
    def generate_problem_table(self, problems, local_solutions, rating):
        """Generate markdown table for problems of specific rating"""
        if rating not in local_solutions:
            return ""
        
        table_lines = [
            "| # | Problem | Difficulty | Status | Solution | Tags |",
            "|---|---------|------------|--------|----------|------|"
        ]
        
        problem_count = 1
        for solution in local_solutions[rating]:
            # Find matching problem from API data
            matching_problem = None
            for problem in problems:
                if (str(problem['contest_id']) == solution['contest_id'] and 
                    problem['index'] == solution['index']):
                    matching_problem = problem
                    break
            
            if matching_problem:
                tags_str = ", ".join([f"`{tag}`" for tag in matching_problem['tags'][:3]])  # Limit to 3 tags
                problem_link = f"[{matching_problem['contest_id']}{matching_problem['index']} - {matching_problem['name']}]({matching_problem['url']})"
                solution_link = f"[📝 Code](./{solution['file_path']})"
                
                table_lines.append(
                    f"| {problem_count} | {problem_link} | {rating} | ✅ Solved | {solution_link} | {tags_str} |"
                )
                problem_count += 1
        
        return "\n".join(table_lines)
    
    def update_readme(self):
        """Main function to update README.md"""
        print("Fetching Codeforces data...")
        problems = self.fetch_user_submissions()
        
        print("Scanning local solutions...")
        local_solutions = self.scan_local_solutions()
        
        print("Generating statistics...")
        stats = self.generate_progress_stats(problems)
        
        # Read current README
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
        else:
            print("README.md not found. Please create it first.")
            return
        
        # Update statistics
        stats_section = f"""### 🏆 Statistics Dashboard

| Metric | Count | Progress |
|--------|-------|----------|
| **Total Problems** | {stats['total']} | {'🟩' * min(5, stats['total'])}{'⬜' * max(0, 5-stats['total'])} |
| **800-Rated** | {stats['by_rating'].get('800', 0)} | {'✅' if stats['by_rating'].get('800', 0) > 0 else '⏳'} |
| **Current Streak** | {stats['current_streak']} day | 🔥 |"""
        
        # Update problems solved badge
        readme_content = re.sub(
            r'Problems%20Solved-\d+',
            f"Problems%20Solved-{stats['total']}",
            readme_content
        )
        
        # Update last updated date
        current_date = datetime.now().strftime("%B %Y")
        readme_content = re.sub(
            r'Last updated: <strong>.*?</strong>',
            f'Last updated: <strong>{current_date}</strong>',
            readme_content
        )
        
        # Generate problem tables for 800-rated only
        if '800' in local_solutions and local_solutions['800']:
            table = self.generate_problem_table(problems, local_solutions, '800')
            # You would need to implement regex replacement for the 800-rated section
            # This is a simplified version
        
        # Write updated README
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ README.md updated successfully!")
        print(f"📊 Total problems: {stats['total']}")
        
        return stats

def main():
    """Main execution function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Update Codeforces README.md automatically')
    parser.add_argument('username', help='Your Codeforces username')
    parser.add_argument('--repo-path', default='.', help='Path to your repository (default: current directory)')
    
    args = parser.parse_args()
    
    updater = CodeforcesReadmeUpdater(args.username, args.repo_path)
    stats = updater.update_readme()
    
    if stats:
        print("\n🎉 Update completed!")
        print(f"📈 Your progress: {stats['total']} problems solved")

if __name__ == "__main__":
    main()