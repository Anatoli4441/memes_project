FROM jenkins/jenkins:lts

USER root
RUN apt-get update && apt-get install -y docker.io git python3 python3-pip

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt

USER jenkins
