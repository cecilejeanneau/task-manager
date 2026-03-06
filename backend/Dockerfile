FROM python:3.12

WORKDIR /app
COPY . /app/

RUN pip install -r requirements.txt \
	&& pip install flake8 \
	&& flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics \
	&& PYTHONPATH=/app pytest --maxfail=1 --disable-warnings --tb=short

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
