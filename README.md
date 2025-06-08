## figure

[source](https://www.visualcapitalist.com/mapped-data-center-electricity-consumption-by-state/)

## Project Description

From 2005 through 2018, Virginia consistently has had the highest data center electricity use in the United States. In fact, Virginia is often referred to as "Data Center Alley" as it hosts the largest concentration of data centers in the world, particularly in Northern Virginia. [David Kidd](https://www.governing.com/infrastructure/the-data-center-capital-of-the-world-is-in-virginia) pointed out in 2023 there were nearly 300 data center estimated to handle more than one-third of global online traffic. Northern Virginia data centers had a combined power consumption capacity of 2,552 MW. That’s four times the capacity of the next closest American markets, Dallas (654 MW) and Silicon Valley (615 MW)[src](https://www.visualcapitalist.com/cp/top-data-center-markets/).

This dominance is due to a combination of factors, including proximity to government agencies, strong internet infrastructure, and favorable tax incentives according to [Statistica Research Department's Nov 26, 2024 Data Center Electricity Consumption share in the United States 2023 by state report](https://www.statista.com/statistics/1537743/us-data-center-electricity-use-share-by-state/). Not mention There are 26 root DNS servers in Norther Virgina.

In total, there are approximately 580 data centers in total in the entire State of Virgina[src](https://www.datacentermap.com/usa/virginia/)

[Dominon Energy, Inc. ](https://en.wikipedia.org/wiki/Dominion_Energy), commonly referred to as Dominion, is the energy company headquartered in Richmond, Virginia that supplies electricity in parts of Virginia, North Carolina, and South Carolina and supplies natural gas to parts of Utah, Idaho and Wyoming, West Virginia, Ohio, Pennsylvania, North Carolina, South Carolina, and Georgia. Dominion also has generation facilities in Indiana, Illinois, Connecticut, and Rhode Island. Data centers represent the only growing sector of electricity demand in Virginia[pg 5](https://rga.lis.virginia.gov/Published/2021/SD17/PDF), accounting for 21% of Dominion Energy’s electricity sales [pg 26](https://s2.q4cdn.com/510812146/files/doc_financials/2022/q4/2023-02-08-DE-IR-4Q-2022-earnings-call-slides-vTC-Final.pdf)

How might this data center usage affect the energy consumption in megaWatts (MW) in the state of Virigina? Could we build a machine learning model to predict the energy consumption usage in general? What are the trends in energy consumption around hours of the day, holidays, or possible long term trends. And can we see trends in data center growth with energy consumption over the year?

## My Solution

I use the estimated energy consumption in Megawatts per 24 hour period per day from [Dominon Energy, Inc. ](https://en.wikipedia.org/wiki/Dominion_Energy) between 2005-04-30 and 2018-01-02 as the data was freely available in Kaggle.

I use a `eXtreme Gradient Boosting (XGBoost)` regression prediction model to forecast MW usage for Dominion data to take advantage of the high accuracy and performance of XGBoost models.

I used Mean Square Error (MSE) to measure error in the machine learning models because:

- I do not anticipate any significant outliers in the data which makes sense when looking at consumption data from hour to hour.
- I want to penalize large errors more severly

brew install libomp

## Data

Obtained from Kaggle: [here](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption?resource=download&select=DOM_hourly.csv)

I use the estimated energy consumption in Megawatts per 24 hour period per day from [Dominon Energy, Inc. ](https://en.wikipedia.org/wiki/Dominion_Energy) between 2005-04-30 and 2018-01-02. Commonly referred to as Dominion, it is an American energy company headquartered in Richmond, Virginia that supplies electricity in parts of Virginia, North Carolina, and South Carolina and supplies natural gas to parts of Utah, Idaho and Wyoming, West Virginia, Ohio, Pennsylvania, North Carolina, South Carolina, and Georgia. Dominion also has generation facilities in Indiana, Illinois, Connecticut, and Rhode Island.

## Special notes

XGBoost utilizes Open Multi-Processing (OpenMP) for parallelization during training and prediction, which can significantly impact performance. If you are running on a 64-bit MacOS and yoou do not have OpenMP runtime installed you will need to install `libomp`. You can do so easily by

```bash
brew install libomp
```

#

https://www.youtube.com/watch?v=vV12dGe_Fho - vid 1

https://www.youtube.com/watch?v=z3ZnOW-S550 - vid 2

# What was used

EDA - that involved cleaning up the data to mitigate effect of outliers (see eda_initial.ipynb and eda_adv.ipynb)
Statistics - outlier removal using Tukey Boxplots
