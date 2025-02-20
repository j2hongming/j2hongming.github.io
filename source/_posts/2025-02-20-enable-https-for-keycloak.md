---
title: Keycloak container啟用HTTPS
comments: true
date: 2025-02-20 09:10:29
description:
categories: software_development
tags:
- keycloak
- ssl
- tls
- https
- certificate
- ldap
---

使用[slominskir/keycloak\_ldap: Docker Compose with Keycloak and 389 LDAP Directory Server](https://github.com/slominskir/keycloak_ldap)當作例子

有三個部分需要調整: volumes, environment, ports

需要準備憑證並透過volume與environment讓keycloak可以讀得到，最後把8443 port開放出來

``` yml
    volumes:
      ...
      - ./certs/server.crt:/etc/x509/https/tls.crt
      - ./certs/server.key:/etc/x509/https/tls.key
```

``` yml
    environment:
      KC_HTTPS_CERTIFICATE_FILE: /etc/x509/https/tls.crt
      KC_HTTPS_CERTIFICATE_KEY_FILE: /etc/x509/https/tls.key
```

``` yml
    ports:
      ...
      - "8443:8443"
```

修改後的yaml如下:
``` yml
services:
  ldap:
    image: 389ds/dirsrv:2.4
    hostname: ldap
    container_name: ldap
    healthcheck:
      test: ["CMD", "/usr/lib/dirsrv/dscontainer", "-H"]
      interval: 10s
      timeout: 10s
      retries: 3
      start_period: 120s
    environment:
      DS_DM_PASSWORD: password
      DS_SUFFIX_NAME: dc=example,dc=com
    volumes:
      - ./ldap/init:/init
    entrypoint: /init/entrypoint.sh

  keycloak:
    image: quay.io/keycloak/keycloak:22.0.4
    depends_on:
      ldap:
        condition: service_healthy
    hostname: keycloak
    container_name: keycloak
    ports:
      - "8080:8080"
      - "8443:8443"
    environment:
      KC_HTTPS_CERTIFICATE_FILE: /etc/x509/https/tls.crt
      KC_HTTPS_CERTIFICATE_KEY_FILE: /etc/x509/https/tls.key
      KEYCLOAK_ADMIN: admin
      KEYCLOAK_ADMIN_PASSWORD: admin
    command: start-dev
    volumes:
      - ./keycloak/init:/init
      - ./certs/server.crt:/etc/x509/https/tls.crt
      - ./certs/server.key:/etc/x509/https/tls.key
    entrypoint: /init/entrypoint.sh
```

自簽一張有SAN設定的憑證作測試，之後使用openshift介接keycloak才不會遇到錯誤
``` bash
wget https://github.com/slominskir/keycloak_ldap.git
mkdir -p keycloak_ldap/certs
cd keycloak_ldap
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout certs/server.key -out certs/server.crt -days 30 -subj "/C=TW/ST=Taiwan/L=Taoyuan City/O=Foo/OU=Bar/CN=keycloak.foo.example.com" -extensions v3_req -config req.conf
```

req.conf
```
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[ req_distinguished_name ]
C = TW
ST = Taiwan
L = Taoyuan City
O = Foo
OU = Bar
CN = keycloak.foo.example.com

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = keycloak.foo.example.com
```

也可以自簽一張只有CN沒有SAN的憑證作測試
``` bash
wget https://github.com/slominskir/keycloak_ldap.git
mkdir -p keycloak_ldap/certs
cd keycloak_ldap
openssl req -x509 -newkey rsa:4096 -sha256 -nodes -keyout certs/server.key -out certs/server.crt -days 30 -subj "/C=TW/ST=Taiwan/L=Taoyuan City/O=Foo/OU=Bar/CN=keycloak.foo.example.com"
```

## 除錯
若出現錯誤的話，透過`docker logs keycloak`查log

正確啟動的話log會像
```
| Step 1: Start Keycloak |
--------------------------
--------------------------------------
| Step 2: Wait for Keycloak to start |
--------------------------------------
Updating the configuration and installing your custom providers, if any. Please wait.
2025-02-20 09:55:51,444 INFO  [io.quarkus.deployment.QuarkusAugmentor] (main) Quarkus augmentation completed in 7391ms
2025-02-20 09:55:53,021 INFO  [org.keycloak.quarkus.runtime.hostname.DefaultHostnameProvider] (main) Hostname settings: Base URL: <unset>, Hostname: <request>, Strict HTTPS: false, Path: <request>, Strict BackChannel: false, Admin URL: <unset>, Admin: <request>, Port: -1, Proxied: false
2025-02-20 09:55:54,774 WARN  [io.quarkus.agroal.runtime.DataSources] (main) Datasource <default> enables XA but transaction recovery is not enabled. Please enable transaction recovery by setting quarkus.transaction-manager.enable-recovery=true, otherwise data may be lost if the application is terminated abruptly
2025-02-20 09:55:55,371 WARN  [org.infinispan.PERSISTENCE] (keycloak-cache-init) ISPN000554: jboss-marshalling is deprecated and planned for removal
2025-02-20 09:55:55,479 WARN  [org.infinispan.CONFIG] (keycloak-cache-init) ISPN000569: Unable to persist Infinispan internal caches as no global state enabled
2025-02-20 09:55:55,609 INFO  [org.infinispan.CONTAINER] (keycloak-cache-init) ISPN000556: Starting user marshaller 'org.infinispan.jboss.marshalling.core.JBossUserMarshaller'
2025-02-20 09:55:56,191 INFO  [org.keycloak.connections.infinispan.DefaultInfinispanConnectionProviderFactory] (main) Node name: node_374503, Site name: null
2025-02-20 09:55:57,272 INFO  [org.keycloak.quarkus.runtime.storage.legacy.liquibase.QuarkusJpaUpdaterProvider] (main) Initializing database schema. Using changelog META-INF/jpa-changelog-master.xml
2025-02-20 09:55:59,380 INFO  [org.keycloak.broker.provider.AbstractIdentityProviderMapper] (main) Registering class org.keycloak.broker.provider.mappersync.ConfigSyncEventListener
2025-02-20 09:55:59,414 INFO  [org.keycloak.services] (main) KC-SERVICES0050: Initializing master realm
2025-02-20 09:56:01,297 INFO  [io.quarkus] (main) Keycloak 22.0.4 on JVM (powered by Quarkus 3.2.6.Final) started in 9.714s. Listening on: http://0.0.0.0:8080 and https://0.0.0.0:8443
2025-02-20 09:56:01,298 INFO  [io.quarkus] (main) Profile dev activated.
2025-02-20 09:56:01,298 INFO  [io.quarkus] (main) Installed features: [agroal, cdi, hibernate-orm, jdbc-h2, jdbc-mariadb, jdbc-mssql, jdbc-mysql, jdbc-oracle, jdbc-postgresql, keycloak, logging-gelf, micrometer, narayana-jta, reactive-routes, resteasy, resteasy-jackson, smallrye-context-propagation, smallrye-health, vertx]
2025-02-20 09:56:01,443 INFO  [org.keycloak.services] (main) KC-SERVICES0009: Added user 'admin' to realm 'master'
2025-02-20 09:56:01,445 WARN  [org.keycloak.quarkus.runtime.KeycloakMain] (main) Running the server in development mode. DO NOT use this configuration in production.
```

目前有遇到一個關於檔案權限的議題，調整完/etc/x509/https/tls.key權限後重啟就正常了
```
2025-02-20 09:53:25,858 INFO  [org.keycloak.connections.infinispan.DefaultInfinispanConnectionProviderFactory] (main) Node name: node_956104, Site name: null
2025-02-20 09:53:26,906 INFO  [org.keycloak.quarkus.runtime.storage.legacy.liquibase.QuarkusJpaUpdaterProvider] (main) Initializing database schema. Using changelog META-INF/jpa-changelog-master.xml
2025-02-20 09:53:28,746 INFO  [org.keycloak.services] (main) KC-SERVICES0050: Initializing master realm
2025-02-20 09:53:30,751 ERROR [org.keycloak.quarkus.runtime.cli.ExecutionExceptionHandler] (main) ERROR: Failed to start server in (development) mode
2025-02-20 09:53:30,752 ERROR [org.keycloak.quarkus.runtime.cli.ExecutionExceptionHandler] (main) ERROR: /etc/x509/https/tls.key
2025-02-20 09:53:30,753 ERROR [org.keycloak.quarkus.runtime.cli.ExecutionExceptionHandler] (main) For more details run the same command passing the '--verbose' option. Also you can use '--help' to see the details about the usage of the particular command.
```