# Gitty --- IBM Summer Project 2019
# Kavan Lam and Nimrah Gill
# July 19, 2019

"""
The following uses the models created from model_creation to make predictions
"""

### Importing required modules ###
from model_creation import *
from gensim.models import KeyedVectors
import ast
import keras

def model_prediction(issue_text):
    global word2vec_model_global
    global keras_model_global

    ### Attempt to load in keras and word2vec model ###
    # Check the word2vec model
    if word2vec_model_global is None:
        if not(word2vec_small_exist()):
            return 500
        else:
            word2vec_model_global = KeyedVectors.load(word2vec_model_location + word2vec_small_name, mmap="r")
    # Check keras model
    if keras_model_global is None:
        if not(keras_model_exist()):
            return 500
        else:
            keras.backend.clear_session()
            keras_model_global = load_model(keras_model_location + keras_model_name)

    ### Load in the list of teams and assignees ###
    file1 = open(assignee_team_location + team_output_dict_name, "r")
    file2 = open(assignee_team_location + assignee_output_dict_name, "r")
    team_mapping = ast.literal_eval(file1.read())
    assignee_mapping = ast.literal_eval(file2.read())
    file1.close()
    file2.close()

    ### Turn issue text into a vector ###
    issue_text = remove_punctuation(issue_text)
    issue_text = issue_text.lower()
    issue_text_list = [get_index_of_word_keyvector(word, word2vec_model_global) for word in issue_text.split(" ") if word != ""]
    issue_text_list = [issue_text_list]
    issue_text_list = pad_sequences(issue_text_list, maxlen=max_length, padding="post", value=0)

    ### Make thr predictions ###
    probabilities = keras_model_global.predict(np.array(issue_text_list))
    best_team = []
    best_assignee = []

    # Get the best team
    for i in range(3):
        index = np.array(probabilities[0][0]).argmax()
        for key, value in team_mapping.items():
            if index == value:
                best_team.append(key)
                probabilities[0][0][value] = -1
                break

    # Get the best assignee
    for i in range(3):
        index = np.array(probabilities[1][0]).argmax()
        for key, value in assignee_mapping.items():
            if index == value:
                best_assignee.append(key)
                probabilities[1][0][value] = -1
                break

    return [best_assignee, best_team]


def get_index_of_word_keyvector(word, w2v_model_in):
    """
    Return the index of the given word from the Word2Vec wv model. Return 0 if the word is not in the model.
    """
    try:
        return w2v_model_in.vocab[word].index
    except KeyError:
        return 0