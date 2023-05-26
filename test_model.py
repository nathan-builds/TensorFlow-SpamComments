import tensorflow as tf
import binary_model_trainer as binary_model
from keras.preprocessing.text import Tokenizer


model = tf.keras.models.load_model('model/comments_model.h5')

X, y = binary_model.load_comments_data()
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

print(model.summary())

while True:
    comment = input('Enter Comment:')
    print(binary_model.get_predictions(comment, tokenizer, model))
