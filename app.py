import datetime
import os
import shutil
from pathlib import Path

import fitdecode
import pandas as pd
import plotly.express as px
import streamlit as st

current_dir = os.path.dirname(__file__)


def load_fit_tmp(path):
    """
    this is an only sample function
    load fit file and convert to dataframe
    you should change codes below for fit file structure that you expect
    """
    list_record = []
    with fitdecode.FitReader(path) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.records.FitDataMessage):
                if frame.name == "record":
                    for field in frame.fields:
                        list_record.append(field.value)
    list_record = [
        x for x in list_record
        if (x is not None) and (type(x) != datetime.datetime)
    ]
    df = pd.DataFrame({"lap": list_record})
    return df


@st.cache
def convert_df(df):
    """
    convert df to csv
    """
    return df.to_csv(index=False).encode('utf-8')


def calc_tmp(df):
    """
    this is an only sample function
    you should define process for your purpose
    """
    df = df.loc[0:100, :]
    return df


# upload .fit file
uploaded_file = st.file_uploader("upload your .fit file")
if uploaded_file is not None:
    # set path
    data_directory_path = Path(current_dir, "data")
    file_path = Path(data_directory_path, uploaded_file.name)

    # make data directory
    if data_directory_path.exists():
        shutil.rmtree(data_directory_path)
    os.makedirs(data_directory_path)

    # export .file to data directory
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # load fit file and convert to dataframe
    df = load_fit_tmp(file_path)

    # data processing
    df = calc_tmp(df)

    # show df
    fig = px.line(df, x=df.index, y="lap", title="lap")
    st.plotly_chart(fig, use_container_width=True)

    # convert df to csv
    csv = convert_df(df)

    # download
    st.download_button(
        label="Download",
        data=csv,
        file_name='sample.csv',
        mime='text/csv',
    )
