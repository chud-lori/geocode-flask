FROM python:3.8

ADD . /geocode-flask
WORKDIR /geocode-flask
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["setup.py"]

EXPOSE 5000