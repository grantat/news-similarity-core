# News Similarity Core - Research Code

Research code associated with @oduwsdl group's News Similarity Project.

## Site parsers

Utilizes Top-news-selectors (tns) package: https://github.com/oduwsdl/top-news-selectors to extract news articles based on CSS selectors.

## Setup

To setup this repository and retrieve the data before running of the scripts run:

```shell
$ git clone https://github.com/grantat/news-similarity-core
$ pip3 install requirements
```

For nodejs requirements:

```shell
$ yarn install
```

The `data` directory for this project should also be downloaded since it is included as a [Git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules).

## Development

Steps to collect data:

1. Run `parse_sites.py` to generate a JSON file of hero/headline stories for each news outlet
2. (One time) Run `stories.py` to download story mementos from web.archive.org
3. Run `col_sim_prep.py` to format `parsed_links.json` to group links by day of the month generating `links_per_day.json`
4. (Not included in this repository) Start `col-sim` docker and run with the generated `links_per_day.json` file
    - To execute `colSim.py` use (replace k_val as desired with: k1, k3, k10):
    ```shell
    $ python3 colSim.py links_per_day_dir/ outputDir/ --k_val="k10"
    ```
    If mounting data with Docker:
    ```shell
    $ docker run -it --rm -v $(pwd)/data:data/ --net="host" dockername python3 colSim.py --k_val="k10" links_per_day_dir/ outputDir/
    ```

If the `data` directory is already downloaded, visualizations are generated using R:
- `memento_time_diff.R` looks at the time differences between the selected memento and the target time (e.g. 1AM GMT)
- `memento-heatmap.R` shows memento times based on a 24 hour period as a heatmap - helps in choosing which hour has the most mementos between sites
- `col_sim.R` visualizes news similarity values as either line graphs or bar charts for a month

If a user desires to take screenshots of mementos in their `data` directory you can utilize the Nodejs `memento_screenshots.js`.
It can be executed as follows:

```shell
$ node memento_screenshot.js {DATE(Y-m-d)} {OUT_DIRECTORY}
# Example:
$ node memento_screenshots.js 2016-10-05 dir_10_05/
```

## Data

The data directory, `/data`, is available in a separate repository: https://github.com/grantat/news-similarity.
