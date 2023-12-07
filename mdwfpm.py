import streamlit as st
import pandas as pd
import numpy as np

st.title('MDWFP Migration Tracker')




DATA_URL = ('MDWFP_import.csv')

df = pd.read_csv(DATA_URL)
users = ['Jim', 'Bob', 'Sally']
config = {
    'Assignment' : st.column_config.SelectboxColumn('Name', options=users)
}
df['In Progress'] = False
df['Content Review'] = False
df['Client Review'] = False
df['Done'] = False


       




st.subheader('Raw data')

# edited_df = st.data_editor(df)
st.data_editor(df, column_config=config)


