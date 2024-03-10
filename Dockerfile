FROM python:3.12.1
WORKDIR /app
COPY . .
COPY templates/ templates/
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]

