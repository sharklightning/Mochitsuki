FROM python:3.11-alpine

WORKDIR /app

RUN python3 -m pip install --upgrade pip

COPY ./requirements.txt /app
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p src/cards && mkdir -p src/resp && mkdir -p src/temp

COPY . /app

CMD ["python", "src/_main.py"]
