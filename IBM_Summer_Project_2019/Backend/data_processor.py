# Gitty --- IBM Summer Project 2019
# Kavan Lam and Nimrah Gill
# July 19, 2019

"""
The following is a collection of functions that model_creation will use
to process data to make it compatible with word2vec and Keras
"""

### Required modules to assist with data processing ###
import pandas as pd
import string
import numpy as np


### Defining constants ###
# The data below was retrieved from https://github.com/OpenLiberty/open-liberty/wiki/Open-Liberty-Teams and will help
# improve the quality of the data as we can fill in missing data when it is known
known_team_to_person_mapping = {'Teams Assigned': ['Blizzard', 'Blizzard', 'Blizzard', 'Blizzard', 'Blizzard',
                             'Zombie Apocalypse', 'Zombie Apocalypse', 'Zombie Apocalypse', 'Zombie Apocalypse', 'Zombie Apocalypse', 'Zombie Apocalypse', 'Zombie Apocalypse',
                             'OSGi Infrastructure', 'OSGi Infrastructure', 'OSGi Infrastructure', 'OSGi Infrastructure', 'OSGi Infrastructure',
                             'Security SSO', 'Security SSO', 'Security SSO', 'Security SSO', 'Security SSO',
                             'Wendigo East', 'Wendigo East', 'Wendigo East', 'Wendigo East',
                             'Wendigo West', 'Wendigo West', 'Wendigo West', 'Wendigo West',
                             'CSI', 'CSI', 'CSI', 'CSI', 'CSI',
                             'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals', 'Narwhals',
                             'MicroProfileUK', 'MicroProfileUK', 'MicroProfileUK', 'MicroProfileUK', 'MicroProfileUK', 'MicroProfileUK',
                             'Libra', 'Libra', 'Libra', 'Libra', 'Libra', 'Libra',
                             'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI', 'Admin UI',],
          'Assignees': ['brideck', 'jgrassel', 'olendvcook', 'tkburroughs', 'dazey3',
                        'aguibert', 'frowe', 'jmstephensgit', 'KyleAure', 'mswatosh', 'njr-11', 'nmittles',
                        'tjwatson', 'sebratton', 'anjumfatima90', 'dazavala', 'jaridk',
                        'ayoho', 'arunavemulapalli', 'brutif', 'c00crane', 'chunlongliang-ibm',
                        'agiridharan', 'jvanhill', 'kristip17', 'ryanesch',
                        'WhiteCat22', 'andymc12', 'jim-krueger', 'jkoehler22',
                        'sabolo', 'mhldr', 'websterc87', 'SYLVAING', 'dave-waddling',
                        'uberskigeek', 'jarcher-IBM', 'kberkos-public', 'ginnick', 'kaczyns', 'mezarin', 'garypicher', 'tspewak', 'awisniew90', 'Viane', 'ThomasGHenry',
                        'benjamin-confino', 'tevans78', 'jonhawkes', 'hutchig', 'Emily-Jiang', 'neilgsyoung',
                        'Charlotte-Holt', 'dmuelle', 'jantley-ibm', 'chirp1', 'helyarp', 'Rwalls1',
                        'k8vance88', 'kinueng', 'mbroz2', 'erica-banda-03', 'steven1046', 'lavenal', 'aknguyen7', 'dmorgant', 'amyreit', 'ellenwyllie']}
known_team_to_person_data_frame = pd.DataFrame(data=known_team_to_person_mapping)
nan_team_filler = "No Team"
nan_assignee_filler = "No Assignee"
drop_threshold = 3


### Defining helper functions ###
def read_csv_data(csv_data):
    """
    Read in data from csv_data and parse it into a a data frame
    """
    df = pd.read_csv(csv_data, error_bad_lines=False)
    return df


def remove_nan_rows(data_frame):
    """
    Remove rows with nan for all output columns
    """
    df = data_frame.dropna(thresh=2).iloc[:, :].reset_index(drop=True)
    return df


