FROM python:3.10

WORKDIR /app
    
COPY . /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD uvicorn nima_agent:app --port=8000 --host=0.0.0.0

