FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY code/requirements.txt /code/

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000