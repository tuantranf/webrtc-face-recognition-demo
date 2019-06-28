FROM tensorflow/tensorflow

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \ 
    cmake \
    gfortran \
    git \
    wget \
    curl \
    pkg-config \
    python-dev \ 
    libopencv-dev \ 
    ffmpeg \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    python-pycurl \ 
    python-numpy \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN cd ~ && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd  dlib/ && \
    python setup.py install --yes USE_AVX_INSTRUCTIONS

ADD ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt 

ADD . /code

WORKDIR /code

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD ["server.py"]

