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
df_stay_at_home_neb_closure = df[df["StatePolicy"].isin(["StayAtHome","NEBusinessClose"])]
# %%
## So I learnt that when StateWide is 1 then the policy is statewide
df_stay_at_home_neb_closure_statewide = df_stay_at_home_neb_closure[ (df_stay_at_home_neb_closure["StateWide"]==1)]
df_stay_at_home_neb_closure_statewide.to_csv("../inputs/derived/%s_stay_at_home_statewide_dates.csv" %(output_code))
df_neb_closure = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="NEBusinessClose"]
neb_closure_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_neb_closure.set_index("StatePostal").to_dict()["DateEnacted"].items()}
df_stay_at_home = df_stay_at_home_neb_closure_statewide[df_stay_at_home_neb_closure_statewide["StatePolicy"]=="StayAtHome"]
stay_at_home_by_state_code = {k: datetime.datetime.strptime(str(int(v)),"%Y%m%d") for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
#stay_at_home_by_state_code = {k: str(int(v)) for k,v in df_stay_at_home.set_index("StatePostal").to_dict()["DateEnacted"].items()}
# %%
## Maryland Nevada New York Maine DC Maryland

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