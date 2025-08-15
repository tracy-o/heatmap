import subprocess
from collections import defaultdict
import pandas as pd
import argparse
import os

def get_commit_data(repo_path, message_regex=None):
    """
    Analyzes the Git history of a specified repository to gather commit data.
    """
    print(f"Analyzing commit history for repo at: {repo_path}")

    command = [
        "git",
        "log",
        "--all",
        "--pretty=format:%an",
        "--name-only",
        "--no-merges"
    ]

    if message_regex:
        command.extend(["--perl-regexp", f"--grep=^(?!.*({message_regex})).*$"])

    try:
        output = subprocess.check_output(command, cwd=repo_path, universal_newlines=True, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e.stderr}")
        return []
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return []

    blocks = output.strip().split('\n\n')
    changes = []

    for block in blocks:
        lines = block.strip().split('\n')
        if not lines:
            continue

        author = lines[0]
        filenames = lines[1:]

        for filename in filenames:
            changes.append((author, filename.strip()))

    return changes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a CSV of Git commit data.")
    parser.add_argument("repo_path", type=str, help="The path to the Git repository to analyze.")
    parser.add_argument("--message", type=str, help="A regex to filter out commit messages. e.g., 'format|make format'")
    parser.add_argument(
        "--output-path",
        type=str,
        default="commit_data.csv",
        help="The path to save the output CSV file. Defaults to 'commit_data.csv'."
    )
    args = parser.parse_args()

    repo_path = os.path.abspath(args.repo_path)
    output_path = os.path.abspath(args.output_path)

    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Error: The provided path '{repo_path}' does not appear to be a Git repository.")
        exit(1)

    changes = get_commit_data(repo_path, args.message)
    if not changes:
        print("No commit history found or an error occurred. Exiting.")
        exit(1)

    df = pd.DataFrame(changes, columns=['Author', 'File'])
    df['CommitCount'] = 1

    df_counts = df.groupby(['File', 'Author']).size().reset_index(name='CommitCount')
    df_counts.to_csv(output_path, index=False)

    print(f"\nData successfully saved to {output_path}")
