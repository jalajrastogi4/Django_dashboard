import pandas as pd
import numpy as np
import altair as alt
import re
import os

def read_file():
    module_dir = os.path.dirname(__file__)
    fname = os.path.join(module_dir,"files/Workflow_Result.txt")
    f = open(fname)
    lines = f.readlines()
    rng = len(lines)
    my_lt = []
    for i in range(2, rng, 4):
        if i < rng:
            x = lines[i]
            my_lt.append(re.split(r'\t+', x))
        
    f.close()

    return my_lt


def hms_to_sec(val):
    l = val.split(':')
    sec = int(l[1])*60 + int(l[2])
    return sec


def create_df_list(my_lt):
    result = []

    for i in my_lt:
        trust_with_task_list = i[0].split(',')
        task_trust_dict = {val.strip().split('-')[1].strip():val.strip().split('-')[0].strip()  for val in trust_with_task_list}

        task_with_timestamp = i[1].split(',')
        task_timestamp_dict = {val.strip().split('-')[1].strip():val.strip().split('-')[0].strip()  for val in task_with_timestamp}

        df1 = pd.DataFrame(task_trust_dict.values(), index=task_trust_dict.keys())
        df1.rename(columns={0:"TrustID"}, inplace=True)

        df2 = pd.DataFrame(task_timestamp_dict.values(), index=task_timestamp_dict.keys())
        df2.rename(columns={0:"Time Taken (h:m:s)"}, inplace=True)

        final_df = df1.join(df2)

        final_df["Time(in sec)"] = final_df["Time Taken (h:m:s)"].apply(hms_to_sec)
        
        result.append(final_df)

    return result


def make_chart(df):
    selection = alt.selection_interval(encodings=['x'])

    colorCondition = alt.condition(selection, alt.value('lightgreen'), alt.value('gray'))

    x = alt.Chart(df).mark_bar().encode(
        x=alt.X('TrustID', sort='-x'),
        y='Time(in sec)',
        tooltip = ['TrustID', 'Time Taken (h:m:s)'],
        color=colorCondition
    ).interactive().add_selection(selection).properties(
        width=500,
        height=400
    )
    
    return x


def trust_frame(result_frames, trust_id):
    #trust_id = "ODART20181"
    trust_dframe = None
    for dframe in result_frames:
        trust_row = dframe[dframe['TrustID'] == trust_id]
        if trust_dframe is None:
            trust_dframe = trust_row
        else:
            trust_dframe = pd.concat([trust_dframe, trust_row], axis=0)
        
    return trust_dframe


def trust_chart(trust_frame, trust_id):
    x = alt.Chart(trust_frame.reset_index()).mark_bar().encode(
        x='index',
        y='Time(in sec)',
        color=alt.value('lightgreen'),
    ).properties(title=trust_id, width=300)
    
    return x