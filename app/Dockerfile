FROM python:3.12.4-bookworm

# set working directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt update -y \
    && apt install -y postgresql netcat-traditional
#postgresql-dev g++ python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY ./manage.py .
COPY ./server ./server
COPY ./plates ./plates

# create dir for static files
#RUN mkdir /usr/src/app/staticfiles

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
