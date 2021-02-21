## Data sources
### state level NPI data
USstatesCov19distancingpolicy.csv
https://github.com/COVID19StatePolicy/SocialDistancing/blob/master/data/USstatesCov19distancingpolicy.csv
citation:
Nancy Fullman, Bree Bang-Jensen, Kenya Amano, Christopher Adolph, and John Wilkerson. "State-level social distancing policies in response to COVID-19 in the US". Version 1.14, May 9, 2020. http://www.covid19statepolicy.org

### state level covid-19 cases and deaths data
https://github.com/nytimes/covid-19-data/blob/master/us-states.csv
Accessed: July 12, 2020

Lets find the case data from here later:
https://docs.google.com/spreadsheets/u/2/d/e/2PACX-1vRwAqp96T9sYYq2-i7Tj0pvTf6XVHjDSMIKBdZHXiCGGdNC0ypEU9NbngS8mxea55JuCFuua1MUeOj5/pubhtml#

### Unacast movement data
I am using the version that I accessed on May 9th, 2020

### Commute time state side
https://www.cnbc.com/2018/02/22/study-states-with-the-longest-and-shortest-commutes.html

## ACS 2018 Commuting Data
Responsible person: It is compiled by Akshay Deverakonda
Source is: 

## LabourDataJuly2020
Responsible person: It is compiled by Fahim Hassan
The source is: https://policy-practice.oxfamamerica.org/work/poverty-in-the-us/map-oxfam-state-labor-index-2019/scorecard/?state=AL#methodology

## Google_Global_Mobility_Report.csv
Responsible person: Syed
Source: https://www.google.com/covid19/mobility/
Reports created 2020-07-09.
Accessed on: July 12, 2020

## us_states_population_and_land_area.csv
US States Population, Land Area, Population Denisity per mile
Compiled by: Akshay Deverakonda
Population: (Source: ACS 2019 (https://www.census.gov/data/tables/time-series/demo/popest/2010s-state-total.html#par_textimage)
Land Area:  (Source: Census 2010 (https://www.census.gov/prod/cen2010/cph-2-1.pdf, Table 20, page 91)

## us_states_annual_state_GDP_for_2019.csv
This contain the annual GDP of US states for the year 2019
compiled by: Akshay Deverakonda

## us_states_unemployment_and_race_ethnicity.csv
Source: Complined by Fahim hasan found in the [DVRN google drive sheet](https://docs.google.com/spreadsheets/d/14u-ITLW0iIKfiWZxIR9vmpIdslvvj2Pm5g9MPSCJOWg/edit#gid=305453204) in a tab called unemployment_and_race_ethnicity. The unemployment data is sourced from [BLS website](https://www.bls.gov/charts/state-employment-and-unemployment/state-unemployment-rates-animated.htm). The race ethnicity data is sourced from [Kaiser Family Foundataion](https://www.kff.org/other/state-indicator/distribution-by-raceethnicity/?currentTimeframe=0&sortModel=%7B%22colId%22:%22Location%22,%22sort%22:%22asc%22%7D).

The vaiables we are adding from this file are: ['Unemployment Rate Jan 2020',
	'Unemployment Rate Feb 2020',
	'Unemployment Rate Mar 2020',
	'Unemployment Rate Apr 2020',
	'Unemployment Rate May 2020',
	'Unemployment Rate Jun 2020',
	'Unemployment Rate Jul 2020',
	'Unemployment Rate Aug 2020',
	'Unemployment Rate Sept 2020',
	'Unemployment Rate Oct 2020',
	'Unemployment Rate Nov 2020',
	'Unemployment Rate Dec 2020',
	'White',
	'Black',
	'Hispanic',
	'Asian',
	'American Indian/Alaska Native',
	'Native Hawaiian/Other Pacific Islander',
	'Multiple Races']

In this data, in two columns (American Indian/Alaska Native, Native Hawaiian/Other Pacific Islander) there are text values, those values are either "N/A" or "<.01". I have manually changed those "N/A" with "nan" and "<.01" as "0.001".

## us_states_stccenter_covid19data_socioeconomic_determinants.csv
This is downloaded from the Github repo https://github.com/stccenter/COVID-19-Data. Here is the [link to the actual file](https://github.com/stccenter/COVID-19-Data/blob/master/Socioeconomic%20Data/Socioeconomic%20determinants/socioeconomic%20determinant%20for%20state.csv). I have accessed it on Februrary 21, 2021. Here is the [link to the commit](https://github.com/stccenter/COVID-19-Data/commit/2512dd22845a47090ce534fd69978df882ffd361) that I used.

We are taking only a few variables from there:

["Senior Population",
"Young Population",
"Male Population",
"Median household income",
"Poverty rate"]

The recommended citation is provided in the readme of the repository: https://github.com/stccenter/COVID-19-Data