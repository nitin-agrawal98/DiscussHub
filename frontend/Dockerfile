FROM node:alpine AS build

WORKDIR /app

COPY package.json .

RUN yarn install

COPY . .

RUN yarn start
