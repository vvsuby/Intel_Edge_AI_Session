from PIL import Image #pip install pillow
import glob
import  numpy as np
from sklearn.model_selection import train_test_split

img_dir = '../datasets/cat_dog/train/'
categories = ['cat', 'dog']
image_w = 64
image_h = 64

pixel = image_h * image_w * 3
X = []
Y = []
files = None

for idx, category in enumerate(categories):
    files = glob.glob(img_dir + category + '*.jpg')
    for i, f in enumerate(files):
        try:
            img = Image.open(f)
            img = img.convert('RGB')
            img = img.resize((image_w, image_h))
            data = np.asarray(img)
            X.append(data)
            Y.append(idx)
            if i % 300 == 0:
                print(category, ':', f)
        except:
            print('error :', category, f)
X = np.array(X)
Y = np.array(Y)
X = X / 255
print(X[0])
print(Y[0])
print(X.shape)
print(Y.shape)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1)
xy = (X_train, X_test, Y_train, Y_test)
np.save('../datasets/binary_image_data.npy', xy, dtype=object)










