# coding: utf-8
import numpy as np
import cv2
import json
from os import listdir
from os.path import isfile, join
from skimage.feature import hog
import joblib
from sklearn.svm import LinearSVC
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn import metrics
import face_recognition

MODEL_PATH = './data/models/model.pkl'

def rgb2gray(rgb):
    # funtion to convert an rgb image to gray image
    #     Y' = 0.299 R + 0.587 G + 0.114 B
    return rgb[:, :, 0] * .299 + rgb[:, :, 1] * .587 + rgb[:, :, 2] * .114

def load_data(data_path):
    data, target = [], []
    data_path = data_path
    only_dirs = [f for f in listdir(data_path)]
    for dir in only_dirs:
        if dir[:1] == '.':
            continue
        label = dir
        dir = data_path + '/' + dir
        only_files = [f for f in listdir(dir) if isfile(join(dir, f))]
        for file in only_files:
            if file[:1] == '.':
                continue
            image_path = dir + '/' + file
            image = cv2.imread(image_path)

            face_locations = face_recognition.face_locations(image)

            for (top, right, bottom, left) in face_locations:
                rgb_face = image[top:bottom, left:right]
                rgb_face = cv2.resize(rgb_face, (200, 200))
                rgb_face = rgb2gray(rgb_face)
                hog_vector = hog(rgb_face, orientations=8, pixels_per_cell=(10, 10), cells_per_block=(4, 4), block_norm='L2')
                data.append(np.array(hog_vector))
                target.append(label)

    return np.asarray(data), np.asarray(target)

def train(data_path):
    #train model
    data,target = load_data(data_path)
    print(data.shape)
    print(target.shape)
    X_train, X_test, y_train, y_test = train_test_split(data, target, test_size=0.2, random_state=0)

    svm = LinearSVC()
    clf = CalibratedClassifierCV(svm)

    clf.fit(X_train, y_train)
    print ("Accuracy on training set:")
    print (clf.score(X_train, y_train))
    print ("Accuracy on testing set:")
    print (clf.score(X_test, y_test))

    y_pred = clf.predict(X_test)
    print ("Classification Report:")
    print (metrics.classification_report(y_test, y_pred))

    joblib.dump(clf, MODEL_PATH)
    
def predict(test_image, threshold, uploadWidth, uploadHeight):
    model = joblib.load(MODEL_PATH)

    i = 0
    face_locations = face_recognition.face_locations(test_image)

    output = []

    item = Object()
    item.version = "0.0.1"
    item.numObjects = len(face_locations)
    item.threshold = threshold
    output.append(item)

    for (top, right, bottom, left) in face_locations:
        rgb_face = test_image[top:bottom, left:right]
        rgb_face = cv2.resize(rgb_face, (200, 200))
        rgb_face = rgb2gray(rgb_face)
        hog_vector = hog(rgb_face, orientations=8, pixels_per_cell=(10, 10), cells_per_block=(4, 4), block_norm='L2')
        probabilities = model.predict_proba(np.asarray([hog_vector]))[0]
        index = np.argmax(probabilities)
        label = model.classes_[index]
        proba = round(probabilities[index], 2)
        color = (0, 255, 255)

        if proba < threshold:
            label = '  Unknown'
            color = (0, 0, 255)

        print("{} - {} - {} {} {} {}".format(label, proba, top, right, bottom, left))

        # Add some metadata to the output
        item = Object()
        item.class_name = "{}".format(label)
        item.name = label
        item.score = proba
        # item.x = float(1 - left/uploadWidth)
        # item.y = float(1 - top/uploadHeight)
        # item.height = float((bottom-top)/uploadHeight)
        # item.width = float((right-left)/uploadWidth)
        item.x = left
        item.y = top
        item.height = bottom-top
        item.width = right-left

        output.append(item)
    
    outputJson = json.dumps([ob.__dict__ for ob in output])
    return outputJson

# added to put object in JSON
class Object(object):
    def __init__(self):
        self.name="Face recognition demo using TensorFlow REST API"

    def toJSON(self):
        return json.dumps(self.__dict__)


