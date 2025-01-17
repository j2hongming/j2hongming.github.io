---
title: 啟用Inbound SSL，讓使用者可以用HTTPS存取Nexus
comments: true
date: 2025-01-17 06:26:36
description:
categories: software_development
tags:
- nexus
- ssl
- tls
- https
- certificate
- keytool
---

完整程式碼參考[Github: awesome_container](https://github.com/j2hongming/awesome_container)

## 使用docker啟用nexus
官方建議使用volume將資料持久化，另一種方式是使用mount

docker-compose.yml
``` yml
services:
  nexus:
    image: sonatype/nexus3
    container_name: nexus
    ports:
      - "8081:8081"
      # https://blog.yowko.com/nexus-docker-image-rergistry/
      - "8082:8082"
    volumes:
      - nexus-data:/nexus-data

volumes:
  nexus-data:
    name: nexus-data
```

``` bash
docker compose up -d
```

透過http://{Nexus FQDN}:8081存取

## 修改nexus設定，啟用Inbound SSL

在container內，注意三個主要的路徑
- /nexus-data/etc/ssl/
- /nexus-data/etc/nexus.properties
- /opt/sonatype/nexus/etc/jetty/jetty-https.xml

主要方向是準備keystore.jks並修改jetty server相關的設定

### 準備keystore.jks，讓container內的jetty server使用

看起來nexus是使用java生態系，跑在jetty上。[jetty](https://zh.wikipedia.org/zh-tw/Jetty)是一個基於Java的網頁伺服器和Java Servlet容器

在有[keytool](https://en.wikipedia.org/wiki/Java_KeyStore)的環境產生keystore.jks，參考[官方文件](https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide)
``` bash
keytool -genkeypair -keystore keystore.jks -storepass foo@bar -alias foo.com -keyalg RSA -keysize 2048 -validity 5000 -keypass foo@bar -dname 'CN=*.foo.com, OU=Sonatype, O=Sonatype, L=Unspecified, ST=Unspecified, C=US' -ext 'SAN=DNS:nexus.foo.com,DNS:bar.foo.com,DNS:repo.foo.com'
```

注意`-storepass foo@bar`和`-keypass foo@bar`，接下來jetty https設定會用到

### 準備nexus.properties

nexus.properties
``` bash
# Jetty section
# application-port=8081
application-port-ssl=28443
# application-host=0.0.0.0
# nexus-args=${jetty.etc}/jetty.xml,${jetty.etc}/jetty-http.xml,${jetty.etc}/jetty-requestlog.xml
nexus-args=${jetty.etc}/jetty.xml,${jetty.etc}/jetty-http.xml,${jetty.etc}/jetty-https.xml,${jetty.etc}/jetty-requestlog.xml
# nexus-context-path=/${NEXUS_CONTEXT}
ssl.etc=${karaf.data}/etc/ssl

# Nexus section
# nexus-edition=nexus-pro-edition
# nexus-features=\
#  nexus-pro-feature
```

`application-port-ssl=28443`，inbound SSL使用的port，https://{Nexus FQDN}:28443
`nexus-args`加入`${jetty.etc}/jetty-https.xml`
`ssl.etc=${karaf.data}/etc/ssl`指定keystore.jks的位置

### 調整jerry-https.xml內的參數
主要是以下幾個地方
- `<Set name="KeyStorePassword">foo@bar</Set>`
- `<Set name="KeyManagerPassword">foo@bar</Set>`
- `<Set name="TrustStorePassword">foo@bar</Set>`


## 啟用Inbound SSL的docker compose檔案

docker-compose.yml
``` yml
services:
  nexus:
    image: sonatype/nexus3
    container_name: nexus
    ports:
      - "8081:8081"
      - "28443:28443"
      # https://blog.yowko.com/nexus-docker-image-rergistry/
      - "8082:8082"
    volumes:
      - nexus-data:/nexus-data
      - ./keystore.jks:/nexus-data/etc/ssl/keystore.jks
      - ./nexus.properties:/nexus-data/etc/nexus.properties
      - ./jetty-https.xml:/opt/sonatype/nexus/etc/jetty/jetty-https.xml

volumes:
  nexus-data:
    name: nexus-data
```

透過https://{Nexus FQDN}:28443存取

## 參考
- [sonatype/nexus3 - Docker Image | Docker Hub](https://hub.docker.com/r/sonatype/nexus3/)
    - [使用 Docker 建立 Nexus3 的 Image Registry - Yowko's Notes](https://blog.yowko.com/nexus-docker-image-rergistry/)
- [Configuring SSL](https://help.sonatype.com/en/configuring-ssl.html)
- [SSL Certificate Guide – Sonatype Support](https://support.sonatype.com/hc/en-us/articles/213465768-SSL-Certificate-Guide)