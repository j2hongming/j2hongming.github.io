---
title: 同步keycloak的group至openshift
comments: true
date: 2025-04-30 07:37:00
description:
categories: software_development
tags:
- openshift
- keycloak
- openid_connect
---

延伸這一篇的內容:{% post_link openshift-sso-with-keycloak-and-389-Directory-Server '紀錄Openshift介接Keycloak與389 Directory Server' %}，在LDAP內綁定user至group後，
發現LDAP的group並沒有被同步至keycloak和openshift。

``` bash
ldap:/ # dsidm localhost -b "dc=example,dc=com" organizationalunit create --ou Groups
Successfully created Groups
ldap:/ # dsidm localhost -b "dc=example,dc=com" organizationalunit list
example
People
Groups
ldap:/ # dsidm localhost -b "dc=example,dc=com" account list
dc=example,dc=com
ou=People,dc=example,dc=com
uid=jdoe,ou=People,dc=example,dc=com
uid=william,ou=People,dc=example,dc=com
ou=Groups,dc=example,dc=com
ldap:/ # dsidm localhost -b "dc=example,dc=com" group create
Enter value for cn : bu_1
Successfully created bu_1
ldap:/ # dsidm localhost -b "dc=example,dc=com" group create
Enter value for cn : bu_2
Successfully created bu_2
ldap:/ # dsidm localhost group add_member bu_1 uid=jdoe,ou=People,dc=example,dc=com
added member: uid=jdoe,ou=People,dc=example,dc=com
ldap:/ # dsidm localhost group add_member bu_2 uid=william,ou=People,dc=example,dc=com
added member: uid=william,ou=People,dc=example,dc=com
ldap:/ #
```

`jdoe` belongs to group `bu_1`
`william` belongs to group `bu_2`

有兩件事要處理
1. LDAP的group同步至Keycloak
2. Keycloak的group同步至Openshift

