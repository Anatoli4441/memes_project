# Базовый образ Jenkins LTS
FROM jenkins/jenkins:lts

# Установка необходимых плагинов Jenkins
RUN jenkins-plugin-cli --plugins \
    pipeline \
    blueocean \
    git

# Установка Docker внутри Jenkins контейнера
USER root
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - && \
    add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable" && \
    apt-get update && \
    apt-get install -y docker-ce docker-ce-cli containerd.io

# Добавляем Jenkins пользователя в Docker группу
RUN usermod -aG docker jenkins

# Установка Python и зависимостей проекта
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --upgrade pip

# Копирование файлов проекта в контейнер Jenkins
COPY . /var/jenkins_home/workspace/memes_project/

# Установка зависимостей Python
RUN pip3 install -r /var/jenkins_home/workspace/memes_project/requirements.txt

# Переключение обратно на пользователя Jenkins
USER jenkins
