FROM python:3.14.3-slim
RUN groupadd -r groupdjango && useradd -r -g groupdjango userdj

ENV PYTHONDONTWRTITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip
WORKDIR /var/www/pageglow/
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

USER userdj