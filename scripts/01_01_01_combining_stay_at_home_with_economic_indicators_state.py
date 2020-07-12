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
## Reading the us state economic conditions and paid sick leaves
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
## Reading the political polarization data
###########################
df_political_polarization = pd.read_csv("../inputs/raw/economic_indicators_polarization_by_elections.csv")
df_political_polarization.set_index("state_code")
# %%
df = df.merge(df_political_polarization, how = "inner")
# %%
######################
## Reading the us state interventions on covid19 and social distancing outcomes
######################
df_social_distancing = pd.read_csv("../inputs/derived/01_00_01_after_intervention_avg_metric_change_unacast_by_state.csv",na_filter = False)
df_social_distancing.set_index("state_code")
# %%
df_merged = df.merge(df_social_distancing, how = "inner")
# %%
######################
## Reading the us state average commuting and public transport commuting distance
######################
df_commute_time = pd.read_csv("../inputs/raw/commute_time_and_public_transit_commute_time.csv",na_filter = False)
df_commute_time.set_index("state_code")
# %%
df_merged = df.merge(df_commute_time, how = "inner")

# %%
######################
## Reading the ACS 2018 Commuting Data
######################
df_acs_commuting_data = pd.read_csv("../inputs/raw/ACS_2018_Commuting_Data.csv",na_filter = False)
df_acs_commuting_data.set_index("State")
df_merged = df_merged.merge(df_acs_commuting_data, how = "inner")

# %%
######################
## Reading the Oxfam Labour data
######################
df_oxfam_labour_data = pd.read_csv("../inputs/raw/LabourDataJuly2020.csv",na_filter = False)
df_oxfam_labour_data.set_index("state_code")
df_merged = df_merged.merge(df_oxfam_labour_data, how = "inner")

#%%
## Writing the merged dataframe to a file
df_merged.to_csv("../outputs/data/%s_combined_economic_indicators_with_social_distancing_outcomes_state_wide.csv" %output_code, index = False)
