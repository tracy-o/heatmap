# HeatMap

Data representation for git commits.

## Requirements
```sh
- git
- python3
	- matplotlib
	- pandas
```

## Usage
### Generate data
Data for a repo with a (required) input path:
```sh
$ python3 src/data_gen.py ~/path/to/repo
```

Data for a repo with an input path and specified output path.
The default is `commit_data.csv` in the current working directory:
```sh
$ python3 src/data_gen.py ~/path/to/repo output/commit_data.csv
```

Filter data for commits that do not include a commit message regex:
```sh
$ python3 src/data_gen.py ~/path/to/repo output/commit_data.csv --message "format|mix format|lint"
```

### Generate visual
Visual using default input/output path. The defaults are `./commit_data.csv` for input and `./commit_hotspots.png` for output:
```sh
$ python3 src/data_plot.py
```

Visual using specified input path:
```sh
$ python3 src/data_plot.py output/commit_data.csv
```

Visual using specified input and output path:
```sh
$ python3 src/data_plot.py output/commit_data.csv output/commit_hotspots.png
```

Show top *n* files by commit count:
```sh
python3 src/data_plot.py --top 10
```

Show stacked bar chart showing contributions by user category:
```sh
python3 src/data_plot.py --stacked
```

Filter commits from certain users:
```sh
python3 src/data_plot.py --filter-users "Jane,jane-doe,jane@doe.com"
```
