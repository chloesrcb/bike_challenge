import numpy as np
import tensorflow as tf # for neural network
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

def training(x_train):
    x_train.dropna(inplace=True)
    x_train["meteo"] = x_train["meteo"].astype(int)
    x_train["vent"] = x_train["vent"].astype(int)
    x_train["pluie"] = x_train["pluie"].astype(float)
    train_dataset = x_train.sample(frac=0.8, random_state=0).copy()
    train_label = train_dataset.pop("Total jour")

    test_dataset = x_train.drop(train_dataset.index)
    test_label = test_dataset.pop("Total jour")
    #Normalize data
    normalizer = preprocessing.Normalization()
    normalizer.adapt(np.array(train_dataset))
    print(normalizer.mean.numpy())
    print('Normalized:', normalizer(train_dataset).numpy())

    # set seed
    tf.random.set_seed(0)


    model = keras.Sequential([
      normalizer,
      layers.Dense(9, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(64, activation='relu'),
      layers.Dense(1)
    ])

    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.1),
        loss='mean_absolute_error'
    )

    for i in range(2):
        model.fit(
            train_dataset, train_label,
            epochs=100,
            # Calculate validation results on 20% of the training data
            validation_split = 0.2
        )

    y_pred = model.predict(test_dataset)
    x = tf.linspace(0, test_label.shape[0]-1, test_label.shape[0])
    return (y_pred, x, test_label, model, test_dataset)

   


