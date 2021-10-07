FROM node:lts-alpine as build-stage
WORKDIR /homepage
COPY package*.json ./

RUN npm install
COPY . .
RUN npm run build

# # production stage
FROM nginx:stable-alpine as production-stage
# 필요없는 기존 conf 문서를 삭제하고, nginx에 설정하기 위한 conf를 복사
RUN rm /etc/nginx/conf.d/default.conf
COPY ./nginx/homepage.conf /etc/nginx/conf.d/homepage.conf
# build-stage(=상위 node 이미지)에서 빌드한 결과물을 nginx로 옮긴다
COPY --from=build-stage ./homepage/dist /usr/share/nginx/html/homepage
# 80번 포트 개방
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]