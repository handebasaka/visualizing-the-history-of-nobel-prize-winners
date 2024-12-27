## Visualizing The History of Nobel Prize Winners

The Nobel Prize has been one of the most prestigious international awards since 1901. Each year, it is awarded in chemistry, literature, physics, physiology or medicine, economics, and peace. In addition to the honor, prestige, and substantial prize money, recipients also receive a gold medal featuring an image of Alfred Nobel (1833 - 1896), who established the prize.

In this project, we will explore and answer several questions related to Nobel Prize winners and their data. I encourage you to dive deeper and explore additional questions that pique your interest!

**Dataset:** The Nobel Foundation provides all of the data since 1901 via an [API](https://www.nobelprize.org/organization/developer-zone-2/). This endpoint sorts the output based on Nobel Laureates (persons and/or organizations). It returns all information about Laureates and Nobel Prizes. We will get the data from the API, create the dataset, and then explore the trends.

To get started on answering questions and creating some plots in Python, we will need some packages below:
- `requests`: It is a simple HTTP library which allows you to send HTTP/1.1 requests extremely easily.
- `pandas`: It is a data analysis and manipulation library that provides data structures and tools.
- `matplotlib.pyplot`: It is a plotting library for creating visualizations in Python.
- `seaborn`: It provides a high-level interface for drawing attractive and informative statistical graphics.


## Goals
- The goal of this project is to answer below questions to explore the details about Nobel Prize winners.

**Questions**
1. Who was the first woman to receive a Nobel Prize, and in which category?

2. Which decade had the most Nobel Prize winners across all categories?

3. Which individuals or organizations have won more than one Nobel Prize throughout the years?

4. What is the gender distribution of Nobel Prize winners by category?

5. What is the distribution of Nobel Prize winners by birth-country and continent?

*You will get graphs to answer these questions in the Python file but you can also find the answers and comments in the Jupyter Notebook.*

## Tools and Technologies Used
`Python`

`Request` for fetch data

`Pandas` for data manipulation 

`Matplotlib` and `Seaborn` for data visualization

## How to Run
clone:
```sh
git clone https://github.com/handebasaka/visualizing-the-history-of-nobel-prize-winners
```
open the solution file:
```bash
cd visualizing-the-history-of-nobel-prize-winners
```
run python script:
```bash
python3 visualizing-the-history-of-nobel-prize-winners.py
```
