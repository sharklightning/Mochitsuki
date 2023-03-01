FROM python:latest

WORKDIR /
COPY . /

RUN pip3 install flask
RUN pip3 install python-dotenv
RUN pip3 install openai
RUN pip3 install httpx

CMD ["python", "app/src/main.py"]