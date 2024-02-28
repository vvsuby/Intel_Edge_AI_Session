import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from tensorflow.keras.datasets import mnist

autoencoder = load_model('./models/autoencoder.h5')

(x_train, _), (x_test, _) = mnist.load_data()

x_train = x_train / 255
x_test = x_test / 255

conv_x_train = x_train.reshape(-1, 28, 28, 1)
conv_x_test = x_test.reshape(-1, 28, 28, 1)
print(conv_x_train.shape, conv_x_test.shape)

noise_factor = 0.5
conv_x_test_noisy = conv_x_test + np.random.normal(
    loc=0.0, scale=1.0, size=conv_x_test.shape) * noise_factor
conv_x_test_noisy = np.clip(conv_x_test_noisy, 0.0, 1.0)

decoded_img = autoencoder.predict(conv_x_test_noisy[:10])

n = 10
plt.gray()
for i in range(n):
    ax = plt.subplot(3, 10, i + 1)
    plt.imshow(x_test[i])
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax = plt.subplot(3, 10, i + 1 + n)
    plt.imshow(conv_x_test_noisy[i].reshape(28, 28))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)

    ax = plt.subplot(3, 10, i + 1 + 2*n)
    plt.imshow(decoded_img[i].reshape(28, 28))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
plt.show()





























