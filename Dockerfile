FROM python:slim
WORKDIR /code
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 50051
COPY . .
CMD ["python", "server.py"]
