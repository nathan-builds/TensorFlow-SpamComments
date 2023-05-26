from instagrapi import Client
import tensorflow as tf
import binary_model_trainer as binary_model
from keras.preprocessing.text import Tokenizer
import re


class SpamBot:

    def __int__(self):
        self._model = tf.keras.models.load_model('model/comments_model.h5')
        x, y = binary_model.load_comments_data()
        self._tokenizer = Tokenizer()
        self._tokenizer.fit_on_texts(x)
        self._SPAM = "spam"

    def scan_insta(self):
        cl = Client()
        cl.delay_range = [10, 30]
        cl.load_settings("session.json")
        cl.login("testpython12345", "psalm100")
        # cl.dump_settings("session.json")

        user_id = cl.user_id_from_username("testpython12345")

        spamList = {}

        while True:
            medias = cl.user_medias(user_id, 20)

            for m in medias:
                comments = cl.media_comments(m.id, 0)
                for c in comments:
                    stripped_text = re.sub(r'[^\x00-\x7F]+', ' ', c.text)
                    stripped_text = stripped_text.strip()
                    if self.is_spam(stripped_text):
                        spamList[m.id] = stripped_text
                        cl.comment_bulk_delete(m.id, [int(c.pk)])

    def is_spam(self, comment):
        pred = binary_model.get_predictions(comment, self._tokenizer, self._model)
        if pred == self._SPAM:
            return True
        else:
            return False
