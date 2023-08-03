# pull official base image
FROM python:3.11.4-slim-buster

# set work directory
WORKDIR /usr/src/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/entrypoint.sh
RUN chmod +x /usr/src/entrypoint.sh

RUN apt-get update && apt-get install -y netcat

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]