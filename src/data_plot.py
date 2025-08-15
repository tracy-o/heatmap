import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

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

def create_plots(df, plot_type, top_n, special_users, filtered_users, output_location):
    """
    Generates and saves a plot based on the provided data.
    """
    if filtered_users:
        df = df[df['Author'].isin(filtered_users)]
        if df.empty:
            print("No data found for the specified users. Exiting.")
            return

    # Adjust figure size dynamically based on the number of files
    # 0.4 inches per file provides good spacing for labels
    fig_height = max(6, top_n * 0.4)
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, fig_height))

    if plot_type == 'stacked':
        # Create a new 'Category' column
        df['Category'] = df['Author'].apply(lambda x: 'Special Users' if x in special_users else 'Other')

        # Aggregate the data by File and the new Category
        pivot_df = df.groupby(['File', 'Category'])['CommitCount'].sum().unstack(fill_value=0)

        # Ensure 'Special Users' and 'Other' columns exist, even if empty
        if 'Special Users' not in pivot_df.columns:
            pivot_df['Special Users'] = 0
        if 'Other' not in pivot_df.columns:
            pivot_df['Other'] = 0

        # pink, blue
        colors = ['#FFC0CB', '#007ACC']

        pivot_df = pivot_df[['Special Users', 'Other']]
        pivot_df.loc[pivot_df.sum(axis=1).nlargest(top_n).index].plot(kind='barh', stacked=True, color=colors, ax=ax)

        ax.set_title(f'Top {top_n} File Hotspots by Contributor Category', fontsize=16)
        ax.set_xlabel('Number of Commits', fontsize=12)
        ax.set_ylabel('File', fontsize=12)
        ax.invert_yaxis()

    else:
        top_files = df.groupby('File')['CommitCount'].sum().nlargest(top_n)
        ax.barh(top_files.index, top_files.values, color='#4CAF50')
        ax.set_title(f'Top {top_n} Files with the Most Commits', fontsize=16)
        ax.set_xlabel('Number of Commits', fontsize=12)
        ax.set_ylabel('File', fontsize=12)
        ax.invert_yaxis()

    plt.tight_layout()
    plt.savefig(output_location)
    print(f"A chart of the top commit hotspots has been saved as '{output_location}'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Git commit hotspot visualization.")
    parser.add_argument(
        "input_path",
        type=str,
        default="commit_data.csv",
        help="The path to the input CSV data file. Defaults to 'commit_data.csv'."
    )
    parser.add_argument(
        "output_path",
        type=str,
        default="commit_hotspots.png",
        help="The path to the output PNG image file. Defaults to 'commit_hotspots.png'."
    )
    parser.add_argument("--stacked", action="store_true", help="Generate a stacked bar chart showing contributors.")
    parser.add_argument("--top", type=int, default=20, help="The number of top files to display. Defaults to 20.")
    parser.add_argument("--filter-users", type=str, help="A comma-separated list of users to include in the plot.")

    args = parser.parse_args()
    input_path = os.path.abspath(args.input_path)
    output_path = os.path.abspath(args.output_path)

    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
        print("Please run git_data_generator.py first to create the data file.")
        exit(1)

    filtered_users_list = args.filter_users.split(',') if args.filter_users else None
    plot_type = 'stacked' if args.stacked else 'simple'

    create_plots(df, plot_type, args.top, TEAM_BELFRAGE, filtered_users_list, output_path)