def fill_missing_team(data_frame):
    """
    Fill in the missing value for "Teams Assigned" in the data_frame data, when "Assignees" is not NaN and the
    information is known
    """
    # Dealing with cases where there are no multiple values in a column
    data_frame[["Teams Assigned", "Assignees"]] = data_frame.set_index("Assignees")["Teams Assigned"].fillna(
        known_team_to_person_data_frame.set_index("Assignees")["Teams Assigned"]).reset_index()[["Teams Assigned", "Assignees"]].values

    # Dealing with cases where there are multiple values in a column
    for i in range(len(data_frame)):
        assignee_val = data_frame["Assignees"][i]
        if pd.notna(assignee_val):
            assignees = assignee_val.split(',')
            if len(assignees) > 1:
                for assignee in assignees:
                    if assignee in known_team_to_person_data_frame['Assignees'].values:
                        if pd.isna(data_frame["Teams Assigned"][i]):
                            data_frame["Teams Assigned"][i] = \
                                known_team_to_person_data_frame[known_team_to_person_data_frame['Assignees'] == assignee]['Teams Assigned'].values[0]
                        elif (known_team_to_person_data_frame[known_team_to_person_data_frame['Assignees'] == assignee]['Teams Assigned'].values[0] not in
                              data_frame["Teams Assigned"][i]):
                            data_frame["Teams Assigned"][i] += ', ' + known_team_to_person_data_frame[known_team_to_person_data_frame['Assignees'] == assignee][
                                'Teams Assigned'].values[0]
    return data_frame


def replace_nan(data_frame):
    """
    Replace all the nan entries with appropriate filler
    """
    data_frame["Teams Assigned"] = data_frame["Teams Assigned"].fillna(nan_team_filler)
    data_frame["Assignees"] = data_frame["Assignees"].fillna(nan_assignee_filler)
    return data_frame


def remove_punctuation(input_str):
    """
    Removes all the punctuation from input_string and return the new string
    """
    new_str = input_str.translate(str.maketrans("", "", string.punctuation))
    return new_str


def get_all_issue_text(data_frame):
    """
    Retrieve all the issue text from data_frame and structure it such that each
    issue gets one sublist and within the sublist are the words without punctuation
    and lower cased from the issue. Each word is one element/string.
    """
    all_issue_text = []
    for i in range(len(data_frame.iloc[:, 0])):
        issue_text = data_frame.iloc[i, 0]
        if issue_text == "":
            continue
        issue_text = remove_punctuation(issue_text)
        issue_text = issue_text.lower()
        words_from_issue = [word for word in issue_text.split(" ") if word != ""]
        all_issue_text.append(words_from_issue)
    return all_issue_text


def get_output_dict(data_frame, option_num):
    # Determine which category we want
    if option_num == 1:
        column_title = "Teams Assigned"
    else:
        column_title = "Assignees"

    # Retrieve the data
    all_unique_values, value_counts = np.unique(data_frame[column_title], return_counts=True)
    return_dict = {}
    mapping_value = 0
    for key, count in zip(all_unique_values, value_counts):
        if count >= drop_threshold or key == nan_team_filler or key == nan_assignee_filler:
            return_dict[key] = mapping_value
            mapping_value += 1
    return return_dict


def get_word_from_index(index, w2v_model_in):
    """
    Returns the word at given index from the Word2Vec model. Return the word at index 0 if given index is
    out of range.
    """
    try:
        return w2v_model_in.wv.index2word[index]
    except IndexError:
        return w2v_model_in.wv.index2word[0]


def get_index_of_word(word, w2v_model_in):
    """
    Return the index of the given word from the Word2Vec model. Return 0 if the word is not in the model.
    """
    try:
        return w2v_model_in.wv.vocab[word].index
    except KeyError:
        return 0


def vectorize_data(data_frame, team_output_dict, assignee_output_dict, w2v_model, max_length):
    input_vector = []
    full_output_vector = []
    output_vector_team = []
    output_vector_assignee = []

    for issue_text, team, assignee in zip(data_frame.iloc[:, 0], data_frame.iloc[:, 1], data_frame.iloc[:, 2]):
        issue_text = issue_text.lower()
        issue_text = remove_punctuation(issue_text)
        words_in_issue_text = np.array([get_index_of_word(word, w2v_model) for word in issue_text.split(" ")
                                       [:max_length] if word != ""])
        input_vector.append(words_in_issue_text)
        if team in team_output_dict.keys():
            output_vector_team.append(team_output_dict[team])
        else:
            output_vector_team.append(team_output_dict[nan_team_filler])
        if assignee in assignee_output_dict.keys():
            output_vector_assignee.append(assignee_output_dict[assignee])
        else:
            output_vector_assignee.append(assignee_output_dict[nan_assignee_filler])

    full_output_vector.append(np.array(output_vector_team))
    full_output_vector.append(np.array(output_vector_assignee))

    return input_vector, full_output_vector

