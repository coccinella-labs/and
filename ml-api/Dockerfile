FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade --index-url https://pypi.org/simple pip setuptools wheel
RUN pip install --no-cache-dir --index-url https://pypi.org/simple -r requirements.txt
RUN pip install --ignore-requires-python --index-url https://pypi.org/simple numpy==2.3.3

COPY . .

EXPOSE 8000

CMD ["python", "main.py"]