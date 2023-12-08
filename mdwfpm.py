import streamlit as st
import pandas as pd
import numpy as np
import os
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

st.title('MDWFP Migration Tracker')

def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')



# DATA_URL = ()

df = pd.read_csv('folder/out.csv').astype(str) 
df['Notes'] = ''
users = ['Jim', 'Bob', 'Sally']
progress = ['In Progress', 'Content Review', 'Client Review', 'Done']
config = {
    'Assignment' : st.column_config.SelectboxColumn('Name', options=users),
    'State' : st.column_config.SelectboxColumn('State', options=progress),
    'Content Guidance' : st.column_config.Column('Notes', help="Add notes here",
            width="large")
}
df = df.astype(str)




       




st.subheader('Raw data')

# edited_df = st.data_editor(df)
edited_df=st.data_editor(df, column_config=config, column_order=('State', 'Assignment', 'Content Guidance','URL', 'Title', 'Suggested Title'))



button = st.button("Save")

st.write('Make sure you save your changes')

if button:
    os.makedirs('folder/', exist_ok=True)
    edited_df.to_csv('folder/out.csv', index=False) 


#Filtered results
def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df 
    
df = df.copy()
modification_container = st.container()




st.dataframe(filter_dataframe(df)
)

def filters_widgets(df, columns=None, allow_single_value_widgets=False):
    # Parse the df and get filter widgets based for provided columns
    if not columns: #if columns not provided, use all columns to create widgets
        columns=df.columns.tolist()
    if allow_single_value_widgets:
        threshold=0
    else:
        threshold=1
    widget_dict = {}
    filter_widgets = st.container()
    filter_widgets.warning(
        "After selecting filters press the 'Apply Filters' button at the bottom.")
    if not allow_single_value_widgets:
        filter_widgets.markdown("Only showing columns that contain more than 1 unique value.")
    with filter_widgets.form(key="data_filters"):
        not_showing = [] 
        for y in df[columns]:
            if str(y) in st.session_state: #update value from session state if exists
                selected_opts = st.session_state[str(y)]
            else: #if doesnt exist use all values as defaults
                selected_opts = df[y].unique().tolist()
            if len(df[y].unique().tolist()) > threshold: #checks if above threshold
                widget_dict[y] = st.multiselect(
                    label=str(y),
                    options=df[y].unique().tolist(),
                    default=selected_opts,
                    key=str(y),
                )
            else:#if doesnt pass threshold
                not_showing.append(y)
        if not_showing:#if the list is not empty, show this warning
            st.warning(
                f"Not showing filters for {' '.join(not_showing)} since they only contain one unique value."
            )
        submit_button = st.form_submit_button("Apply Filters")
    #reset button to return all unselected values back
    reset_button = filter_widgets.button(
        "Reset All Filters",
        key="reset_buttons",
        on_click=reset_filter_widgets_to_default,
        args=(df, columns),
    )
    filter_widgets.warning(
        "Dont forget to apply filters by pressing 'Apply Filters' at the bottom."
    )

def reset_filter_widgets_to_default(df, columns):
    for y in df[columns]:
        if str(y) in st.session_state:
            del st.session_state[y]


filters_widgets(df)    