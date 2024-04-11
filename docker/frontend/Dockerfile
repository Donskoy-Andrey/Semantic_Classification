FROM node:20.10.0

WORKDIR /app

COPY ../../semantic/frontend/package*.json ./

RUN npm install

COPY ../../semantic/frontend .

EXPOSE 3000

RUN npm install

CMD ["npm", "start"]
