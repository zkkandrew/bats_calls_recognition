# comparisons within each group
# 1.0 select data by group/stimuli/bodypart

import random
from scipy import stats

# save all results to a list
results_list = []


figure5_group_list = df_figure5["group_order"].unique()
for fg in figure5_group_list:
    df_fg = df_figure5[df_figure5["group_order"] == fg]
    fg_sti_list = df_fg["stimuli_order"].unique()
    for sti in fg_sti_list:
        df_fg_sti = df_fg[df_fg["stimuli_order"] == sti]
        fg_bp_list = df_fg_sti["bodypart"].unique()
        for bp in fg_bp_list:
            df_fg_sti_bp = df_fg_sti[df_fg_sti["bodypart"] == bp]
            fg_param_list = df_fg_sti_bp["param"].unique()
            for param in fg_param_list:
                df_fg_sti_bp_param = df_fg_sti_bp[df_fg_sti_bp["param"] == param]
                # data of each gropu/stimuli/bodypart/param selected
                fg_sti_bp_param_len = len(df_fg_sti_bp_param)
                if fg_sti_bp_param_len > 3:
                    print(
                        f"Group: {fg}, Stimuli: {sti}, Bodypart: {bp}, N={len(df_fg_sti_bp_param)}"
                    )
                    # averageley and randomly separate into two sub-groups
                    fg_sti_bp_value_list = list(df_fg_sti_bp_param["value"])
                    # print(fg_sti_bp_value_list)
                    average_stat = 0
                    average_p = 0
                    for random_times in range(10):  # random 10 times
                        random.shuffle(fg_sti_bp_value_list)
                        # print(fg_sti_bp_value_list)
                        sub_list1 = fg_sti_bp_value_list[
                            : len(fg_sti_bp_value_list) // 2
                        ]
                        sub_list2 = fg_sti_bp_value_list[
                            len(fg_sti_bp_value_list) // 2 :
                        ]
                        # print(f'Random indices for sub-group 1: {sub_list1}')
                        # print(f'Random indices for sub-group 2: {sub_list2}')
                        # normal test two sub-groups
                        stat_norm, p_norm = stats.kstest(
                            fg_sti_bp_value_list, cdf="norm"
                        )
                        # print(f'Normality test for full group: stat={stat_norm}, p={p_norm}')
                        stat, p = stats.levene(sub_list1, sub_list2)
                        # print(f'Levene test for equal variances: stat={stat}, p={p}')
                        # t-test or wilcoxon test

                        stat_w, p_w = stats.kruskal(sub_list1, sub_list2)
                        average_stat += stat_w
                        average_p += p_w
                        # print(f'Kruskal-Wallis H-test: stat={stat_w}, p={p_w}')
                    # save sub-groups data
                    for result_val in sub_list1:
                        results_list.append(
                            {
                                "group": fg,
                                "stimuli": sti,
                                "bodypart": bp,
                                "param": param,
                                "sub_group": 1,
                                "value": result_val,
                                "average_kruskal_stat": average_stat / 10,
                                "average_kruskal_p": average_p / 10,
                            }
                        )
                    for result_val in sub_list2:
                        results_list.append(
                            {
                                "group": fg,
                                "stimuli": sti,
                                "bodypart": bp,
                                "param": param,
                                "sub_group": 2,
                                "value": result_val,
                                "average_kruskal_stat": average_stat / 10,
                                "average_kruskal_p": average_p / 10,
                            }
                        )
                    print(
                        f"Average Kruskal-Wallis H-test over 10 random splits: stat={average_stat / 10}, p={average_p / 10}"
                    )
                else:
                    for index, row in df_fg_sti_bp_param.iterrows():
                        results_list.append(
                            {
                                "group": fg,
                                "stimuli": sti,
                                "bodypart": bp,
                                "param": param,
                                "sub_group": 1,
                                "value": row["value"],
                                "average_kruskal_stat": 0,
                                "average_kruskal_p": 0,
                            }
                        )
