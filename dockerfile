FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libpq-dev

# Install torch first from official wheel
COPY torch-2.6.0-cp310-cp310-manylinux1_x86_64.whl .
RUN pip install torch-2.6.0-cp310-cp310-manylinux1_x86_64.whl

# Then install the rest
COPY requirements.txt .
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "sentiment_project.wsgi:application", "--bind", "0.0.0.0:8000"]
