Author: Chase Renick
Date: 7/2019
Purpose: Functions to call database to perform query

//Importing Packages
import pandas as pd
import numpy as np
from collections import Counter
from collections import OrderedDict
from itertools import combinations
import operator
import vertica_python
import sys
import ssl
import re

def getData(selectStr):
    tempDF=pd.DataFrame()
    conn_info = {'host': '11.11.11.111',
             'port': 0000,
             'user': 'username',
             'password': 'you wish!',
             'database': 'whatevz',
             # 10 minutes timeout on queries
             'read_timeout': 1000,
             # default throw error on invalid UTF-8 results
             'unicode_error': 'strict',
             # SSL is disabled by default
             'ssl': False,
             'connection_timeout': 100
         }
    # simple connection, with manual close
    connection = vertica_python.connect(**conn_info)
    cur = connection.cursor()
    cur.execute(selectStr)
    #get the data
    data_rows=cur.fetchall()
    #dataframe!
    tempDF = pd.DataFrame(data_rows)
    #column Names
    ColumnList = [d.name for d in cur.description]
    #name them correctly
    tempDF.columns=ColumnList
    connection.close()
    return tempDF
# user_query = getData("""SELECT * as tids FROM dsl.BVALTABLE_NEW WHERE COL_NAME LIKE = '% """ +str(users_command)+"%'")

def get_col(users_command):
    """
    INPUT: User search command
    OUTPUT: Dataframe from database based on SQL query
    """
    # df = getData("""SELECT * FROM dsl.BVAL_DATA_DICT_POC WHERE TEAM_NM = '""" +str(users_command)+"'") #GC SHADOW
    df = getData("""SELECT * FROM some table WHERE ColumnName = '""" +str(users_command)+"'") #GC SHADOW

    #what to do when invalid column is entered in search
    return df
