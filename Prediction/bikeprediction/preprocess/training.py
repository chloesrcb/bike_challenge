import numpy as np
import tensorflow as tf # for neural network
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

def training(x_train):
    """
        Create a prevision model by training it
        Entry : x_train = dataframe to train the model
        Return : y_pred = list of prediction on test database
                 test_label = list of expected values of the test database 
                 model = trained model
                 test_dataset = test dataframe
    """
    x_train.dropna(inplace=True)
    x_train["meteo"] = x_train["meteo"].astype(int)
    x_train["vent"] = x_train["vent"].astype(int)
    x_train["pluie"] = x_train["pluie"].astype(float)
    train_dataset = x_train.sample(frac=0.8, random_state=0).copy()
    train_label = train_dataset.pop("Total jour")

    test_dataset = x_train.drop(train_dataset.index)
    test_label = test_dataset.pop("Total jour")
    
    # Normalize data to have the same scale
    normalizer = preprocessing.Normalization()
    normalizer.adapt(np.array(train_dataset))
    print(normalizer.mean.numpy())
    print('Normalized:', normalizer(train_dataset).numpy())

    # set seed
    tf.random.set_seed(0)


    model = keras.Sequential([
      normalizer,
      layers.Dense(15, activation='relu'),
      layers.Dense(128, activation='relu'),
      layers.Dense(128, activation='relu'),
      layers.Dense(1)
    ])

    model.compile(
        optimizer=tf.optimizers.Adam(learning_rate=0.1),
        loss='mean_absolute_error'
    )

    for i in range(1):
        model.fit(
            train_dataset, train_label,
            epochs=100,
            # Calculate validation results on 20% of the training data
            validation_split = 0.2
        )

    y_pred = model.predict(test_dataset)
    return (y_pred, test_label, model, test_dataset)

   


