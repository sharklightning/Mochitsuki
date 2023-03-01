FROM python:latest

WORKDIR /
COPY . /

RUN pip3 install flask
RUN pip3 install python-dotenv
RUN pip3 install openai
RUN pip3 install httpx
RUN mkdir app/src/cards && mkdir app/src/resp && app/src/temp

CMD ["python", "app/src/main.py"]
