import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the CSV file
try:
    df = pd.read_csv('commit_counts.csv')
except FileNotFoundError:
    print("Error: The file 'commit_counts.csv' was not found.")
    print("Please make sure you have run the data generation script first.")
    exit()

# Get the top 20 most committed files
top_20_files = df.head(20)

# Create the bar chart
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the data
ax.barh(top_20_files['File'], top_20_files['CommitCount'], color='#4CAF50')

# Set labels and title
ax.set_xlabel('Number of Commits', fontsize=12)
ax.set_ylabel('File', fontsize=12)
ax.set_title('Top 20 Files with the Most Commits', fontsize=16)

# Invert y-axis to show the highest value on top
ax.invert_yaxis()

# Add a grid for better readability
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig('commit_hotspots.png')

print("A bar chart of the top 20 commit hotspots has been saved as 'commit_hotspots.png'.")
