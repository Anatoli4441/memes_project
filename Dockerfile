FROM python

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    git \
    && apt-get clean


COPY . /app
WORKDIR /app


RUN pip install --no-cache-dir -r requirements.txt

CMD ["pytest"]
