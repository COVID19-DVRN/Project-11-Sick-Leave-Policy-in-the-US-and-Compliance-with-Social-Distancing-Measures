import pandas as pd
import datetime
import matplotlib.pyplot as plt
import scipy.stats as stats
# %%
output_code = "00_01_01"
now = datetime.datetime.now().strftime("%Y%m%d")
# %%
df_white_collarness_ranking = pd.read_csv("../inputs/internal/00_01_01_white_collarness_ranking.csv")
# %%
## Now reading the evidation dataset compiled by Tareq
df_evidation = pd.read_csv("../inputs/external/Evidation Data - Sheet1.csv")
# %%
evidation_work_from_home_dict = df_evidation.set_index("State").to_dict()["Rank - Started working from home"]
evidation_avoided_large_gathering_dict = df_evidation.set_index("State").to_dict()["Rank - Avoided large gatherings"]
state_name_to_state_code_dict = df_evidation.set_index("State").to_dict()["State Code"]
# %%
white_collarness_dict = df_white_collarness_ranking.set_index("state_name").to_dict()["ranking_based_on_white_colarness"]

# %%
common_states = set(white_collarness_dict) & set(evidation_work_from_home_dict)

# %%
state_names = []
state_codes = []
evidation_work_from_home_ranks = []
white_collarness_ranks = []
for state in common_states:
    evidation_work_from_home_ranks.append(evidation_work_from_home_dict[state])
    white_collarness_ranks.append(white_collarness_dict[state])
    state_names.append(state)
    state_codes.append(state_name_to_state_code_dict[state])
# %%
tau, p_value_tau = stats.kendalltau(evidation_work_from_home_ranks, white_collarness_ranks)
# %%
rho, p_value_spearman = stats.spearmanr(evidation_work_from_home_ranks,white_collarness_ranks)
# %%
fig,ax = plt.subplots(figsize = (10,8))
ax.plot(evidation_work_from_home_ranks,white_collarness_ranks, "o", color = "green")
ax.text(0,44, 'spearman rank corr, r = %.2f\np value %.3f\nkendal tau rank corr, r = %.2f\np value %.3f\n' %(rho, p_value_spearman, tau, p_value_tau), fontsize=13)
for i in range(len(state_codes)):
    ax.annotate(state_names[i],(evidation_work_from_home_ranks[i]+0.1,white_collarness_ranks[i]+0.1))
ax.set_xlabel("Evidation work form home ranking for state \n(lower rank means more percentage of answered that they stayed at home)", fontsize=13)
ax.set_ylabel("Ranking of states based on White collar job \n(lower rank means there were more white collar job in that state)", fontsize=13)
fig.tight_layout()
fig.savefig("../outputs/figures/%s_rank_correlation_between_white_collarness_and_work_from_home_%s.png" %(output_code,now), dpi = 150)

# %%
##################
##################
## Avoided large gathering with white collarness

# %%
state_names = []
state_codes = []
evidation_ranks = []
white_collarness_ranks = []
for state in common_states:
    evidation_ranks.append(evidation_avoided_large_gathering_dict[state])
    white_collarness_ranks.append(white_collarness_dict[state])
    state_names.append(state)
    state_codes.append(state_name_to_state_code_dict[state])
# %%
tau, p_value_tau = stats.kendalltau(evidation_ranks, white_collarness_ranks)
# %%
rho, p_value_spearman = stats.spearmanr(evidation_ranks,white_collarness_ranks)
# %%
fig,ax = plt.subplots(figsize = (10,8))
ax.plot(evidation_ranks,white_collarness_ranks, "o", color = "green")
ax.text(0,44, 'spearman rank corr, r = %.2f\np value %.3f\nkendal tau rank corr, r = %.2f\np value %.3f\n' %(rho, p_value_spearman, tau, p_value_tau), fontsize=13)
for i in range(len(state_codes)):
    ax.annotate(state_names[i],(evidation_ranks[i]+0.1,white_collarness_ranks[i]+0.1))
ax.set_xlabel("Evidation avoided large gathering ranking for state \n(lower rank means more percentage of people answered they avoided large gathering)", fontsize=13)
ax.set_ylabel("Ranking of states based on White collar job \n(lower rank means there were more white collar job in that state)", fontsize=13)
fig.tight_layout()
fig.savefig("../outputs/figures/%s_rank_correlation_between_white_collarness_and_avoided_large_gathering_%s.png" %(output_code,now), dpi = 150)

