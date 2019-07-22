#Author: Chase Renick
#Date: 7/2019
#Purpose: Functions to call database to perform query

#Importing Packages
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

#Main Connection and Query tool
def getData(selectStr):
    """
    INPUT: A SQL Query
    OUTPUT: A dataframe from DB2
    PURPOSE: To connect to a database and return a dataframe based on the query specified
    """
    
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

#Function to get your specific table
def searchDataFrame():
    """
    INPUT: User search command
    OUTPUT: Dataframe from database based on SQL query
    """
    return getData("""SELECT * FROM schema.table_name""")
