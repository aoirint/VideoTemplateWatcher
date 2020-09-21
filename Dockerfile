FROM aoirint/ffmpeg-python

WORKDIR /work

RUN apt update -qq && apt upgrade -y \
  && apt install -y \
    libsm6 \
    libxext6 \
    libxrender-dev \
    fonts-ipafont \
  && fc-cache -f -v

ADD requirements.txt /code/
RUN pip3 install -r /code/requirements.txt

ADD VideoTemplateWatcher/ /code

ENTRYPOINT [ "python3", "/code/VideoTemplateWatcher.py" ]
CMD [ "--help" ]
