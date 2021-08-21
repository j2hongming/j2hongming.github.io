---
title: 在本機瀏覽Open API格式的文件
comments: true
date: 2021-08-06 00:59:35
description:
categories: software_development
tags:
- open_api
- swagger
- redoc
---
Open API類似原始資料, 可以使用ReDoc或是Swagger UI其中之一呈現

若有使用vs code的話可以直接安裝擴充功能: [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi)

若想要放在內部機器上可以使用docker

```
git clone git@github.com:j2hongming/open_api.git
```

docker-compose.yaml內容如下
```yaml=
version: '3'
services:
  redoc:
    image: redocly/redoc
    ports:
      - 8888:80
    volumes:
      - ./api.yaml:/usr/share/nginx/html/api.yaml
    environment:
      - SPEC_URL=/api.yaml
  swagger:
    image: swaggerapi/swagger-ui
    ports:
      - 8080:8080
    volumes:
      - ./api.yaml:/api.yaml
    environment:
      - SWAGGER_JSON=/api.yaml
```

## 參考
- [OpenAPI 3.0 Tutorial](https://support.smartbear.com/swaggerhub/docs/tutorials/openapi-3-tutorial.html)
- [Swagger Live Demo](https://editor.swagger.io/)
- [Bearer Authentication](https://swagger.io/docs/specification/authentication/bearer-authentication/)
- [Python Flask automatically generated Swagger 3.0/Openapi Document](http://donofden.com/blog/2020/06/14/Python-Flask-automatically-generated-Swagger-3-0-openapi-Document)
