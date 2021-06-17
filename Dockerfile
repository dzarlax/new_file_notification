FROM python:3.8

ADD main.py requirements.txt /
VOLUME /working_dir

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg

RUN pip install -r /requirements.txt

ENTRYPOINT ["/usr/bin/env"]
CMD ["python3", "/main.py"]