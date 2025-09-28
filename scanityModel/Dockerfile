FROM python:3.13
LABEL authors="gneg"

COPY . .

RUN pip3 install --upgrade pip -r requirements.txt

ENTRYPOINT ["python3", "main.py"]