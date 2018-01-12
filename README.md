# News Velocity - JCDL 2018

## Site parsers

Based off of CSS selectors. CSS selectors cannot select objects in iframes, for example: http://web.archive.org/web/20161109010834/http://www.latimes.com/

## Development

Steps to build data and visualizations:

1. Run `parse_sites.py` to generate a JSON file of hero/headline stories for each news outlet
2. (One time) Run `stories.py` to download story mementos from web.archive.org
3. Run `col_sim_prep.py` to format `parsed_links.json` to group links by day of the month generating `links_per_day.json`
4. Start `col-sim` docker and run with the generated `links_per_day.json` file
