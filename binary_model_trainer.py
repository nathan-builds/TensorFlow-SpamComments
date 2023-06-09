import time
import pickle
import keras.api._v2.keras as keras
import tensorflow as tf
import xlrd

gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # only use GPU memory that we need, not allocate all the GPU memory
    tf.config.experimental.set_memory_growth(gpus[0], enable=True)

import tqdm
import numpy as np

from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint, TensorBoard
from sklearn.model_selection import train_test_split
from keras.layers import Embedding, LSTM, Dropout, Dense
from keras.models import Sequential
from keras.metrics import Recall, Precision

SEQUENCE_LENGTH = 100  # the length of all sequences (number of words per sample)
EMBEDDING_SIZE = 100  # Using 100-Dimensional GloVe embedding vectors
TEST_SIZE = 0.25  # ratio of testing set

BATCH_SIZE = 64
EPOCHS = 10  # number of epochs

label2int = {"ham": 0, "spam": 1}
int2label = {0: "ham", 1: "spam"}


def load_data():
    """
    Loads SMS Spam Collection dataset
    """
    texts, labels = [], []
    with open("data/SMSSpamCollection") as f:
        for line in f:
            split = line.split()
            labels.append(split[0].strip())
            texts.append(' '.join(split[1:]).strip())
    return texts, labels


def load_comments_data():
    texts, labels = [], []

    wb = xlrd.open_workbook('comments_data/full_set_final.xls')
    sheet = wb.sheet_by_index(0)
    for row_number in range(sheet.nrows):
        spam_flag = int(sheet.row(row_number)[0].value)
        comment_text = sheet.row(row_number)[1].value.strip()
        texts.append(comment_text)
        labels.append("ham" if spam_flag == 0 else "spam")

    return texts, labels


def get_embedding_vectors(tokenizer, dim=100):
    embedding_index = {}
    with open(f"data/glove.6B.{dim}d.txt", encoding='utf8') as f:
        for line in tqdm.tqdm(f, "Reading GloVe"):
            values = line.split()
            word = values[0]
            vectors = np.asarray(values[1:], dtype='float32')
            embedding_index[word] = vectors

    word_index = tokenizer.word_index
    embedding_matrix = np.zeros((len(word_index) + 1, dim))
    for word, i in word_index.items():
        embedding_vector = embedding_index.get(word)
        if embedding_vector is not None:
            # words not found will be 0s
            embedding_matrix[i] = embedding_vector

    return embedding_matrix


def get_model(tokenizer, lstm_units):
    """
    Constructs the model,
    Embedding vectors => LSTM => 2 output Fully-Connected neurons with softmax activation
    """
    # get the GloVe embedding vectors
    embedding_matrix = get_embedding_vectors(tokenizer)
    model = Sequential()
    model.add(Embedding(len(tokenizer.word_index) + 1,
                        EMBEDDING_SIZE,
                        weights=[embedding_matrix],
                        trainable=False,
                        input_length=SEQUENCE_LENGTH))

    model.add(LSTM(lstm_units, recurrent_dropout=0.2))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation="softmax"))
    # compile as rmsprop optimizer
    # aswell as with recall metric
    model.compile(optimizer="rmsprop", loss="categorical_crossentropy",
                  metrics=["accuracy", Precision(), Recall()])
    model.summary()
    return model


def save_model(model):
    model.save('model/comments_model.h5')


def get_predictions(text, tokenizer, model):
    sequence = tokenizer.texts_to_sequences([text])
    # pad the sequence
    sequence = pad_sequences(sequence, maxlen=SEQUENCE_LENGTH)
    # get the prediction
    prediction = model.predict(sequence)[0]
    # one-hot encoded vector, revert using np.argmax
    return int2label[np.argmax(prediction)]


def main():
    X, y = load_comments_data()

    # X, y = load_data()

    # Text tokenization
    # vectorizing text, turning each text into sequence of integers
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(X)
    # lets dump it to a file, so we can use it in testing
    pickle.dump(tokenizer, open("results/tokenizer.pickle", "wb"))
    # convert to sequence of integers
    X = tokenizer.texts_to_sequences(X)

    # convert to numpy arrays
    X = np.array(X)
    y = np.array(y)
    # pad sequences at the beginning of each sequence with 0's
    # for example if SEQUENCE_LENGTH=4:
    # [[5, 3, 2], [5, 1, 2, 3], [3, 4]]
    # will be transformed to:
    # [[0, 5, 3, 2], [5, 1, 2, 3], [0, 0, 3, 4]]
    X = pad_sequences(X, maxlen=SEQUENCE_LENGTH)

    y = [label2int[label] for label in y]
    y = to_categorical(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=7)
    # print our data shapes
    print("X_train.shape:", X_train.shape)
    print("X_test.shape:", X_test.shape)
    print("y_train.shape:", y_train.shape)
    print("y_test.shape:", y_test.shape)

    model = get_model(tokenizer=tokenizer, lstm_units=128)

    # initialize our ModelCheckpoint and TensorBoard callbacks
    # model checkpoint for saving best weights
    model_checkpoint = ModelCheckpoint("results/spam_classifier_{val_loss:.2f}.h5", save_best_only=True,
                                       verbose=1)
    # for better visualization
    tensorboard = TensorBoard(f"logs/spam_classifier_{time.time()}")
    # train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test),
              batch_size=BATCH_SIZE, epochs=EPOCHS,
              callbacks=[tensorboard, model_checkpoint],
              verbose=1)

    # get the loss and metrics
    result = model.evaluate(X_test, y_test)
    # extract those
    loss = result[0]
    accuracy = result[1]
    precision = result[2]
    recall = result[3]

    print(f"[+] Accuracy: {accuracy * 100:.2f}%")
    print(f"[+] Precision:   {precision * 100:.2f}%")
    print(f"[+] Recall:   {recall * 100:.2f}%")
    save_model(model)
    #
    # print(get_predictions('DONT Look at my story', tokenizer, model))
    # print(get_predictions('Awesome Picture!', tokenizer, model))
    # print(get_predictions('IM Paying the first 5000 people who message me', tokenizer, model))
    # print(get_predictions('thank GOD for BTC traders who helped me make $25000', tokenizer, model))
    # print(get_predictions('Looking good!', tokenizer, model))

    while True:
        comment = input('Enter Comment:')
        print(get_predictions(comment, tokenizer, model))


# text = "You won a prize of 1,000$, click here to claim!"
# print(get_predictions(text))
# save_model(model)

if __name__ == '__main__':
    main()
