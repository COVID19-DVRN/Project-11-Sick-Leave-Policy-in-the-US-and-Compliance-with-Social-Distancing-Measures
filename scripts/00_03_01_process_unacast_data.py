import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
# %%
output_code = "00_03_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
df_unacast = pd.read_csv("../inputs/external/untracked/county_level_aggregates_26032020.csv")
# %%
df_single_date = df_unacast[df_unacast["localeventDate"]=="3/23/20"]
# %%
df_state_total_population = df_single_date[["state_code","county_population"]].groupby(["state_code"]).sum().rename(columns={'state_code':'state_code','county_population':'state_population'}).reset_index()
# %%
df_unacast["state_population"] = df_unacast[["localeventDate","state_code","county_population"]].groupby(["state_code","localeventDate"]).transform("sum")
# %%
df_unacast["diff_weighted_by_county_population"] = df_unacast["county_population"] * df_unacast["daily_distance_diff"] / df_unacast["state_population"]
# %%
df_weighted_average = df_unacast[["localeventDate","state_code","diff_weighted_by_county_population"]].groupby(["state_code","localeventDate"]).sum().reset_index()
df_weighted_average.columns = ["state_code","local_event_date","weighted_avg_distance_diff_by_county_population"]
df_weighted_average.set_index("state_code")
# %%
df_median = df_unacast[["localeventDate","state_code","daily_distance_diff"]].groupby(["state_code","localeventDate"]).median().reset_index()
df_median.columns = ["state_code","local_event_date","median_distance_diff_from_counties"]
#df_median.set_index("state_code")

# %%
df_mean = df_unacast[["localeventDate","state_code","daily_distance_diff"]].groupby(["state_code","localeventDate"]).mean().reset_index()
df_mean.columns = ["state_code","local_event_date","mean_distance_diff_from_counties"]

# %%
df_new = df_weighted_average.merge(df_median,  how = "inner")
df_new.set_index("state_code")
df_new = df_new.merge(df_mean, how = "inner")
df_new.set_index("state_code").to_csv("../inputs/internal/untracked/%s_state_level_aggregated_movement_diff_unacast.csv" %output_code)