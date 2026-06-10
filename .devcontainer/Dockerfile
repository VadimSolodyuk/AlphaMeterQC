# Базовый образ Python 3.10
FROM python:3.10-slim

LABEL maintainer="VadimSolodyuk <vadim.l.solodyuk@gmail.com>"

# Обновление pip
RUN pip install --upgrade pip

# Системные зависимости для GUI (Tkinter)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    python3-tk \
    tk-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY . .
# VOLUME /workspace

RUN pip install --no-cache-dir -e .[dev]


# Отключение буферизации вывода (критично для subprocess)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["bash"]