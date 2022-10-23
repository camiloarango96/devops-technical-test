FROM python:3.8
WORKDIR /app
COPY src .
COPY requirements.txt .
RUN pip install -r requirements.txt 

CMD ["python", "src/app.py"]

EXPOSE 80