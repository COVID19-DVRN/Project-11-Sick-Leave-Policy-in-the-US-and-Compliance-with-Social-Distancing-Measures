import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
import csv
# %%
output_code = "01_03_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
df_state_name_code_abbrev = pd.read_csv("../inputs/raw/state_code_abbr_fullname.csv")
state_code_to_state_name = df_state_name_code_abbrev.set_index("state_code").to_dict()["state_name"]
state_code_to_state_abbrev = df_state_name_code_abbrev.set_index("state_code").to_dict()["state_abbrev"]
state_name_to_state_code = {v:k for k,v in state_code_to_state_name.items()}
# %%
######################
## Reading the us state policies
######################
df = pd.read_csv("../inputs/raw/USstatesCov19distancingpolicy.csv",encoding='latin1')
# %%
columns_keeping = ["StatePostal","StateName","StatePolicy","DateIssued","DateEnacted","DateExpiry","StateWide","PolicyCodingNotes","PolicySource"]
df = df.loc[:,columns_keeping]
# %%
df_stay_at_home_neb_closure = df[df["StatePolicy"].isin(["StayAtHome","NEBusinessClose","EmergDec"])]
# %%
## So I learnt that when StateWide is 1 then the policy is statewide"
df_stay_at_home_neb_closure_statewide = df_stay_at_home_neb_closure[ (df_stay_at_home_neb_closure["StateWide"]==1)]
df_stay_at_home_neb_closure_statewide.set_index("StatePostal").to_csv("../inputs/derived/%s_NPI_intervention_statewide_dates.csv" %(output_code))
df_neb_closure = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="NEBusinessClose"]
neb_closure_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_neb_closure.set_index("StatePostal").to_dict()["DateEnacted"].items()}
df_emerg_dec = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="EmergDec"]
emerg_dec_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_emerg_dec.set_index("StatePostal").to_dict()["DateEnacted"].items()}
df_stay_at_home = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="StayAtHome"]
stay_at_home_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
#stay_at_home_by_state_code = {k: str(int(v)) for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
# %%
## Maryland Nevada New York Maine DC Maryland They have dispersed neb closure and 
## stay at home order

# %%
######################
## Reading the unacast social distancing metric data for states
######################
## Now read the Uncast file first
unacast_date_format = "%Y-%m-%d"
df_unacast_state = pd.read_csv("../inputs/raw/untracked/unacast_20200509/sds-v3-full-state.csv")
df_unacast_state["date_converted"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strptime(x,unacast_date_format))
df_unacast_state["date_simple_string"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x,unacast_date_format),"%Y%m%d"))
# %%
######################
## Reading the NYTimes covid-19 cases and death data
######################
df_nytimes = pd.read_csv("../inputs/raw/nytimes-covid19-daily-cases-deaths-us-states.csv")
df_nytimes["state_code"] = df_nytimes["state"].apply(lambda x: state_name_to_state_code[x] if x in state_name_to_state_code else None)
df_nytimes["date_converted"] = df_nytimes["date"].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
# %%
######################
## Reading the us state economic conditions and paid sick leaves
######################
df_economic_indicators = pd.read_csv("../outputs/data/01_01_01_combined_economic_indicators_with_social_distancing_outcomes_state_wide.csv")
df_economic_indicators = df_economic_indicators[['state_code',
       'Dominant Sector (BLS, Feb. 2020)', 'Raw # of employees (in thousands)',
       'Paid Family Leave', 'Paid Sick Leave', 'Any Paid Time Off',
       'Unemployment Rate Feb 2020', 'Unemployment Rate Jan 2021',
       'MedianIncome2017', 'Election Results Coding', 'Number code',
       '2016 result',]]
df_economic_indicators.set_index("state_code")
# %%
def get_deaths_and_cases_on_intervention_date(date_low,current_state,df_nytimes=df_nytimes):
    #df_nytimes_single_state = df_nytimes[df_nytimes["state_code"] == current_state]
    if type(date_low) == str:
        date_low = datetime.datetime.strptime(date_low,"%Y-%m-%d")
    cumulative_cases_at_intervention_date = 0
    cumulative_deaths_at_intervention_date = 0
    new_cases_throghout_week_before_intervention = 0
    new_deaths_throghout_week_before_intervention = 0
    current_state_cumulative_at_intervention = df_nytimes[(df_nytimes["state_code"] == current_state) & (df_nytimes["date_converted"]==date_low)]
    ## If we have cases in the file in the intervention date then we will update it
    if not current_state_cumulative_at_intervention.empty:
        cumulative_cases_at_intervention_date = current_state_cumulative_at_intervention["cases"].item()
        cumulative_deaths_at_intervention_date = current_state_cumulative_at_intervention["deaths"].item()
        
        ## For now we will think that the cumulative cases upto this week happened
        ## on this week.
        ## But if there is a row that belongs to the week before then we will subtract the
        ## cumulative cases the week before    
        new_cases_throghout_week_before_intervention = cumulative_cases_at_intervention_date
        new_deaths_throghout_week_before_intervention = cumulative_deaths_at_intervention_date
        ## If we have the cases at intevention data and even the cases a week before intervention 
        ## then we will subtract the cases on that day to get weekly new cases and deaths
        current_state_cumulative_at_week_before_intervention = df_nytimes[(df_nytimes["state_code"] == current_state) & (df_nytimes["date_converted"]==(date_low - datetime.timedelta(days=7)))]
        if not current_state_cumulative_at_week_before_intervention.empty:
            new_cases_throghout_week_before_intervention -=  current_state_cumulative_at_week_before_intervention["cases"].item()
            new_deaths_throghout_week_before_intervention -= current_state_cumulative_at_week_before_intervention["deaths"].item()
    return cumulative_cases_at_intervention_date, cumulative_deaths_at_intervention_date, new_cases_throghout_week_before_intervention, new_deaths_throghout_week_before_intervention
