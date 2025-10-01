FROM python:3.13
LABEL authors="gneg"

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip3 install --upgrade pip -r requirements.txt

ENTRYPOINT ["python3", "src/main.py"]