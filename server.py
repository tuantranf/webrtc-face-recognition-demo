import face_recognize_api
import os
import numpy
import cv2
from PIL import Image
from flask import Flask, request, Response

app = Flask(__name__)

# for CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST') # Put any other methods you need here
    return response


@app.route('/')
def index():
    return Response('Tensor Flow object detection')

@app.route('/train')
def train():
    try:
        print('Started Training')
        face_recognize_api.train('./data/face-images')
        print('finished Training')
        return Response('Training finished.')
    except Exception as e:
        print('POST /image error: %e' % e)
        return e

@app.route('/local')
def local():
    return Response(open('./static/local.html').read(), mimetype="text/html")


@app.route('/video')
def remote():
    return Response(open('./static/video.html').read(), mimetype="text/html")


# @app.route('/test')
# def test():
#     PATH_TO_TEST_IMAGES_DIR = 'object_detection/test_images'  # cwh
#     TEST_IMAGE_PATHS = [os.path.join(PATH_TO_TEST_IMAGES_DIR, 'image{}.jpg'.format(i)) for i in range(1, 3)]

#     image = Image.open(TEST_IMAGE_PATHS[0])
#     objects = object_detection_api.get_objects(image)

#     return objects


@app.route('/image', methods=['POST'])
def image():
    try:
        image_file = request.files['image']  # get the image

        # Set an image confidence threshold value to limit returned data
        threshold = request.form.get('threshold')
        if threshold is None:
            threshold = 0.5
        else:
            threshold = float(threshold)

        uploadWidth = request.form.get('uploadWidth')
        if uploadWidth is None:
            uploadWidth = 800.0
        else:
            uploadWidth = float(uploadWidth)

        uploadHeight = request.form.get('uploadHeight')
        if uploadHeight is None:
            uploadHeight = 600.0
        else:
            uploadHeight = float(uploadHeight)
        # finally run the image through tensor flow object detection`
        # image_object = cv2.imread('face-images/mike/tuan.jpg')
        image_object = cv2.imdecode(numpy.fromstring(image_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
        response = face_recognize_api.predict(image_object, threshold, uploadWidth, uploadHeight)

        print(response)
        return response

    except Exception as e:
        print('POST /image error: %e' % e)
        return e


if __name__ == '__main__':
	# without SSL
    app.run(debug=True, host='0.0.0.0', threaded=True)

	# with SSL
    #app.run(debug=True, host='0.0.0.0', ssl_context=('ssl/server.crt', 'ssl/server.key'))
