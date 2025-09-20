FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5555

# TODO: это плохо - сервре для отладки. Но это единственное что способно запустить scheduler
CMD ["flask", "run", "--host=0.0.0.0", "--port=5555", "--no-reload"]

# CMD ["python", "app.py"]
# CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5555", "app:app"]