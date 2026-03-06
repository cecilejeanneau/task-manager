
# Use a minimal base image for reduced attack surface
FROM python:3.12-slim

WORKDIR /app
COPY . /app/

# Install only runtime dependencies
RUN pip install --no-cache-dir -r requirements.txt

# (Optional) Run linting and tests in CI, not in production image
# RUN pip install --no-cache-dir flake8 pytest
# RUN flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
# RUN PYTHONPATH=/app pytest --maxfail=1 --disable-warnings --tb=short

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
