# develop stage
FROM node:16.14.2-alpine3.15 as develop-stage

WORKDIR /app
COPY package*.json ./
RUN yarn global add @quasar/cli
COPY ./frontend/ .
RUN npm i

# # build stage
# FROM develop-stage as build-stage
# RUN yarn
# RUN quasar build
# # production stage
# FROM nginx:1.17.5-alpine as production-stage
# COPY --from=build-stage /app/dist/spa /usr/share/nginx/html
# EXPOSE 80
# CMD ["nginx", "-g", "daemon off;"]
