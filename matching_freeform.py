from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
from nltk.corpus import stopwords
import pandas as pd

## You need to download these stopword list to your local
#nltk.download('punkt')
#nltk.download('stopwords')

#Spot Check that you have a list of stop words
basic_list = list(stopwords.words('english'))
#basic_list = ['contains', 'contain', 'table', 'tables', 'can', 'find', 'does', 'column', 'what', 'the']


def get_column_names(df):
    """
    INPUT: A dataframe
    OUTPUT: List of list of cleaned column names
    PURPOSE: To get a list of column names split
    """
    #Fill in blanks
    df = df.fillna(method='ffill')

    #lower a list
    df.columns = list(map(str.lower, df.columns))

    map(lambda s: s.replace("_"," ").replace(".","").replace("?","").strip(),df['revised_column_name'])

    new = df.drop_duplicates(subset='revised_column_name', keep='first')

    #For the moment just take the set since this column is still being filled out with names
    a = list(new['revised_column_name'])

    #Strips out _ character
    #a = list(map(lambda s: s.replace("_"," ").replace(".","").replace("?","").strip(), a))

    #Lowers Column information
    return list(map(str.lower, a))


def get_defs(df):

    df = df.fillna(method='ffill')

    #lower a list
    df.columns = list(map(str.lower, df.columns))

    map(lambda s: s.replace("_"," ").replace(".","").replace("?","").strip(),df['revised_column_name'])

    new = df.drop_duplicates(subset='revised_column_name', keep='first')

    #For the moment just take the set since this column is still being filled out with names

    a = list(new['definition'])

    #Strips out _ character
    #a = list(map(lambda s: s.replace("_"," ").replace(".","").replace("?","").strip(), a))

    #Lowers Column information
    return list(map(str.lower, a))



def add_stopword(stopword_list, new_words_to_add):
    """
    INPUT:Old stop word list, list of new words
    OUTPUT: Revised list of new stop words
    PURPOSE: To take into account increasing vocabulary that may or may not be relevant for finding material
    """
    for word in new_words_to_add:
            stopword_list.append(word)

    return stopword_list


def getidea(userinput, stwords):
    from nltk.corpus import stopwords
    """
    INPUT: A string based on user input to the search box
    OUTPUT: Split string - the stop words to narrow down the search
    PURPOSE: To narrow down a user search to basic idea
    """
    user_input = list(userinput.split())

    revised_set = []
    for word in user_input:
        if word not in set(stwords):
            revised_set.append(word)

    return revised_set


def getdefideas(def_lst, stwords):
    condensed_defs = list()

    for definition in def_lst:
        sep_def = list(definition.split())
        condensed_def = []
        for word in sep_def:
            if word not in set(stwords):
                condensed_def.append(word)
        concat_def = " ".join(condensed_def)
        condensed_defs.append(concat_def)
    return condensed_defs



def getcolfuzzymatch(user_question, new_stopwords, clean_col_names):
    """
    INPUT:
    OUTPUT:
    PURPOSE:
    """
    user_idea = getidea(user_question, new_stopwords)
    concat_user_idea = " ".join(user_idea)

    dictionary = {}
    for col in clean_col_names:
        name_ratio = fuzz.ratio(user_idea, col)
        dictionary[col] = name_ratio

    return dictionary

def getdeffuzzymatch(user_question, new_stopwords, clean_defs):
    user_idea = getidea(user_question, new_stopwords)
    concat_user_idea = " ".join(user_idea)

    lst = list()
    for definition in clean_defs:
        def_ratio = fuzz.ratio(user_idea, definition)
        lst.append(def_ratio)

    return lst

def scoretable(dictionary, lst):
    score_table = pd.DataFrame(list(dictionary.items()), columns=["colName", "colNameScore"])

    score_table.insert(2, "defScore", lst, True)
    return score_table

def get_composite_scores(df):
    comp_scores = list()

    for row in df.itertuples():
        composite_score = (0.7 * row.colNameScore) + (0.3 * row.defScore)
        comp_scores.append(composite_score)

    df.insert(3,"compScore", comp_scores, True)

    final = df[['colName', 'compScore']]

    dictionary = pd.Series(final.compScore.values,index=final.colName).to_dict()

    return dictionary



def get_best_matches(dictionary, threshold=30):
    """
    INPUT: A dictionary and a threshold for the fuzzy match
    OUTPUT: Sorting a dictionary based on values which pass the fuzzy match threshold
    PURPOSE: To sort a dictionary based on the values contained
    """
    new_dict = {}
    for key, value in sorted(dictionary.items(), key=lambda item: (item[1], item[0])):
        if value > threshold:
            new_dict[key] = value

    #Without specifying -1 and turning it into a list new_dic will generate multiple possible
    #combinations of column names for the user based on their request.
    #For now it is taking the max, or last score in the list since it is ordered ordered dictionary
    top_5 = list(new_dict)[-5:]
    top_5_upper = []
    for name in top_5:
        up = name.upper()
        top_5_upper.insert(0,up)
    return top_5_upper

def get_rows(name):
    """
    INPUT:
    OUTPUT:
    PURPOSE:
    """
    df = pd.read_csv(r'C:/Users/zhangje/Desktop/updated_bval.csv', encoding = 'unicode_escape')
    return df[df['Revised_Column_Name']==str(name)]


def top5(searchterm):
    df2 = pd.read_csv(r'C:/Users/zhangje/Desktop/updated_bval.csv', encoding = 'unicode_escape')
    clean_col_names = get_column_names(df2)
    clean_defs = get_defs(df2)
    col_dictionary = getcolfuzzymatch(searchterm, basic_list, clean_col_names)
    condensed = getdefideas(clean_defs, basic_list)
    def_list = getdeffuzzymatch(searchterm, basic_list, condensed)
    score_table = scoretable(col_dictionary, def_list)
    scores = get_composite_scores(score_table)
    probable_col_names = get_best_matches(scores, 10)
    return probable_col_names
