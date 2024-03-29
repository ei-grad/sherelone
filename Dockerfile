FROM python:slim
WORKDIR /usr/src/app
ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ADD . .
CMD gunicorn -b 0.0.0.0:8000 app:app
