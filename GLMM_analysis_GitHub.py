import statsmodels.formula.api as smf
import pandas as pd

def get_GLMM_results(file_path, group_name, stimulus_target, parameter, bodypart):
    df_result = pd.read_excel(
        file_path,
        engine="openpyxl",
        sheet_name=parameter,
    )

    indx = 0
    result_dict = {}
    for index, row in df_result.iterrows():
        parameter_list = row[parameter].replace("[", "").rstrip("]").split(", ")
        # print(f1_list)|
        for ind, parameter_value in enumerate(parameter_list):
            result_dict[indx] = [
                group_name,
                row["stimuli"],
                row["bat"],
                row["bodypart"],
                float(parameter_value),
            ]
            indx += 1

    df_result_reshaped = pd.DataFrame.from_dict(
        result_dict,
        orient="index",
        columns=["group", "stimuli", "bat", bodypart, parameter],
    )

    df_result_reshaped["y"] = 0
    df_result_reshaped.loc[df_result_reshaped["stimuli"] == stimulus_target, "y"] = 1
    df_result_reshaped["bat_num"] = pd.factorize(df_result_reshaped["bat"])[0]

    
    result_model = smf.mixedlm(
        "y ~  " + parameter,
        data=df_result_reshaped,
        groups=df_result_reshaped["bat_num"],  
        re_formula="1",
    )
    result = result_model.fit()
    print(result.summary())
