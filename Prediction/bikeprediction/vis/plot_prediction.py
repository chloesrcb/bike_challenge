import matplotlib.pyplot as plt


def plot_prediction(x, y, reference):
    """
        plot a graphic with the prediction and the real data
        Entry : x =
                y =
                reference =
    """
    plt.scatter(x, reference, label='Real data')
    plt.plot(x, y, color='k', label='Predictions')
    plt.xlabel('Test')
    plt.title('Prediction with neural networks')
    plt.ylabel('Number of bikes')
    plt.legend()