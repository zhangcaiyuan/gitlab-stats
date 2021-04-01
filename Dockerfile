FROM python:3.8-alpine

WORKDIR /server

COPY . .

RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

ENV PYTHONPATH=/server

ENTRYPOINT ["python3", "app.py"]