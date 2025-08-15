import subprocess
from collections import defaultdict
import pandas as pd
import sys
import os

def get_commit_counts_per_file(repo_path):
    """
    Analyzes the Git history of a specified repository to count commits per file.

    Args:
        repo_path (str): The path to the Git repository.

    Returns:
        dict: A dictionary of files and their commit counts.
    """
    print(f"Analyzing commit history for repo at: {repo_path}")

    command = [
        "git",
        "log",
        "--all",
        "--pretty=format:",
        "--name-only",
        "--no-merges"
    ]

    try:
        output = subprocess.check_output(command, cwd=repo_path, universal_newlines=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return {}
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return {}

    files = output.strip().split('\n')
    commit_counts = defaultdict(int)

    for filename in files:
        if filename:
            commit_counts[filename] += 1

    return commit_counts

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python your_script_name.py <repo_path> [output_file]")
        sys.exit(1)

    repo_path = os.path.abspath(sys.argv[1])
    output_file = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath("commit_counts.csv")

    file_hotspots = get_commit_counts_per_file(repo_path)

    df = pd.DataFrame(list(file_hotspots.items()), columns=['File', 'CommitCount'])
    df = df.sort_values(by='CommitCount', ascending=False)
    df.to_csv(output_file, index=False)

    print(f"\nData successfully saved to {output_file}")
