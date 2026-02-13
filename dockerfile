FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /servidor

COPY . .

EXPOSE 5555

CMD ["python3", "servidor.py"]