# %%
columns = ["state_code","current_date","cumulative_cases_at_current_date","cumulative_deaths_at_current_date","new_cases_since_a_week_before","new_deaths_since_a_week_before"]
npi_interventions = ["federal_family_first_act","state_emergency",\
                     "statewide_neb_closure","statewide_stay_at_home"]  
for current_npi_intervention in npi_interventions:
    current_npi_intervention_columns = ["day_since_%s"  %current_npi_intervention]
    columns.extend(current_npi_intervention_columns)

columns.extend(["daily_distance_diff","daily_visitation_diff","encounters_rate"])

df_all_dates_all_together = pd.DataFrame([],columns=columns)
for current_date in sorted(df_unacast_state["date"].unique()):
    ## For each date we will create a single file where we will have all the possible indicators
    writelines = []
    #writelines.append(columns)
    
    ## 'state_code,current_date,cumulative_cases_at_current_date,new_cases_since_a_week_before,cumulative_deaths_at_current_date,new_deaths_since_a_week_before,\
    ## day_since_federal_family_first_act,day_since_state_emergency,day_since_statewide_neb_closure,day_since_statewide_stay_at_home',"daily_distance_diff","daily_visitation_diff","encounters_rate"
    
    ## another loop for a line for each state
    for current_state in sorted(df_unacast_state.state_code.unique()):
        writevalues = []
        writevalues.append(current_state)
        writevalues.append(current_date)
        ## adding the case and death values current and new sincle last week
        writevalues.extend(get_deaths_and_cases_on_intervention_date(current_date,current_state))
        
        ## Now adding number of days since NPI intervention
        important_dates = {}
        federal_family_first_act_date = datetime.datetime(2020,3,18)
        important_dates["federal_family_first_act"] = federal_family_first_act_date
        if current_state in emerg_dec_by_state_code:
            important_dates["state_emergency"] = emerg_dec_by_state_code[current_state]
        if current_state in neb_closure_by_state_code:
            important_dates["statewide_neb_closure"] = neb_closure_by_state_code[current_state]
        if current_state in stay_at_home_by_state_code:
            important_dates["statewide_stay_at_home"] = stay_at_home_by_state_code[current_state]
        
        ## So in this list we will put all the time sincethe intervention data
        ## if the intervention didn't already happend we have a negative date for now
        ## Else if there is no specific intervention date for current intervention, 
        ## we have nan
        days_since_npi_intervention = []
        for current_npi_intervention in npi_interventions:
            if current_npi_intervention in important_dates:
                days_since_npi_intervention.append((datetime.datetime.strptime(current_date,"%Y-%m-%d") - important_dates[current_npi_intervention]).days)
            else:
                days_since_npi_intervention.append("nan")
        
        writevalues.extend(days_since_npi_intervention)
        
        ## We are making sure the serial is "daily_distance_diff","daily_visitation_diff","encounters_rate"
        outcome_variables = ["daily_distance_diff","daily_visitation_diff","encounters_rate"]
        writevalues.extend(df_unacast_state.loc[(df_unacast_state["date_converted"]==current_date)&(df_unacast_state["state_code"]==current_state),outcome_variables].values[0])         
        writelines.append(writevalues)
    
    df_single_day_npi_and_distances = pd.DataFrame(writelines,columns = columns)
    df_new = df_single_day_npi_and_distances.merge(df_economic_indicators, how = "inner")
    df_new.to_csv("../outputs/data/segmented_regression_files_by_date/%s_combined_economic_indicators_with_social_distancing_outcomes_state_wide_%s.csv" %(output_code,current_date), index = False)
    df_all_dates_all_together = df_all_dates_all_together.append(df_new)
df_all_dates_all_together.to_csv("../outputs/data/segmented_regression_files_by_date/%s_all_dates_combined_economic_indicators_with_social_distancing_outcomes_state_wide.csv" %(output_code), index = False)
# %%
with open("../outputs/derived/%s_after_intervention_avg_metric_change_unacast_by_state.csv" %output_code, "w") as f:
    f.writelines("\n".join(writelines))