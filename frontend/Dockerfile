# Frontend Dockerfile

FROM node:18.19.1-slim

RUN mkdir /frontend
WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .

EXPOSE 3000
