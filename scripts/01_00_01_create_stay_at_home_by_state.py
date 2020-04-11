import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
# %%
output_code = "01_00_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
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
fig, axarr = plt.subplots(26,2,figsize = (15,50))
state_codes = sorted(df_unacast_state.state_code.unique())
axarr_flat = axarr.flatten()
for i,current_state in enumerate(state_codes):
    print(i,current_state)
    ax = axarr_flat[i]
    df_unacast_single_state = df_unacast_state[df_unacast_state["state_code"]==current_state]
    df = df_unacast_single_state
    df = df.sort_values('date_converted', ascending=True)
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
    #ax.set_xticks(rotation='vertical')
fig.tight_layout()
plt.savefig("../outputs/figures/%s_state_wise_distance_change_unacast%s.pdf" %(output_code,now))
plt.show()

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

avg_change_avg_distance_week_after_family_first_pass = dict()
avg_change_avg_distance_week_after_state_emergenecy = dict()
avg_change_avg_distance_week_after_state_neb_closure = dict()
avg_change_avg_distance_week_after_state_stay_at_home = dict()

writelines = []
writelines.append(",".join(["state_code","federal_family_first_act_date","weekly_avg_change_in_avg_distance_after_federal_ff_act","weekly_avg_change_in_visitation_after_federal_ff_act","weekly_avg_change_in_encounter_after_federal_ff_act",\
              "state_emerg_date","weekly_avg_change_in_avg_distance_after_state_emerg","weekly_avg_change_in_visitation_after_state_emerg","weekly_avg_change_in_encounter_after_state_emerg",\
                "statewide_neb_closure_date","weekly_avg_change_in_avg_distance_after_neb_closure","weekly_avg_change_in_visitation_after_neb_closure","weekly_avg_change_in_encounter_after_neb_closure",\
                "statewide_stay_at_home_date","weekly_avg_change_in_avg_distance_after_stay_at_home_order","weekly_avg_change_in_visitation_after_stay_at_home_order","weekly_avg_change_in_encounter_after_stay_at_home_order"]))
current_state = "NY"
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
            date_high_inclusive = date_low + datetime.timedelta(days = 7)
            #print(df_unacast_single_state[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive)])
            mean_values = df_unacast_single_state[(df_unacast_single_state["date_converted"] > date_low) & (df_unacast_single_state["date_converted"] <= date_high_inclusive)].mean()
            for metric in ["travel_distance_metric","visitation_metric","encounters_metric"]:
                current_state_writeline.append(str(mean_values[metric]))
        else:
            current_state_writeline.extend(["NA","NA","NA","NA"])

    writelines.append(",".join(current_state_writeline))
    
with open("../inputs/derived/%s_after_intervention_avg_metric_change_unacast_by_state.csv" %output_code, "w") as f:
    f.writelines("\n".join(writelines))