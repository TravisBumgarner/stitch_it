# 1 
FROM python:3.7

# 2
COPY ./requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# 3
COPY /server /server
WORKDIR /server

# 4
ENV PORT 8080

# 5
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app