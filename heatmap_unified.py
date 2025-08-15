import subprocess
from collections import defaultdict
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

def run_git_log(repo_path, message_regex=None):
    """
    Executes a git log command to gather commit data.

    Args:
        repo_path (str): The path to the Git repository.
        message_regex (str, optional): A regex to filter commit messages.

    Returns:
        list: A list of (author, file) tuples for each change.
    """
    command = [
        "git",
        "log",
        "--all",
        "--pretty=format:%an", # Get author name
        "--name-only",
        "--no-merges"
    ]

    if message_regex:
        command.extend(["--perl-regexp", f"--grep='^(?!.*({message_regex})).*$'"])

    print(f"Analyzing commit history for repo at: {repo_path} ...")

    try:
        output = subprocess.check_output(command, cwd=repo_path, universal_newlines=True, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e}")
        return []
    except FileNotFoundError:
        print("Error: Git command not found. Please ensure Git is installed and in your PATH.")
        return []

    lines = output.strip().split('\n')
    changes = []
    current_author = None

    for line in lines:
        if line.strip():
            if not line.startswith("    "):
                current_author = line.strip()
            else:
                filename = line.strip()
                changes.append((current_author, filename))

    return changes

def create_plots(df, plot_type, top_n, team_belfrage):
    """
    Generates and saves a plot based on the provided data.
    """
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))

    if plot_type == 'stacked':
        pivot_df = df.pivot_table(index='File', columns='Author', values='CommitCount', fill_value=0)

        team_belfrage_columns = [user for user in team_belfrage if user in pivot_df.columns]
        other_columns = [col for col in pivot_df.columns if col not in team_belfrage_columns]

        if other_columns:
            pivot_df['Other'] = pivot_df[other_columns].sum(axis=1)
            pivot_df = pivot_df.drop(columns=other_columns)

        pivot_df = pivot_df.loc[pivot_df.sum(axis=1).nlargest(top_n).index]
        pivot_df.plot(kind='barh', stacked=True, ax=ax)

        ax.set_title(f'Top {top_n} File Hotspots by Contributor', fontsize=16)
        ax.set_xlabel('Number of Commits', fontsize=12)
        ax.set_ylabel('File', fontsize=12)
        ax.invert_yaxis()

    else: # Default is a simple bar chart
        top_files = df.groupby('File')['CommitCount'].sum().nlargest(top_n)
        ax.barh(top_files.index, top_files.values, color='#4CAF50')
        ax.set_title(f'Top {top_n} Files with the Most Commits', fontsize=16)
        ax.set_xlabel('Number of Commits', fontsize=12)
        ax.set_ylabel('File', fontsize=12)
        ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig('commit_hotspots.png')
    print("A chart of the top commit hotspots has been saved as 'commit_hotspots.png'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Git commit hotspot visualization.")
    parser.add_argument("repo_path", type=str, help="The path to the Git repository to analyze.")
    parser.add_argument("--message", type=str, help="A regex to filter out commit messages. e.g., 'format|make format'")
    parser.add_argument("--stacked", action="store_true", help="Generate a stacked bar chart showing contributors.")
    parser.add_argument("--top", type=int, default=20, help="The number of top files to display. Defaults to 20.")

    args = parser.parse_args()

    TEAM_BELFRAGE = [
        "Tracy Oduebo", "tracy-o",
        "Ettore Berardi", "ettomatic",
        "Sam French", "samfrench",
        "David Thorpe", "DavidThorpe71",
        "Joseph Pack", "JoeARO",
        "Aleksandar", "isavita",
        "code-anth", "GuiHeurich",
        "Mike", "MikeIrlam",
        "seanmcarey"
    ]

    repo_path = os.path.abspath(args.repo_path)

    if not os.path.exists(os.path.join(repo_path, '.git')):
        print(f"Error: The provided path '{repo_path}' does not appear to be a Git repository.")
        exit(1)

    changes = run_git_log(repo_path, args.message)
    if not changes:
        exit()

    df = pd.DataFrame(changes, columns=['Author', 'File'])
    df['CommitCount'] = 1

    plot_type = 'stacked' if args.stacked else 'simple'
    create_plots(df, plot_type, args.top, TEAM_BELFRAGE)
