---
title: Customize the Openshift console URL
comments: true
date: 2025-05-27 06:22:07
description:
categories: software_development
tags:
- openshift
---



本來參考官方文章
1. [Customizing the console route](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/web_console/customizing-web-console#creating-custom-links_customizing-web-console)
2. [How to customize console URL in OpenShift 4 under the same *.apps subdomain](https://access.redhat.com/solutions/5143911)

沒有很清楚，最後主要參考這篇文章: [Customizing the OpenShift Console URL with TLS](https://meatybytes.io/posts/openshift/ocp-features/security/tls/customizing-console/)

## 目標
default URL: `console-openshift-console.apps.foo.bar.com`
customized URL:  `my-customized.bar.com`

## 現況
DNS record
- *.apps.foo.bar.com => 172.15.30.41

確認現有console URL
``` bash
oc get route -n openshift-console
```

## 調整Ingress config調整Ingress config
``` bash
oc edit ingress.config.openshift.io cluster
```

``` yml
apiVersion: config.openshift.io/v1
kind: Ingress
metadata:
  name: cluster
spec:
  componentRoutes:
    - name: console
      namespace: openshift-console
      hostname: my-customized.bar.com
```

## 新增一筆DNS Record
- *.apps.foo.bar.com => 172.15.30.41
- my-customized.bar.com => 172.15.30.41

## 確認
![](customized_openshift_web_console_url.png)