## LDAP的group同步至keycloak
參考[設定Keycloak v19串接Windows AD / LDAP - Jovepater](https://jovepater.com/article/keycloak-windows-ad-ldap/)，主要需設定**User federation**的Mapper，Mapper Type為**group-ldap-mapper**，**LDAP Groups DN**需對應LDAP的實際值，這邊是**ou=Groups,dc=example,dc=com**

![ldap_keycloak_1](ldap_keycloak_1.png)

![ldap_keycloak_2](ldap_keycloak_2.png)

![ldap_keycloak_3](ldap_keycloak_3.png)

設定完成後，手動同步
![ldap_keycloak_4](ldap_keycloak_4.png)

成功的話會出現在Keycloak Groups的清單
![ldap_keycloak_5](ldap_keycloak_5.png)

## Keycloak的group同步至Openshift

這邊卡了一陣子，有找到官網的文件:[Chapter 7. Configuring identity providers | Red Hat Product Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/authentication_and_authorization/configuring-identity-providers#identity-provider-oidc-CR_configuring-oidc-identity-provider)，但還是有點一頭霧水，只知道可能需要在openid的yaml內補上groups，其他部分不太確定要怎麼做，幸好2025年是生成式AI的時代，感謝Perpluxity

prompt如下
```
I have a openshift cluster and a keycloak. I use OAuth in openshift with openid connect related with keycloak.
keycloak has a realm which name is test-realm and there are two users and two groups. one of the user is foo_user and its group is bu_1

using openshift webconsole to login in with foo_user. there is user sync from keycloak but the group does not sync.

can you figure out what happen
```

[Perpluxity的結果](https://www.perplexity.ai/search/i-have-a-openshift-cluster-and-FBAUKiDFRPqjvXBBR6usZA?1=d)幫了很大的忙，了解除了Openshift端需要調整之外，原本的Identity Provider(Keycloak)也需要調整，也獲得一個關鍵的參考文章: [Keycloak & Open Shift](https://blog.badgerops.net/keycloak-open-shift/)

有兩個主要修改
1. 在Keycloak端的**Client Scope**新增Mapper，Mapper Type為**Group Membership**
2. 在Openshift端的**OAuth Configuration**需加上claims的groups

### Keycloak端新增Mapper
試了兩種方式，目前兩種都可以順利將Keycloak的group同步至Openshift

第一種是參考Perpluxity的結果，在特定Client內設定Client Scope的Mapper

![keycloak_client_groups_1](keycloak_client_groups_1.png)

![keycloak_client_groups_2](keycloak_client_groups_2.png)

![keycloak_client_groups_3](keycloak_client_groups_3.png)

![keycloak_client_groups_4](keycloak_client_groups_4.png)

這邊須注意**Full group path**要關閉，開啟的話登入會失敗

開或關的影響是在openid connect回傳的JWT ID Tokens內的groups內容，開啟的話例如: **/bu_1**，關閉的話僅保留 **bu_1**，沒有/，這部分會在下面驗證的段落看到實際例子
![keycloak_client_groups_5](keycloak_client_groups_5.png)

![keycloak_client_groups_6](keycloak_client_groups_6.png)

第二種參考這一篇[Keycloak & Open Shift](https://blog.badgerops.net/keycloak-open-shift/)，在**profile**這個Client Scope內加入

![keycloak_client_groups_by_profile_1](keycloak_client_groups_by_profile_1.png)

![keycloak_client_groups_by_profile_2](keycloak_client_groups_by_profile_2.png)

同上，這邊須注意**Full group path**要關閉，開啟的話登入會失敗
![keycloak_client_groups_by_profile_3](keycloak_client_groups_by_profile_3.png)

### Openshift端加上claims的groups

![keycloak_client_groups_7](keycloak_client_groups_7.png)

[官網範例](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/authentication_and_authorization/configuring-identity-providers#identity-provider-oidc-CR_configuring-oidc-identity-provider)如下，關鍵是claim的groups:

``` yml
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: oidcidp
    mappingMethod: claim
    type: OpenID
    openID:
      clientID: ...
      clientSecret:
        name: idp-secret
      ca: 
        name: ca-config-map
      extraScopes: 
      - email
      - profile
      extraAuthorizeParameters: 
        include_granted_scopes: "true"
      claims:
        preferredUsername: 
        - preferred_username
        - email
        name: 
        - nickname
        - given_name
        - name
        email: 
        - custom_email_claim
        - email
        groups: 
        - groups
      issuer: https://www.idp-issuer.com
```

### Keycloak端和Openshift端都調整完成後，重新登入

成功啦! 感動涕零QQ
![keycloak_group_in_openshift](keycloak_group_in_openshift.png)

### Keycloak端新增Mapper後如何驗證JWT ID Token的內容

這部分也卡了一陣子，生成式AI這次沒有辦法幫上忙，最後是從[Keycloak & Open Shift](https://blog.badgerops.net/keycloak-open-shift/)這篇提到的[group is not coming in jwt token in keycloak 23.0.0 - Stack Overflow](https://stackoverflow.com/questions/76919561/group-is-not-coming-in-jwt-token-in-keycloak-23-0-0)進而摸索出來

使用下列方式取得JWT ID Token的內容

``` bash
curl -k --request POST \
  --url "https://keycloak.foo.com:8443/realms/test-realm/protocol/openid-connect/token" \
  --data "grant_type=password&client_id=admin-cli&username=jdoe&password=bar"
```

經過JWT decode後，觀察是否出現groups的key
``` json
{
  "exp": 1745998219,
  "iat": 1745997919,
  "jti": "d69b4c67-9a94-48d0-ac7b-cd5ba1d80fb6",
  "iss": "https://keycloak.foo.com:8443/realms/test-realm",
  "sub": "59103cfb-73e3-400c-a558-ca3a1bcd903e",
  "typ": "Bearer",
  "azp": "admin-cli",
  "session_state": "3ddcbeeb-69f4-4950-b33c-996ac0170b5b",
  "acr": "1",
  "scope": "profile email",
  "sid": "3ddcbeeb-69f4-4950-b33c-996ac0170b5b",
  "email_verified": false,
  "name": "John Doe Doe",
  "groups": [
    "bu_1"
  ],
  "preferred_username": "jdoe",
  "given_name": "John Doe",
  "family_name": "Doe"
}
```