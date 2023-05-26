import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_datasets as tfds

test_comment = "Incredibly fascinating story with very realistic acting. Different from the movies, now we see. I " \
               "mean, every " \
               "good movie, now opening, has their own special thing, but movies from this period, and movies from " \
               "Tom Hanks is very touching. " \
               "Also the parts Jonah and the parts that were about the movie (An affair to remember) made me laugh a " \
               "lot In short: love this movie a lot. "


def test():
    model = tf.keras.models.load_model("OldModel/imdb_mlp_model.h5");
    prediction = model.predict(['Hello world', 'This is a test'])
    print(prediction)
    print('success')


def test_data_builder():
    data = tfds.load('test_set')
    print('j')


def please_work():
    train_data, validation_data, test_data = tfds.load(
        name="imdb_reviews",
        split=('train[:60%]', 'train[60%:]', 'test'),
        as_supervised=True)

    embedding = "https://tfhub.dev/google/nnlm-en-dim50/2"
    hub_layer = hub.KerasLayer(embedding, input_shape=[],
                               dtype=tf.string, trainable=True)

    model = tf.keras.Sequential()
    model.add(hub_layer)
    model.add(tf.keras.layers.Dense(16, activation='relu'))
    model.add(tf.keras.layers.Dense(1))

    model.summary()

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.BinaryCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    history = model.fit(train_data.shuffle(10000).batch(512),
                        epochs=10,
                        validation_data=validation_data.batch(512),
                        verbose=1)
    results = model.evaluate(test_data.batch(512), verbose=2)

    for name, value in zip(model.metrics_names, results):
        print("%s: %.3f" % (name, value))
    examples = [
        "The movie was great!",
        "The movie was okay.",
        "The movie was terrible..."
    ]
    vals = model.predict(examples)
    print(vals)


please_work()
