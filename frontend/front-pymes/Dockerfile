# Stage 1: Build the Angular app with Node.js 22
FROM node:22-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build --configuration=production

# Stage 2: Serve the built app with Nginx
FROM nginx:alpine
COPY --from=builder /app/dist/front-pymes /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80