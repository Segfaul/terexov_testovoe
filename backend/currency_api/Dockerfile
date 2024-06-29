# Backend Dockerfile

FROM python:3.11.6-slim

RUN mkdir -p /terexov_testovoe/backend/currency_api
WORKDIR /terexov_testovoe

COPY backend/currency_api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY .env .
COPY backend/__init__.py ./backend
COPY backend/currency_api ./backend/currency_api
