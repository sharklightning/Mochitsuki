FROM python:latest

WORKDIR /app

RUN mkdir -p src/cards && mkdir -p src/resp && mkdir -p src/temp
RUN pip3 install flask
RUN pip3 install python-dotenv
RUN pip3 install openai
RUN pip3 install httpx

COPY . /app

CMD ["python", "src/main.py"]
