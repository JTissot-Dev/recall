FROM node:24-bookworm
WORKDIR /app
COPY . .
RUN npm i
COPY src src
COPY public public
CMD ["sh", "-c", "npm run build && npm run start"]