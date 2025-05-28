FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install flask pandas openpyxl pytz
EXPOSE 10000
CMD ["python", "server.py"]
