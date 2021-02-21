import pandas as pd
import datetime
# %%
output_code = "01_01_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
df_state_name_code_abbrev = pd.read_csv("../inputs/raw/state_code_abbr_fullname.csv")
state_code_to_state_name = df_state_name_code_abbrev.set_index("state_code").to_dict()["state_name"]
state_code_to_state_abbrev = df_state_name_code_abbrev.set_index("state_code").to_dict()["state_abbrev"]
state_name_to_state_code = {v:k for k,v in state_code_to_state_name.items()}
# %%
######################
## Merging the us state economic conditions and paid sick leaves
######################
df = pd.read_csv("../inputs/raw/economic_indicators_and_paid_sick_leave_by_state.csv")
df = df[["State","Abbreviation","state_code",
         "Dominant Sector (BLS, Feb. 2020)",
         "Raw # of employees (in thousands)",
         "Paid Family Leave", "Paid Sick Leave",
         "Any Paid Time Off","Unemployment Rate Feb 2020",
         "Unemployment Rate Jan 2021","MedianIncome2017"]]
df["Dominant Sector (BLS, Feb. 2020)"] = df["Dominant Sector (BLS, Feb. 2020)"].apply(lambda x: x.replace(",","").replace("&","and")) 
df.set_index("state_code")
# %%
###########################
## Merging the political polarization data
###########################
df_political_polarization = pd.read_csv("../inputs/raw/economic_indicators_polarization_by_elections.csv")
df_political_polarization.set_index("state_code")
# %%
df = df.merge(df_political_polarization, how = "inner")
# %%
######################
## Merging the us state interventions on covid19 and social distancing outcomes
######################
df_social_distancing = pd.read_csv("../inputs/derived/01_00_01_after_intervention_avg_metric_change_unacast_by_state.csv",na_filter = False)
df_social_distancing.set_index("state_code")
# %%
df_merged = df.merge(df_social_distancing, how = "inner")
# %%
######################
## Merging the us state average commuting and public transport commuting distance
######################
df_commute_time = pd.read_csv("../inputs/raw/commute_time_and_public_transit_commute_time.csv",na_filter = False)
df_commute_time.set_index("state_code")
# %%
df_merged = df.merge(df_commute_time, how = "inner")
# %%
######################
## Merging the ACS 2018 Commuting Data
######################
df_acs_commuting_data = pd.read_csv("../inputs/raw/ACS_2018_Commuting_Data.csv",na_filter = False)
df_acs_commuting_data.set_index("State")
df_merged = df_merged.merge(df_acs_commuting_data, how = "inner")
# %%
######################
## Merging the Oxfam Labour data
######################
df_oxfam_labour_data = pd.read_csv("../inputs/raw/LabourDataJuly2020.csv",na_filter = False)
df_oxfam_labour_data.set_index("state_code")
df_merged = df_merged.merge(df_oxfam_labour_data, how = "inner")
# %%
######################
## Merging the US States GDP data of year 2019
######################
df_us_states_gdp = pd.read_csv("../inputs/raw/us_states_annual_state_GDP_for_2019.csv",na_filter = False)
df_us_states_gdp.set_index("state_code")
df_merged = df_merged.merge(df_us_states_gdp, how = "inner")
# %%
######################
## Merging the US States Population, Area (in mile) and population density data
######################
df_us_states_population_land_area = pd.read_csv("../inputs/raw/us_states_population_and_land_area.csv",na_filter = False)
df_us_states_population_land_area.set_index("state_code")
df_merged = df_merged.merge(df_us_states_population_land_area, how = "inner")
######################
## Merging the US Unemployement rate in different months and the population by race ethnicity
######################
## New  columns 
columns_to_add = ['Unemployment Rate Jan 2020',
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

df_us_states_unemployment_and_race_ethnicity = pd.read_csv("../inputs/raw/us_states_unemployment_and_race_ethnicity.csv",na_filter = False)
df_us_states_unemployment_and_race_ethnicity = df_us_states_unemployment_and_race_ethnicity[["state_code"]+columns_to_add]
df_us_states_unemployment_and_race_ethnicity.set_index("state_code")
## Two columns "American Indian/Alaska Native" and  "Native Hawaiian/Other Pacific Islander"
## have text values, those values are either "N/A" or "<.01". I am manually changing
## those "N/A" with "nan" and "<.01" as "0.001".
dict_keywords_to_transform = {
	"N/A":"nan",
	"<.01":"0.001"
}
columns_transfomration_required = ["American Indian/Alaska Native", "Native Hawaiian/Other Pacific Islander"]
for column_transfomration_required in columns_transfomration_required:
	df_us_states_unemployment_and_race_ethnicity[column_transfomration_required].replace(dict_keywords_to_transform, inplace = True)
df_merged = df_merged.merge(df_us_states_unemployment_and_race_ethnicity, how = "inner")

#%%
## Writing the merged dataframe to a file
df_merged.to_csv("../outputs/data/%s_combined_economic_indicators_with_social_distancing_outcomes_state_wide.csv" %output_code, index = False)
