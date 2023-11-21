import pandas as pd
import numpy as np
import pickle
from tqdm import tqdm
import base64
from IPython.display import HTML, Markdown
import os
import sys
import warnings
import calendar
from datetime import datetime, timedelta
import plotly.express as px
from io import StringIO
import calendar
import itertools

def df_dl(df, title = 'Download', filename = 'Download'):
    csv = df.to_csv()
    b64 = base64.b64encode(csv.encode())
    payload = b64.decode()
    html = '<a download="{filename}" href="data:text/csv;base64,{payload}" target="_blank">{title}</a>'
    html = html.format(payload=payload, title=title, filename=filename)
    display(HTML(html))

def run_query(query):
    return pd.read_gbq(query,auth_local_webserver = True, project_id = 'storm-wall-185017')

def rq(query):
    return pd.read_gbq(query,auth_local_webserver = True, project_id = 'storm-wall-185017')

def tc(df):
    df.to_clipboard(index = False)
    
def export_gbq(df, table_name):
    df.to_gbq(table_name, 
                 chunksize=10000, 
                 if_exists='replace',
                 auth_local_webserver = True, project_id = 'storm-wall-185017'
                 )    

def null_rate_checker(table_name, base_col):
    null_col_str = ''
    col_list = list(rq(f"""select * from {table_name} limit 1000""").columns)
    for i,j in enumerate(col_list):
        if i < len(col_list):
            temp_col_str = f"""count(distinct case when {j} is null then {base_col} end)/count(distinct {base_col}) as {j}_null_rate,"""
        else:
            temp_col_str = f"""count(distinct case when {j} is null then {base_col} end)/count(distinct {base_col}) as {j}_null_rate"""
        null_col_str = null_col_str + temp_col_str
    
    final_query = f"""select {null_col_str} from {table_name}"""
    return rq(final_query)

def get_cols(table_name):
    query = f"""select * from {table_name} limit 1000"""
    return list(rq(query).columns)

def get_sample(table_name):
    query = f"""select * from {table_name} limit 1000"""
    return rq(query)
    
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)    