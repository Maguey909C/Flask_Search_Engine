from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
import pandas as pd
import numpy as np
import database_query
from warnings import simplefilter

simplefilter(action='ignore', category=FutureWarning)

def lowerColumn(list_of_strings):
    """
    INPUT: A list of strings
    OUTPUT: Same list with strings lower case
    """
    return list(map(str.lower, list_of_strings))

def removePunctuation(list_of_strings):
    """
    INPUT: A list of strings
    OUTPUT: Same list but with punctuation removed
    """

    return  list(map(lambda s: s.replace("_"," ").replace(".","").replace("?","").strip(), list_of_strings))

def getUniqueDf(df, colname):
    """
    INPUT: A dataframe
    OUTPUT: List of list of cleaned column names
    PURPOSE: To get a list of column names split
    """
    #Fill in blanks
    df = df.fillna("UNKNOWN")

    #Dropping duplicate revised names
    unique_df = df.drop_duplicates(subset='revised columns name', keep='first')

    #Take Uniques, remove punctuation, lower them
    all_names = list(unique_df['revised columns name'])
    all_names = removePunctuation(all_names)
    all_names = lowerColumn(all_names)
    unique_df['cleaned col names']= all_names

    #Do stuff with definition
    clean_def = lowerColumn(list(unique_df['definition']))
    clean_def = removePunctuation(clean_def)
    unique_df['cleaned definitions'] = clean_def

    return unique_df

def getIdea(userinput, stwords):
    from nltk.corpus import stopwords
    """
    INPUT: A string based on user input to the search box
    OUTPUT: Split string - the stop words to narrow down the search
    PURPOSE: To narrow down a user search to basic idea
    """
    user_input = list(userinput.split())
    idea = [word for word in user_input if word not in stwords]


    return idea


def getDefIdeas(list_of_definitions, stwords):
    """
    INPUT:
    OUTPUT:
    PURPOSE:
    """
    condensed_defs = list()

    for definition in list_of_definitions:
        sep_def = list(definition.split())
        condensed_def = [word for word in sep_def if word not in set(stwords)]
        concat_def = " ".join(condensed_def)
        condensed_defs.append(concat_def)

    return condensed_defs

def getColFuzzyMatch(userInput, new_stopwords, clean_col_names):
    """
    INPUT: User's input, the stopwords, and the column names to compare
    OUTPUT: A list of all the fuzzy match scores based on the user's input
    PURPOSE: To generate all possible scores for the fuzzy match based on the user's input
    """
    user_idea = getIdea(userInput, new_stopwords)
    concat_user_idea = " ".join(user_idea)
    col_values = [fuzz.ratio(user_idea, col) for col in clean_col_names]

    return col_values

def getDefFuzzyMatch(userInput, new_stopwords, clean_defs):
    """
    INPUT:
    OUTPUT:
    PURPOSE:
    """
    user_idea = getIdea(userInput, new_stopwords)
    concat_user_idea = " ".join(user_idea)

    def_values = [fuzz.ratio(user_idea, definition) for definition in clean_defs]

    return def_values

def finalDF(df, col_fuzzy_scores, def_fuzzy_scores):
    """
    INPUT: A dataframe, all associated column fuzzy scores, all associated def fuzzy scores
    OUTPUT: A dataframe with the additional col, def, and composite columns
    PURPOSE: To have a consolidated dataframe of all the relative information so that scores can be calculated
    """
    df['col fuzzy scores'] = col_fuzzy_scores
    df['def fuzzy scores'] = def_fuzzy_scores
    df['composite scores'] = (np.asarray(df['col fuzzy scores'])*0.7) + (np.asarray(df['def fuzzy scores'])*0.3)

    return df


def getBestMatches(df, threshold=30, top_how_many=10):
    """
    INPUT: A dataframe, a fuzzy match threshold, how many results you want to show
    OUTPUT: A list of the top how many column names based on fuzzy match composite score
    PURPOSE: To return the highest scores based on what the user typed into the search
    """
    return list(df[df['composite scores']>threshold].sort_values(by='composite scores', ascending=False).head(top_how_many)['revised columns name'])

def topColumns(df, userInput, number_of_responses):
    """
    INPUT: A dataframe and the user's input
    OUTPUT:
    PURPOSE:
    """

    #Taking basic stop words
    basic_list = list(stopwords.words('english'))

    #Get the cleaned column names
    df = getUniqueDf(df,'revised column name')

    #Producing Column Fuzzy Scores for each revised column name
    col_fuzzy_scores = getColFuzzyMatch(userInput, basic_list, df['cleaned col names'])

    #Making a condensed definition
    condensed = getDefIdeas(df['cleaned definitions'], basic_list)

    #Producing definitio fuzzy scores for each def
    def_fuzzy_scores = getDefFuzzyMatch(userInput, basic_list, condensed)

    #Making the final df with all relative information
    df = finalDF(df, col_fuzzy_scores, def_fuzzy_scores)

    return getBestMatches(df , 30, number_of_responses)


def findRow(userSelection):
    """
    INPUT: What the user selected from the available options
    OUTPUT: A dataframe which will be parsed for the webpage
    PURPOSE: To find the exact row that the user has selected
    """
    df = database_query.searchDataFrame()
    return df[df['Revised_Columns_Name']==str(userSelection)]

def optimizeSearch(userInput):
    """
    INPUT: A dataframe, the user's input
    OUTPUT: Either the definition of the exact column name or a estimated column based on
    PURPOSE: To determine whether the user is searching for a column or for simply a definition
    """
    df = database_query.searchDataFrame()

    #Lowering and removing punctuation in column names
    df.columns = lowerColumn(df.columns)
    df.columns = removePunctuation(df.columns)
    # userInput = userInput.lower()

    #Stripping User Input of white space
    userInput = userInput.strip()
    all_columns = (list(map(lambda s: s.strip(), df['colname'])))

    if userInput in all_columns:
        def_index = all_columns.index(userInput)
        found_column = [df.iloc[def_index]['revised columns name']]
        return found_column
    else:
        return topColumns(df,userInput, 10)
