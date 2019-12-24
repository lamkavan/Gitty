# Gitty --- IBM Summer Project 2019
# Kavan Lam and Nimrah Gill
# July 19, 2019

# Note: Some of the code written here was inspired by the code at the following link
# https://www.kaggle.com/guichristmann/lstm-classification-model-with-word2vec/notebook#Defining-and-Training-LSTM-Model

"""
The following is the model creation process and is where the models are created and trained
"""

from data_processor import *
from keras.models import Model, load_model
from keras.layers import *
from keras.preprocessing.sequence import pad_sequences
import keras
import gensim
import glob
import os


### Defining constants ###
word2vec_model_location = "./models/"
keras_model_location = "./models/"
data_location = "../Frontend/output/"
assignee_team_location = "./list_of_team_assignees/"
open_liberty_name = "open-liberty.txt"
word2vec_large_name = "word2vec_large.model"
word2vec_small_name = "word2vec_small.kv"
keras_model_name = "keras_model.h5"
all_assignees_list = "list_of_assignees.txt"
all_teams_list = "list_of_team.txt"
team_output_dict_name = "team_output_dict.txt"
assignee_output_dict_name = "assignee_output_dict.txt"
keras_epochs = 3
word2vec_epochs = 2
max_length = 100
training_percentage = 0.90
### Defining special variables here ###
word2vec_model_global = None
keras_model_global = None


def model_creation():
    global word2vec_model_global
    global keras_model_global


    try:
        ### Collecting all issue text ###
        csv_files = [file for file in glob.glob(data_location + "**/*.*", recursive=True)]
        all_issue_text = []
        for csv_file in csv_files:
            if os.path.basename(csv_file) == all_assignees_list or os.path.basename(csv_file) == all_teams_list:
                continue
            # First lets read in the data and clean it up
            data_frame = read_csv_data(data_location + os.path.basename(csv_file))
            # Keep the data that is useful for training. Clean rows with NaN text for both "Teams Assigned" and "Assignees"
            data_frame = remove_nan_rows(data_frame)
            # Fill in missing team data that is known
            data_frame = fill_missing_team(data_frame)
            # Replace all nan entries with appropriate filler
            data_frame = replace_nan(data_frame)
            # Get the data from the cleaned csv files
            all_issue_text += get_all_issue_text(data_frame)


        ### Prepare the word2vec model and model information ###
        if word2vec_large_exist():
            # Simply load up the existing word2vec model for further training
            w2v_model = gensim.models.Word2Vec.load(word2vec_model_location + word2vec_large_name)
            w2v_model.build_vocab(all_issue_text, update=True)
            w2v_model.train(all_issue_text, total_examples=len(all_issue_text), epochs=word2vec_epochs)
        else:
            # Build a word2vec model from scratch as none currently exist
            w2v_model = gensim.models.Word2Vec(all_issue_text, size=200, min_count=2, window=5, workers=6, batch_words=800)

        w2v_weights = w2v_model.wv.vectors
        vocab_size, embeddings_size = w2v_weights.shape


        ### Get Open-liberty data from csv ###
        # First lets read in the data and clean it up
        data_frame = read_csv_data(data_location + open_liberty_name)
        # Keep the data that is useful for training. Clean rows with NaN text for both "Teams Assigned" and "Assignees"
        data_frame = remove_nan_rows(data_frame)
        # Fill in missing team data that is known
        data_frame = fill_missing_team(data_frame)
        # Replace all nan entries with appropriate filler
        data_frame = replace_nan(data_frame)


        ### Reformat data to be compatible with Keras neural network training (LSTM) ###
        # First we get two dictionaries that contains all possible outputs for teams and assignees
        team_output_dict = get_output_dict(data_frame, 1)
        assignee_output_dict = get_output_dict(data_frame, 2)
        # Now we turn the issue text and outputs into vectors
        input_vectors, output_vectors = vectorize_data(data_frame, team_output_dict, assignee_output_dict, w2v_model, max_length)
        input_vectors = pad_sequences(input_vectors, maxlen=max_length, padding="post", value=0)


        ### Here we split the full data set into a training and validation set
        num_of_training_data = int(training_percentage * input_vectors.shape[0])
        input_vector_train = input_vectors[:num_of_training_data]
        input_vector_val = input_vectors[num_of_training_data:]
        output_vectors_train = [output_vectors[0][:num_of_training_data], output_vectors[1][:num_of_training_data]]
        output_vectors_val = [output_vectors[0][num_of_training_data:], output_vectors[1][num_of_training_data:]]


        ### We finally build and train the neural network (LSTM) ###
        if keras_model_exist():
            # Load existing model and further train
            keras.backend.clear_session()
            keras_model = load_model(keras_model_location + keras_model_name)
            history = keras_model.fit(input_vector_train, output_vectors_train, epochs=keras_epochs, batch_size=64,
                                      validation_data=(input_vector_val, output_vectors_val), verbose=1)
        else:
            # Create a new model from scratch
            input_layer = Input(shape=(max_length,))
            embedding_layer = Embedding(input_dim=vocab_size,
                                output_dim=embeddings_size,
                                weights=[w2v_weights],
                                input_length=max_length,
                                mask_zero=True,
                                trainable=False)(input_layer)
            lstm_layer = Bidirectional(LSTM(110))(embedding_layer)
            x1 = Dense(50)(lstm_layer)
            output_1 = Dense(len(team_output_dict.keys()), activation="softmax")(x1)
            output_2 = Dense(len(assignee_output_dict.keys()), activation="softmax")(x1)
            keras_model = Model(inputs=input_layer, outputs=[output_1, output_2])
            keras_model.compile(optimizer="adam", loss=["sparse_categorical_crossentropy", "sparse_categorical_crossentropy"], metrics=["accuracy"])
            history = keras_model.fit(input_vector_train, output_vectors_train, epochs=keras_epochs, batch_size=64,
                                       validation_data=(input_vector_val, output_vectors_val), verbose=1)


        ### Save the word2vec and keras model (Replace existing ones) ###
        keras_model.save(keras_model_location + keras_model_name)
        w2v_model.save(word2vec_model_location + word2vec_large_name)
        w2v_model.wv.save(word2vec_model_location + word2vec_small_name)
        file1 = open(assignee_team_location + team_output_dict_name, "w")
        file2 = open(assignee_team_location + assignee_output_dict_name, "w")
        file1.write(str(team_output_dict))
        file2.write(str(assignee_output_dict))
        file1.close()
        file2.close()


        ### Store the models in global variables so model predict can use them ###
        word2vec_model_global = w2v_model.wv
        keras_model_global = keras_model


        ### Return the accuracy and results ###
        accuracy = keras_model.evaluate(input_vector_val, output_vectors_val, verbose=0)
        return accuracy
    except:
        return 500


def word2vec_large_exist():
    files = [os.path.basename(file) for file in glob.glob(word2vec_model_location + "**/*.*", recursive=True)]
    if word2vec_large_name in files:
        return True
    return False


def word2vec_small_exist():
    files = [os.path.basename(file) for file in glob.glob(word2vec_model_location + "**/*.*", recursive=True)]
    if word2vec_small_name in files:
        return True
    return False


def keras_model_exist():
    files = [os.path.basename(file) for file in glob.glob(keras_model_location + "**/*.*", recursive=True)]
    if keras_model_name in files:
        return True
    return False
