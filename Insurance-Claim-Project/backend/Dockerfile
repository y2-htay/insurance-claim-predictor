FROM python:3.12

# Install PostgreSQL client tools (including pg_isready)
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
