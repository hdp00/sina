FROM yuxio/flask-python351
COPY ./config/localtime /etc/localtime
EXPOSE 5050
CMD python3 /usr/src/app/code/test.py


