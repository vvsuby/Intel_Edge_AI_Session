import dlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np

detector = dlib.get_frontal_face_detector()
shape = dlib.shape_predictor('./models/shape_predictor_68_face_landmarks.dat')

# img = dlib.load_rgb_image('./imgs/04.jpg')
# plt.figure(figsize=(16, 10))
# plt.imshow(img)
# plt.show()

# img_result = img.copy()
# dets = detector(img, 1)

# if len(dets):
#     fig, ax = plt.subplots(1, figsize=(10, 16))
#     for det in dets:
#         x, y, w, h = det.left(), det.top(), det.width(), det.height()
#         rect = patches.Rectangle((x, y), w, h,
#                                  linewidth=2, edgecolor='r', facecolor='None')
#         ax.add_patch(rect)
#     ax.imshow(img_result)
#     plt.show()
# else :
#     print('Not find faces')
#
# fig, ax = plt.subplots(1, figsize=(16, 10))
# obj = dlib.full_object_detections()
#
# for detection in dets:
#     s = shape(img, detection)
#     obj.append(s)
#
#     for point in s.parts():
#         circle = patches.Circle((point.x, point.y), radius=3,
#                                 edgecolor='b', facecolor='b')
#         ax.add_patch(circle)
#     ax.imshow(img_result)
# plt.show()

def align_faces(img):
    dets = detector(img)
    objs = dlib.full_object_detections()
    for detection in dets:
        s = shape(img, detection)
        objs.append(s)

    faces = dlib.get_face_chips(img, objs, size=256, padding=0.5)
    return faces

# test_img = dlib.load_rgb_image('./imgs/11.jpg')
# test_faces = align_faces(test_img)
# fig, axes = plt.subplots(1, len(test_faces)+1, figsize=(10, 8))
# axes[0].imshow(test_img)
# for i, face in enumerate(test_faces):
#     axes[i+1].imshow(face)
# plt.show()

sess = tf.Session()
init_op = tf.group(tf.global_variables_initializer(),
                   tf.local_variables_initializer())
sess.run(init_op)

saver = tf.train.import_meta_graph('./models/model.meta')
saver.restore(sess, tf.train.latest_checkpoint('./models'))
graph = tf.get_default_graph()
X = graph.get_tensor_by_name('X:0')
Y = graph.get_tensor_by_name('Y:0')
Xs = graph.get_tensor_by_name('generator/xs:0')

def preprocess(img):
    return img / 127.5 - 1
def deprecess(img):
    return (img + 1) / 2

img1 = dlib.load_rgb_image('./imgs/14.jpg')
img1_faces = align_faces(img1)

img2 = dlib.load_rgb_image('./imgs/01.jpg')
img2_faces = align_faces(img2)

fig, axes = plt.subplots(1, 2, figsize=(8, 5))
axes[0].imshow(img1_faces[0])
axes[1].imshow(img2_faces[0])
plt.show()

src_img = img1_faces[0]
ref_img = img2_faces[0]

X_img = preprocess(src_img)
X_img = np.expand_dims(X_img, axis=0)

Y_img = preprocess(ref_img)
Y_img = np.expand_dims(Y_img, axis=0)

output = sess.run(Xs, feed_dict={X:X_img, Y:Y_img})
output_img = deprecess(output[0])

fig, axes = plt.subplots(1, 3, figsize=(8, 5))
axes[0].imshow(img1_faces[0])
axes[1].imshow(img2_faces[0])
axes[2].imshow(output_img)
plt.show()











































