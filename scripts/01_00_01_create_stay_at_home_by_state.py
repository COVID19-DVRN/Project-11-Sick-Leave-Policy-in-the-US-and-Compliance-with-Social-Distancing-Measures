import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
# %%
output_code = "01_00_01"
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
df_stay_at_home_neb_closure_statewide.set_index("StatePostal").to_csv("../inputs/derived/%s_stay_at_home_statewide_dates.csv" %(output_code))
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
df_unacast_state = pd.read_csv("../inputs/raw/untracked/unacast_20200409/0409_sds_full_state.csv")
df_unacast_state["date_converted"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strptime(x,"%m/%d/%y"))
df_unacast_state["date_simple_string"] = df_unacast_state["date"].apply(lambda x: datetime.datetime.strftime(datetime.datetime.strptime(x,"%m/%d/%y"),"%Y%m%d"))
# %%

current_state = "MN"
df_unacast_single_state = df_unacast_state[df_unacast_state["state_code"]==current_state]
df = df_unacast_single_state
df = df.sort_values('date_converted', ascending=True)
fig,ax = plt.subplots(1,1,figsize = (20,5))
ax.plot(df['date_converted'], df['travel_distance_metric'])
if current_state in emerg_dec_by_state_code:
    current_state_emerg_dec = emerg_dec_by_state_code[current_state]
    ax.axvline(current_state_emerg_dec, color = "red")
if current_state in stay_at_home_by_state_code:
    current_state_stay_at_home = stay_at_home_by_state_code[current_state]
    ax.axvline(current_state_stay_at_home, color = "orange")
if current_state in neb_closure_by_state_code:
    current_state_neb_closure = neb_closure_by_state_code[current_state]
    ax.axvline(current_state_neb_closure, color = "blue")
pre_covid_in_dataset = datetime.datetime(2020,3,8)
ax.axvline(pre_covid_in_dataset, color = "green")
ax.set_title(current_state,fontsize = 20)
ax.set_ylim(-1,0.3)
plt.xticks(rotation='vertical')

# %%
## The state wise intervention and traffic change plots
# =============================================================================
# 
# fig, axarr = plt.subplots(26,2,figsize = (15,50))
# state_codes = sorted(df_unacast_state.state_code.unique())
# axarr_flat = axarr.flatten()
# for i,current_state in enumerate(state_codes):
#     print(i,current_state)
#     ax = axarr_flat[i]
#     df_unacast_single_state = df_unacast_state[df_unacast_state["state_code"]==current_state]
#     df = df_unacast_single_state
#     df = df.sort_values('date_converted', ascending=True)
#     ax.plot(df['date_converted'], df['travel_distance_metric'])
#     if current_state in emerg_dec_by_state_code:
#         current_state_emerg_dec = emerg_dec_by_state_code[current_state]
#         ax.axvline(current_state_emerg_dec, color = "red")
#     if current_state in stay_at_home_by_state_code:
#         current_state_stay_at_home = stay_at_home_by_state_code[current_state]
#         ax.axvline(current_state_stay_at_home, color = "orange")
#     if current_state in neb_closure_by_state_code:
#         current_state_neb_closure = neb_closure_by_state_code[current_state]
#         ax.axvline(current_state_neb_closure, color = "blue")
#     pre_covid_in_dataset = datetime.datetime(2020,3,8)
#     ax.axvline(pre_covid_in_dataset, color = "green")
#     ax.set_title(current_state,fontsize = 20)
#     ax.set_ylim(-1,0.3)
#     #ax.set_xticks(rotation='vertical')
# fig.tight_layout()
# plt.savefig("../outputs/figures/%s_state_wise_distance_change_unacast_%s.pdf" %(output_code,now))
# plt.show()
# =============================================================================

# %%
######################
## Reading the NYTimes covid-19 cases and death data
######################
df_nytimes = pd.read_csv("../inputs/raw/nytimes-covid19-daily-cases-deaths-us-states.csv")
df_nytimes["state_code"] = df_nytimes["state"].apply(lambda x: state_name_to_state_code[x] if x in state_name_to_state_code else None)
df_nytimes["date_converted"] = df_nytimes["date"].apply(lambda x: datetime.datetime.strptime(x,"%Y-%m-%d"))
# %%
def get_deaths_and_cases_on_intervention_date(date_low,current_state,df_nytimes=df_nytimes):
    #df_nytimes_single_state = df_nytimes[df_nytimes["state_code"] == current_state]
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

writelines = []
writelines.append(",".join(["state_code","federal_family_first_act_date","cumulative_cases_at_ff_act","cumulative_deaths_at_ff_act","new_cases_since_week_before_ff_act","new_death_since_week_before_ff_act","weekly_avg_change_in_avg_distance_after_federal_ff_act","weekly_avg_change_in_visitation_after_federal_ff_act","weekly_avg_change_in_encounter_after_federal_ff_act",\
              "state_emerg_date","cumulative_cases_at_state_emerg","cumulative_deaths_at_state_emerg","new_cases_since_week_before_state_emerg","new_death_since_week_before_state_emerg","weekly_avg_change_in_avg_distance_after_state_emerg","weekly_avg_change_in_visitation_after_state_emerg","weekly_avg_change_in_encounter_after_state_emerg",\
                "statewide_neb_closure_date","cumulative_cases_at_neb_closure","cumulative_deaths_at_neb_closure","new_cases_since_week_before_neb_closure","new_death_since_week_before_neb_closure","weekly_avg_change_in_avg_distance_after_neb_closure","weekly_avg_change_in_visitation_after_neb_closure","weekly_avg_change_in_encounter_after_neb_closure",\
                "statewide_stay_at_home_date","cumulative_cases_at_stay_at_home_order","cumulative_deaths_at_stay_at_home_order","new_cases_since_week_before_stay_at_home_order","new_death_since_week_before_stay_at_home_order","weekly_avg_change_in_avg_distance_after_stay_at_home_order","weekly_avg_change_in_visitation_after_stay_at_home_order","weekly_avg_change_in_encounter_after_stay_at_home_order"]))

for current_state in sorted(df_unacast_state.state_code.unique()):
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
    for intervention_type in ["federal_family_first_act","state_emergency",\
                              "statewide_neb_closure","statewide_stay_at_home"]:
        
        if intervention_type in important_dates:            
            #print(intervention_type)
            current_state_writeline.append(important_dates[intervention_type].strftime("%Y%m%d"))
            date_low = important_dates[intervention_type]
            ## First putting the cumulative case and deaths on intervention date
            ## and the new cases since one week before the intervention date
            current_state_writeline.extend(map(str,get_deaths_and_cases_on_intervention_date(date_low, current_state, df_nytimes)))
            
            ## Now putting the effects after interventions date
            date_high_inclusive = date_low + datetime.timedelta(days = 7)
            #print(df_unacast_single_state[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive)])
            mean_values = df_unacast_single_state[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive)].mean()
            for metric in ["travel_distance_metric","visitation_metric","encounters_metric"]:
                current_state_writeline.append(str(mean_values[metric]))
        else:
            current_state_writeline.extend(["nan","nan","nan","nan","nan","nan","nan","nan"])
            
    writelines.append(",".join(current_state_writeline))

with open("../inputs/derived/%s_after_intervention_avg_metric_change_unacast_by_state.csv" %output_code, "w") as f:
    f.writelines("\n".join(writelines))