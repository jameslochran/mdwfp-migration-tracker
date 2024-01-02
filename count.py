import pandas as pd
import re

def count_slashes_in_urls(df, url_column, new_column_name="num_slashes"):
    """
    Counts the number of forward slashes in URLs within a pandas DataFrame column and adds a new column with the counts.

    Args:
        df (pandas.DataFrame): The DataFrame containing the URL column.
        url_column (str): The name of the column containing the URLs.
        new_column_name (str, optional): The name of the new column to create with the slash counts. Defaults to "num_slashes".

    Returns:
        pandas.DataFrame: The DataFrame with the additional column containing the slash counts.
    """

    df[new_column_name] = df[url_column].apply(lambda url: len(re.findall(r"/\/", url)))
    return df

# Example usage

df = pd.read_csv('folder/out.csv').astype(str) 
# df['new_column_name'] = df['url'].apply(lambda url: len(re.findall(r"/\/", 'url')))
# df['count'] = df['Legacy URL'].apply(lambda x: x.count('/'))
# df['IP'] = df['IP'].astype('datetime64[ns]')
# df['Content Review'] = pd.to_datetime(df['Content Review'])
# df['Client Review'] = pd.to_datetime(df['Client Review'])
# df['Done'] = pd.to_datetime(df['Done'])
df['IP'] = pd.Timestamp('now')
df['Content Review'] = pd.Timestamp('now')
df['client Review'] = pd.Timestamp('now')
df['Done'] = pd.Timestamp('now')



print(df)
df.to_csv('folder/out.csv', index=False) 
