# Базовый образ Python 3.12
FROM python:3.12-slim

LABEL maintainer="VadimSolodyuk <vadim.l.solodyuk@gmail.com>"

# Аргументы для создания пользователя (нужно для маппинга UID)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Создание пользователя vscode, установка системных зависимостей (для GUI - Tkinter) и sudo
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    git \
    python3-tk \
    tk-dev \
    sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && rm -rf /var/lib/apt/lists/*

# Обновление pip
RUN pip install --upgrade pip

WORKDIR /workspace

COPY pyproject.toml ./

# Создаем минимальную структуру пакета (подставь имя своего пакета)
RUN mkdir -p src/alphameterqc && touch src/alphameterqc/__init__.py

RUN pip install --no-cache-dir -e .[dev] \
    # Отдаем права на рабочую директорию пользователю vscode
    && chown -R $USERNAME:$USERNAME /workspace

# Отключение буферизации вывода (критично для subprocess)
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Переключаемся на непривилегированного пользователя
USER $USERNAME

CMD ["bash"]