FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# installs wkhtmltopdf (for pdfkit compatibility)
RUN apt-get update && apt-get install -y wkhtmltopdf

COPY . .

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
