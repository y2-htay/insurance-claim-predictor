FROM python:3.12

# Install PostgreSQL client tools (including pg_isready)
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# installs wkhtmltopdf (for pdfkit compatibility)
RUN apt-get update && apt-get install -y wkhtmltopdf

COPY . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
