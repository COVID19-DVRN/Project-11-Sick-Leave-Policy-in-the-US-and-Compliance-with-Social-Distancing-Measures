import pandas as pd
import datetime
import numpy as np
# %%
output_code = "01_02_01"
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
## So I learnt that when StateWide is 1 then the policy is statewide
df_stay_at_home_neb_closure_statewide = df_stay_at_home_neb_closure[ (df_stay_at_home_neb_closure["StateWide"]==1)]
df_neb_closure = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="NEBusinessClose"]
neb_closure_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_neb_closure.set_index("StatePostal").to_dict()["DateEnacted"].items()}
df_emerg_dec = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="EmergDec"]
emerg_dec_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_emerg_dec.set_index("StatePostal").to_dict()["DateEnacted"].items()}
df_stay_at_home = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="StayAtHome"]
stay_at_home_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
#stay_at_home_by_state_code = {k: str(int(v)) for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
# %%
######################
## Reading the unacast social distancing metric data for states
######################
## Now read the Uncast file first
df_unacast_state = pd.read_csv("../inputs/raw/untracked/unacast_20200409/0409_sds_full_state.csv")
df_unacast_state["date_converted"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strptime(x,"%m/%d/%y"))
df_unacast_state["date_simple_string"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x,"%m/%d/%y"),"%Y%m%d"))
# %%
## Now creating three actual values for each state.
## Average of change in average distance travelled on Mar 19th and a week later
## because the federal act was passed on March 18 that says about 14 days paid
## sick leave https://en.wikipedia.org/wiki/Families_First_Coronavirus_Response_Act

## For the states that have emergency declared, the average of the week after
## declaration

## For the states that have mandated statewide Non essential business closure
## the average of the week after

## For the states that have mandated statewide Stay at home order
## the average of the week after

writelines = {}
intervention_types = ["federal_family_first_act","state_emergency",\
                              "statewide_neb_closure","statewide_stay_at_home"]
for intervention_type in intervention_types:
    writelines[intervention_type] = 'state_code,travel_distance_metric,visitation_metric,encounters_metric,date_converted,intervention\n'

for current_state in sorted(df_unacast_state.state_code.unique()):
    print("Current state %s" %(current_state))
    df_unacast_single_state = df_unacast_state[df_unacast_state["state_code"]==current_state]
    important_dates = {}
    federal_family_first_act_date = datetime.datetime(2020,3,18)
    important_dates["federal_family_first_act"] = federal_family_first_act_date
    if current_state in emerg_dec_by_state_code:
        current_date = emerg_dec_by_state_code[current_state]
        important_dates["state_emergency"] = current_date
    if current_state in neb_closure_by_state_code:
        current_date = neb_closure_by_state_code[current_state]
        important_dates["statewide_neb_closure"] = current_date
    if current_state in stay_at_home_by_state_code:
        current_date = stay_at_home_by_state_code[current_state]
        important_dates["statewide_stay_at_home"] = current_date
    
    current_state_writeline = []
    current_state_writeline.append(current_state)
    for intervention_type in intervention_types:
        
        if intervention_type in important_dates:            
            print(intervention_type)
            intervention_date = important_dates[intervention_type]
            print(intervention_date)
            date_low = intervention_date - datetime.timedelta(days=7)
            
            ## Now putting the effects after interventions date
            date_high_inclusive = intervention_date + datetime.timedelta(days = 7)
            #print(df_unacast_single_state[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive)])
            df_longitudinal = df_unacast_single_state.loc[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive), ["state_code","travel_distance_metric","visitation_metric","encounters_metric","date_converted"]]
            df_longitudinal["intervention"] = df_longitudinal["date_converted"].apply(lambda d: 0 if d <= intervention_date else 1)
            df_longitudinal["date_converted"]= df_longitudinal["date_converted"].apply(lambda d: d.strftime("%Y%m%d"))
            writelines[intervention_type] += df_longitudinal.to_csv(index=False, header = False)
for intervention_type in intervention_types:
    with open("../outputs/data/%s_longitudinal_intervention_daily_for_diff_in_diff_by_state_%s.csv" %(output_code,intervention_type), "w") as f:
        f.writelines(writelines[intervention_type])