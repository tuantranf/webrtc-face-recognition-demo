# Tensorflow People Recognition API Web Service

This is an example of how to turn the Face Recognition and into a web service. 

- [LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html) for Image Recognition
- [face-recognition](https://github.com/ageitgey/face_recognition) for face detection
- A Python Flask web server
- WebRTC for real time webcam

## Quick start with Docker
```bash
git clone [this-repository] webrtc-face-recognition
cd webrtc-face-recognition
docker build -t webrtc-face-regconition:latest .
docker run --rm -it -p 5000:5000 webrtc-face-regconition
```

## Develop with Docker
```bash
git clone [this-repository] webrtc-face-recognition
cd webrtc-face-recognition
docker build -t webrtc-face-regconition:latest .
# mount current code to container
docker run --rm -it -p 5000:5000 -v $(pwd):/code webrtc-face-regconition
```

## Example web apps
Point your browser to:
-  `https://localhost:5000/local` - shows a mirrored video from a webcam
- `https://localhost:5000/video` - shows object detection running on a HTML `<video>` tag

