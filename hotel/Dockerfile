
FROM python

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY . .



CMD ["python", "hotel/manage.py", "runserver", "0.0.0.0:8000"]