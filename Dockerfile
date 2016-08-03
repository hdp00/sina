FROM yuxio/flask-python351
COPY ./config/localtime /etc/localtime
CMD python3 /usr/src/app/code/run.py


