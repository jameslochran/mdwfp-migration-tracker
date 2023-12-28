# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
import numpy as np
import os
import hmac
import csv
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

LOGGER = get_logger(__name__)

def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


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

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter table on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df
def getData():
    df = pd.read_csv('folder/out.csv').astype(str) 
    


    
    merge = ["Merge ⬆️", "Merge ⬇️"]   
    users = ['Jim', 'Sarah P', 'Sarah C', 'Braden']
    progress = ['Backlog','In Progress', 'Content Review', 'Client Review', 'Done']
    config = {
      'Assignment' : st.column_config.SelectboxColumn('Name', options=users),
      'State' : st.column_config.SelectboxColumn('State', options=progress),
      'Merge' : st.column_config.SelectboxColumn('Merge', options=merge),
      'Notes': st.column_config.TextColumn('Notes', width="Large"),
      'New URL': st.column_config.TextColumn('New URL', width="Medium"),
      'Legacy URL': st.column_config.LinkColumn('Legacy URL', help="URL to old site", validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,)
      
      
        }
    df = df.astype(str)
    return df


def run():
    st.set_page_config(page_title="Migration Tracker", page_icon="📄", initial_sidebar_state="collapsed", layout="wide", menu_items={'About': "# This is a header. This is an *extremely* cool app!"})
    


    st.title('MDWFP Migration Tracker')
    st.subheader('Track the progress of individual page migration status for the MDWFP project') 

    if not check_password():
        st.stop()


    df = getData()
    # df = pd.read_csv('folder/out.csv').astype(str) 
    
    
    merge = ["Merge ⬆️", "Merge ⬇️"] 
    users = ['Jim', 'Sarah P', 'Sarah C', 'Braden', 'Open']
    progress = ['Backlog','In Progress', 'Content Review', 'Client Review', 'Done']
    config = {
      'Users' : st.column_config.SelectboxColumn('Name', options=users),
      'State' : st.column_config.SelectboxColumn('State', options=progress, default='Backlog'),
      'Merge' : st.column_config.SelectboxColumn('Merge', options=merge, width="Large"),
      'Notes': st.column_config.TextColumn('Notes', width="Large"),
      'New URL': st.column_config.TextColumn('New URL', width="Medium"),
      'Legacy URL': st.column_config.LinkColumn('Legacy URL', help="URL to old site", validate="^https://[a-z]+\.streamlit\.app$",
            max_chars=100,)
      
        }
    df = df.astype(str)
    edited_df = df
    st.markdown('This table provides a view of the stories based on the filters that have been applied.')
    st.link_button("Figma Design", "https://www.figma.com/file/e6ygQs8uULxi9tx16aGnhu/Low-fidelity-Mock-ups?type=design&node-id=333%3A1743&mode=design&t=6GZLiRRRPt0HXqxG-1")
    st.markdown('Check the add filters box to see the filter options. Filters can be grouped by selecting multiple columns. ')
    filtered_df = st.data_editor(filter_dataframe(df),column_config=config, column_order=('State', 'Users', 'Notes','Merge','Legacy URL','New URL', 'Title', 'Suggested Title', 'Jira Epic'),key=1234 )

    
    edited_df.update(filtered_df)
    # st.dataframe(edited_df)

    button = st.button("Save")


    st.write('Make sure you save your changes')

    if button:
        os.makedirs('folder/', exist_ok=True)
        edited_df.to_csv('folder/out.csv', index=False) 
        edited_df = getData() 
        
  
        
   
    try: inprog = edited_df.groupby('State').size()['In Progress']  
    except KeyError:
        inprog = 0

    try: backlog = edited_df['State'].value_counts()['Backlog']  
    except KeyError:
        backlog = 0

    try: done = edited_df['State'].value_counts()['Done'] 
    except KeyError:
        done = 0 

    try: review = edited_df['State'].value_counts()['Client Review']
    except KeyError:
        review = 0   

    try: content = edited_df['State'].value_counts()['Content Review'] 
    except KeyError:
        content = 0 

    countofRows = len(edited_df)



    with st.expander("Story Metrics"):
        st.write('Story status metrics')
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Backlog", backlog)
        col1.metric('% ', backlog/countofRows*100)
        col2.metric("In Progress", inprog)
        col2.metric("%", inprog/countofRows*100)
        col3.metric("Content Review", review)
        col3.metric("%", review/countofRows*100)
        col4.metric("Client Review", content)
        col4.metric("%", content/countofRows*100)
        col5.metric("Done", done)
        col5.metric("%", done/countofRows*100)
    
  
    
    try: u1 = edited_df.groupby('Users').size()[users[0]]  
    except KeyError:
        u1 = 0

    try: u2 = edited_df.groupby('Users').size()[users[1]]  
    except KeyError:
        u2 = 0

    try: u3 = edited_df.groupby('Users').size()[users[2]]  
    except KeyError:
        u3 = 0

    try: u4 = edited_df.groupby('Users').size()[users[3]]  
    except KeyError:
        u4 = 0  

    try: u5 = edited_df.groupby('Users').size()[users[4]]  
    except KeyError:
        u5 = 0
    
    
       
    
    
    
    with st.expander("Migrator Metrics"):
        st.write('Number of stories assigned to each migrator')
        col6, col7, col8, col9, col10 = st.columns(5)
        col6.metric(users[0], u1)
        col7.metric(users[1], u2)
        col8.metric(users[2], u3)
        col9.metric(users[3], u4)
        col10.metric(users[4], u5)







   


          







if __name__ == "__main__":
    run()
