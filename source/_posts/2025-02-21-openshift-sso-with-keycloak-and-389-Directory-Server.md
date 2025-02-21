---
title: 紀錄Openshift介接Keycloak與389 Directory Server
comments: true
date: 2025-02-21 05:45:23
description:
categories: software_development
tags:
- openshift
- keycloak
- ldap
- openid_connect
- 389_directory_server
---

自己做完一輪後發現有很多Authentication和Authorization知識和觀念需要再補強: OAuth Flow、OpenID Connect、User federation、憑證的SAN。或許之後會在整理一篇比較偏觀念性的，並且可以對照這一篇出現的概念。

此外，Keycloak感覺十分強大，可以整合很多服務，值得進一步研究

![config_overview](config_overview.png)

## 目標
使用389 Directory Server的帳號與密碼登入Openshift Console

## 前置作業
- Openshift 4.17
    - Ingress URI: apps.foo.bar.com
- Keycloak 22.0.4
    - 啟用HTTPS且憑證需要包含SAN(Subject Alternative Name)
    - User federation設定介接389 Directory Server
    - DNS有一筆FQDN: keycloak.bar.com

### 啟用HTTPS且憑證需要包含SAN(Subject Alternative Name)

參考這篇，{% post_link enable-https-for-keycloak %}

### User federation設定介接389 Directory Server

使用[slominskir/keycloak\_ldap: Docker Compose with Keycloak and 389 LDAP Directory Server](https://github.com/slominskir/keycloak_ldap)當作例子

啟動container後預設Realm會有`test-realm`，包含一位使用者`jdoe`，User federation存在一個設定`test-realm-ldap-provider`

![keycloak_with_ldap_example](keycloak_with_ldap_example.png)

![keycloak_with_ldap_example_user_federation](keycloak_with_ldap_example_user_federation.png)

這位預設的使用者並無指定密碼，可以進入至ldap的container內設定
```
dsidm localhost account reset_password uid=jdoe,ou=People,dc=example,dc=com
```

## 主要設定

- Keycloak Client
- Openshift OAuth settings

### Keycloak Client
在Keycloak端的設定新增一個Client

![keycloak_create_client_1](keycloak_create_client_1.png)
- Client type: `OpenID Connect`
- Client ID: `keycloak`

須注意這邊的`keycloak`可以設定其他任意值，需要和後續Openshfit內的設定有關

![keycloak_create_client_2](keycloak_create_client_2.png)

- Client authentication: `On`
- Authentication flow: `Standard flow`
詳細說明可參考保哥的[如何用 Docker 快速上手 Keycloak 開發模式](https://blog.miniasp.com/post/2023/04/21/Running-Keycloak-in-development-mode)

![keycloak_create_client_3](keycloak_create_client_3.png)

- Valid redirect URIs: https://oauth-openshift.apps.foo.bar.com/oauth2callback/openid

須注意最後面的`openid`字串可以設定其他任意值，需要和後續Openshfit內的設定有關

### Openshift OAuth settings

Adminitration => Cluster Settings => Configuration => OAuth
![openshift_cluster_settings_oauth](openshift_cluster_settings_oauth.png)


Identitiy providers => Add 'OpenID Connect'

- Name: `openid`
    - 和Keycloak Client的**Valid redirect URIs**有關
- Client ID: `keycloak`
    - 和Keycloak Client的**Client ID**有關
- Client secret: 可以在Keycloak Client的**Credentials**找到
- Issuer URL: `https://keycloak.bar.com:8443/realms/test-realm`
    - test-realm是Keycloak內的Realm
    - 需要HTTPS
    - 這邊需要注意Keycloak的版本的URI會有些差異，可以參考[Keycloak: All API response with 404 - Stack Overflow](https://stackoverflow.com/questions/72596189/keycloak-all-api-response-with-404)，版本17(包含)之後的URI沒有auth的字串**https://keycloak.bar.com:8443/realms/yourrealm**，版本17(不包含)之前的URI有auth的字串，**http://keycloak.bar.com:8443/auth/realms/yourrealm**
- CA file
    - Keycloak的憑證，需要包含SAN(Subject Alternative Name)

有發生錯誤的話可以在Cluster Settings的ClusterOperators中關於authentication的Message看到相關訊息，有遇到以下幾個狀況
- 憑證不包含SAN時，會出現**OAuthServerConfigObservationDegraded: failed to apply IDP openid config: tls: failed to verify certificate: x509: certificate relies on legacy Common Name field, use SANs instead**
- Issure URL有問題，有出現**well-known/openid-configuration:**

例如下圖

![openshift_cluster_settings_oauth_openid_error](openshift_cluster_settings_oauth_openid_error.png)

成功的話Status顯示Available且登入畫面會出現所設定的OpenID Connect

![openshift_cluster_settings_oauth_openid_success_1](openshift_cluster_settings_oauth_openid_success_1.png)

![openshift_cluster_settings_oauth_openid_success_2](openshift_cluster_settings_oauth_openid_success_2.png)


## 測試

觀察一下URL:**https://keycloak.bar.com:8443/realms/test-realm/protocol/openid-connect/auth?client_id=keycloak&redirect_uri=https%3A%2F%2Foauth-openshift.apps.foo.bar.com%2Foauth2callback%2Fopenid&response_type=code&scope=openid&state=xxx**

有client_id和redirect_uri，看起來是之前在Keycloak Client當中設定的值

![openshift_cluster_settings_oauth_openid_success_3](openshift_cluster_settings_oauth_openid_success_3.png)


![openshift_cluster_settings_oauth_openid_success_4](openshift_cluster_settings_oauth_openid_success_4.png)

可以在kubeadmin觀察，jdoe登入後在User Management => Users會出現一筆紀錄，Identities為`openid:xxx`

![openshift_cluster_settings_oauth_openid_success_5](openshift_cluster_settings_oauth_openid_success_5.png)

## 參考
- [OpenShift, SSO with KeyCloak & Active Directory | DELL Technologies](https://www.dell.com/community/en/conversations/developer-blog/openshift-sso-with-keycloak-active-directory/647f9e39f4ccf8a8de2cc1ae)
- [How to Integrate OpenShift with Keycloak - The New Stack](https://thenewstack.io/how-to-integrate-openshift-with-keycloak/)
- LDAP
    - [設定Keycloak v19串接Windows AD / LDAP - Jovepater](https://jovepater.com/article/keycloak-windows-ad-ldap/)
    - [Keycloak使用群晖Synology Directory Server作为AD/LDAP用户数据源](https://bra.live/using-synology-directory-server-as-keycloak-user-federation-source/)
- 憑證
    - [Error x509: certificate relies on legacy Common Name field, use SANs instead in Openshift - Red Hat Customer Portal](https://access.redhat.com/solutions/6886271)
    - [How to create custom self-signed certificates for ingress and apiserver for Openshift using openssl - Red Hat Customer Portal](https://access.redhat.com/solutions/7034830)
    - [How to create a certificate with Subject Alternative Name (SAN) extensions for OpenShift 4 mirror registry - Red Hat Customer Portal](https://access.redhat.com/solutions/6973542)
    - [Create a self-signed certificate using OpenSSL | by Allan Sun | 隨筆雜記](https://blog.cssuen.tw/create-a-self-signed-certificate-using-openssl-240c7b0579d3)
    - [用 SAN Certificate 做 Multi-Domain Certificate | by Allan Sun | 隨筆雜記](https://blog.cssuen.tw/%E7%94%A8-san-certificate-%E5%81%9A-multi-domain-certificate-c7403e05c697)