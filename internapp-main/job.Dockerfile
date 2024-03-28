FROM node:14
WORKDIR /usr/src/app
COPY package.json ./requirements.txt
RUN npm install cors
COPY . .
CMD node job.js 

