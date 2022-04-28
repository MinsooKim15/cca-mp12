# syntax=docker/dockerfile:1
# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
WORKDIR /mp12

COPY requirements.txt requirements.txt
# RUN pip --no-cache-dir install torch torchvision
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
ARG DATASET=mnist
ARG TYPE=ff

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python3", "/mp12/classify.py"]
