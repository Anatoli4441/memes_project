FROM jenkins/jenkins:lts

USER root

RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean


RUN /usr/local/bin/install-plugins.sh git workflow-aggregator docker-workflow

USER jenkins

# Копируем файл настроек в контейнер (опционально, если хотите настроить Jenkins)
 COPY jenkins_config.xml /var/jenkins_home/config.xml
