from instagrapi import Client
import tensorflow as tf
import binary_model_trainer as binary_model
from keras.preprocessing.text import Tokenizer
import re

SPAM = "spam"

cl = Client()
cl.delay_range = [10, 30]
cl.load_settings("session.json")
cl.login("testpython12345", "psalm100")
# cl.dump_settings("session.json")

user_id = cl.user_id_from_username("testpython12345")

model = tf.keras.models.load_model('model/comments_model.h5')

X, y = binary_model.load_comments_data()
tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

spamList = {}

while True:
    medias = cl.user_medias(user_id, 20)

    for m in medias:
        comments = cl.media_comments(m.id, 0)
        for c in comments:
            stripped_text = re.sub(r'[^\x00-\x7F]+', ' ', c.text)
            stripped_text = stripped_text.strip()
            pred = binary_model.get_predictions(stripped_text, tokenizer, model)
            if pred == SPAM:
                spamList[m.id] = stripped_text
                cl.comment_bulk_delete(m.id, [int(c.pk)])
