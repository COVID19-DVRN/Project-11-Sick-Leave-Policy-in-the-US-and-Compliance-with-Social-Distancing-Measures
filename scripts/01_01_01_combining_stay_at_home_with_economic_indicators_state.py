import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np
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
## Reading the us state econimic conditions and paid sick leaves
######################
df = pd.read_csv("../inputs/raw/economic_indicators_and_paid_sick_leave_by_state.csv")
df.set_index("state_code")
# %%
######################
## Reading the us state interventions on covid19 and social distancing outcomes
######################
df_social_distancing = pd.read_csv("../inputs/derived/01_00_01_after_intervention_avg_metric_change_unacast_by_state.csv",na_filter = False)
df_social_distancing.set_index("state_code")
# %%
df_new = df.merge(df_social_distancing, how = "inner")
df_new.to_csv("../outputs/data/%s_combined_economic_indicatros_with_social_distancing_outcomes_state_wide.csv" %output_code, index = False)