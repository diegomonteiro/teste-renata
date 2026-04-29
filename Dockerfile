FROM pdal/pdal:latest

WORKDIR /app

COPY requirements.txt .

RUN /opt/conda/bin/python -m pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["/opt/conda/bin/python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
