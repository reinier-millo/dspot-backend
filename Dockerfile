###########
# BUILDER #
###########

# pull official base image
FROM python:3.11 as builder

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APP_SRC_DIRNAME=dspot-backend

# set work directory
WORKDIR /$APP_SRC_DIRNAME

# lint
RUN pip install --upgrade pip

COPY . .

# install psycopg2 dependencies
RUN apt-get update
RUN apt upgrade -y
RUN apt-get install nano python3-dev libpq-dev -y

# install dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /$APP_SRC_DIRNAME/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.11

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system app --ingroup app

# create the appropriate directories
ENV APP_SRC_DIRNAME=dspot-backend
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
ENV PYTHONPATH=$APP_HOME

# install psycopg2 dependencies
RUN apt-get update
RUN apt upgrade -y
RUN apt-get install nano python3-dev libpq-dev -y

# install dependencies
RUN pip install --upgrade pip
COPY --from=builder /$APP_SRC_DIRNAME/wheels /wheels
COPY --from=builder /$APP_SRC_DIRNAME/requirements.txt .
RUN pip install --no-cache /wheels/*


# chown all the files to the app user
COPY --chown=app:app . $APP_HOME
RUN chown app:app -R $APP_HOME
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

EXPOSE 8000
CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
