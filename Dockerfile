FROM python:3.8-slim

LABEL maintainer="qortmddbs731@korea.ac.kr"

COPY . /app
WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

ENV DASH_DEBUG False
EXPOSE 8050

CMD ["python", "app.py"]