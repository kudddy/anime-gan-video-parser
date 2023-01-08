FROM python:3.8

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update \
    && apt-get install -y -qq git python-dev libxml2-dev libxslt1-dev antiword \
                              unrtf poppler-utils tesseract-ocr flac libx264-dev \
                              ffmpeg lame libmad0 libsox-fmt-mp3 sox libjpeg-dev swig \
                              pkg-config libpoppler-private-dev libpoppler-cpp-dev\
    && apt-get clean


COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN pip3 install dlib~=19.21.1
COPY . /app

CMD python3 main.py