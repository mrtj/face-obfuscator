FROM python:3.6-slim-stretch

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libatlas-base-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-numpy \
    software-properties-common \
    zip \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN mkdir -p /opt
 
RUN cd /opt && \
    mkdir -p dlib && \
    git clone -b 'v19.9' --single-branch https://github.com/davisking/dlib.git dlib/ && \
    cd dlib/ && \
    python3 setup.py install --yes USE_AVX_INSTRUCTIONS

RUN pip3 install opencv-python==4.5.*

RUN cd /opt && \
    git clone https://github.com/ageitgey/face_recognition.git

RUN cd /opt/face_recognition && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

COPY . /opt/face_obfuscator

CMD cd /opt/face_obfuscator && \
    python3 face_obfuscator.py
