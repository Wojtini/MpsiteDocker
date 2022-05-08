FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY code/requirements.txt /app/

RUN pip install --upgrade pip setuptools
RUN pip install -r requirements.txt
COPY . /app/
EXPOSE 8000
EXPOSE 5432
