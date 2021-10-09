FROM python:alpine

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["py", "main.py"]
