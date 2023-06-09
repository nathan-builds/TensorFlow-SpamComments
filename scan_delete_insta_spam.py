from instagrapi import Client
import tensorflow as tf
import binary_model_trainer as binary_model
from keras.preprocessing.text import Tokenizer
import re


class SpamBot:

    def __init__(self, insta_scanner=False):
        self.comment_dict = {}
        self.model = tf.keras.models.load_model('model/comments_model.h5')
        x, y = binary_model.load_comments_data()
        self.tokenizer = Tokenizer()
        self.tokenizer.fit_on_texts(x)
        self.SPAM = "spam"
        if insta_scanner:
            self.cl = Client()
            self.cl.delay_range = [1, 3]
            #self.cl.load_settings("session.json")
            self.cl.login("spottythedestroyer", "Genesis11")
            #self.cl.dump_settings("session.json")
            self.user_id = self.cl.user_id_from_username("spottythedestroyer")

    def scan_insta(self):
        print('SCANNING MEDIA')
        spamList = []
        notSpamList = []

        medias = self.cl.user_medias(self.user_id, 20)

        for m in medias:
            comments = self.cl.media_comments(m.id, 0)
            for c in comments:
                ## we already know about this comment
                if c.pk in self.comment_dict:
                    continue
                stripped_text = re.sub(r'[^\x00-\x7F]+', ' ', c.text)
                stripped_text = stripped_text.strip()
                if self.is_spam(stripped_text):
                    spamList.append(stripped_text)
                    self.cl.comment_bulk_delete(m.id, [int(c.pk)])
                else:
                    notSpamList.append(stripped_text)
                # just store in comment dic so we know now to add it next time
                self.comment_dict[c.pk] = 1

        commentDict = {"deleted": spamList, "not_deleted": notSpamList}
        return commentDict

    def is_spam(self, comment):
        pred = binary_model.get_predictions(comment, self.tokenizer, self.model)
        if pred == self.SPAM:
            return True
        else:
            return False
