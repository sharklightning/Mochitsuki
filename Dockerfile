FROM python:latest

WORKDIR /
COPY . /

RUN mkdir /app/src/cards && mkdir /app/src/resp && /app/src/temp
RUN pip3 install flask
RUN pip3 install python-dotenv
RUN pip3 install openai
RUN pip3 install httpx

CMD ["python", "app/src/main.py"]
