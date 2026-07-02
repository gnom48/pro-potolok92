FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5555

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5555", "app:app"]
