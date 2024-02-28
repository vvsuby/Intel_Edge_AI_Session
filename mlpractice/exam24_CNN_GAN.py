import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

OUT_DIR = './CNN_out'
img_shape = (28, 28, 1)
epochs = 100000
batch_size = 128
noise = 100
sample_interval = 100

MY_NUMBER = 9

(x_train, y_train), (_, _) = mnist.load_data()
x_train = x_train[y_train == MY_NUMBER]
print(x_train.shape)


x_train = x_train / 127.5 - 1
x_train = np.expand_dims(x_train, axis=3)
print(x_train.shape)

generator = Sequential()
generator.add(Dense(256*7*7, input_dim=noise))
generator.add(Reshape((7, 7, 256)))
generator.add(Conv2DTranspose(128, kernel_size=3, strides=2, padding='same'))
generator.add(BatchNormalization())
generator.add(LeakyReLU(alpha=0.01))
generator.add(Conv2DTranspose(64, kernel_size=3, strides=1, padding='same'))
generator.add(BatchNormalization())
generator.add(LeakyReLU(alpha=0.01))
generator.add(Conv2DTranspose(1, kernel_size=3, strides=2, padding='same'))
generator.add(Activation('tanh'))
generator.summary()


lrelu = LeakyReLU(alpha=0.01)
discriminator = Sequential()
discriminator.add(Conv2D(32, kernel_size=3, strides=2, padding='same', input_shape=img_shape))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Conv2D(64, kernel_size=3, strides=2, padding='same'))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Conv2D(128, kernel_size=3, strides=2, padding='same'))
discriminator.add(LeakyReLU(alpha=0.01))
discriminator.add(Flatten())
discriminator.add(Dense(1, activation='sigmoid'))
discriminator.summary()

discriminator.compile(loss='binary_crossentropy', optimizer='adam',
                      metrics=['accuracy'])
discriminator.trainable = False

gan_model = Sequential()
gan_model.add(generator)
gan_model.add(discriminator)
gan_model.summary()

gan_model.compile(loss='binary_crossentropy', optimizer='adam')


real = np.ones((batch_size, 1))
fake = np.zeros((batch_size, 1))

# print(real)
# print(fake)

for epoch in range(epochs):
    idx = np.random.randint(0, x_train.shape[0], batch_size)
    real_img = x_train[idx]

    z = np.random.normal(0, 1, (batch_size, noise))
    fake_img = generator.predict(z)

    d_hist_real = discriminator.train_on_batch(real_img, real)
    d_hist_fake = discriminator.train_on_batch(fake_img, fake)

    d_loss, d_acc = 0.5 * np.add(d_hist_real, d_hist_fake)


    z = np.random.normal(0, 1, (batch_size, noise))
    gan_hist = gan_model.train_on_batch(z, real)

    if epoch % sample_interval == 0:
        print('%d [D loss: %f, acc: %.2f%%] [G loss:%f]'%(
            epoch, d_loss, d_acc*100, gan_hist))
        row = col = 4
        z = np.random.normal(0, 1, (row * col, noise))
        fake_imgs = generator.predict(z)
        fake_imgs = 0.5 * fake_imgs
        _, axs = plt.subplots(row, col, figsize=(row, col), sharey=True, sharex=True)
        count = 0
        for i in range(row):
            for j in range(col):
                axs[i, j].imshow(fake_imgs[count, :, :, 0], cmap='gray')
                axs[i, j].axis('off')
                count += 1
        path = os.path.join(OUT_DIR, 'img-{}'.format(epoch+1))
        plt.savefig(path)
        plt.close()
        generator.save('./models/generator_9_JKY.h5')



















