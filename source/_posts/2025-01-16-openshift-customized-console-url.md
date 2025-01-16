---
title: 客製化openshift console URL
comments: true
date: 2025-01-16 07:54:15
description:
categories: software_development
tags:
- openshift
---

[官方文件](https://docs.openshift.com/container-platform/4.17/web_console/customizing-the-web-console.html#customizing-the-console-route_customizing-web-console)和[官方知識庫](https://access.redhat.com/solutions/5143911)都有提到如何修改，因為沒有太多上下文，第一次看完後有點摸不著頭緒，最後找到[Customizing the OpenShift Console URL with TLS](https://meatybytes.io/posts/openshift/ocp-features/security/tls/customizing-console/)並按照這一篇文章設定成功

從參考資料看起來要從預設的`console-openshift-console.apps.foo.bar.com`改為以下兩種形式都可以，目前只有試過第一種成功，第二種還需要客製化憑證，需要找時間再試試
1. 類似base domain的`my-customized.apps.foo.bar.com`或`my-customized.bar.com`
2. 不同base domain的`my-customized.other.com`

## Openshift Ingress Configuration in Cluster Settings

剛開始看到ingress.config.openshift.io，不太確定是屬於哪一種資料(Pod, Deployment, Service)，最後是在Cluster Settings找到，看起來是專屬於openshift的設定資料，在spec加上`componentRoutes`，儲存後就會生效

Cluster Settings
![](openshift_cluster_settings_for_ingress.png)

``` bash
oc edit ingress.config.openshift.io cluster
```

``` yml
apiVersion: config.openshift.io/v1
kind: Ingress
metadata:
  creationTimestamp: "2025-01-09T08:13:27Z"
  generation: 8
  name: cluster
  resourceVersion: "2859957"
  uid: 662c61fb-000a-4185-90f6-534c09cdf05f
spec:
  componentRoutes:
  - hostname: my-customized.apps.foo.bar.com
    name: console
    namespace: openshift-console
```

可以使用以下指令檢查，成功的話會多出一筆console-custom且原本的`console-openshift-console.apps.foo.bar.com`還是可以存取

``` bash
oc get route -n openshift-console
```

```
NAME             HOST/PORT                                             PATH   SERVICES    PORT    TERMINATION          WILDCARD
console          console-openshift-console.apps.foo.bar.com            console     https   reencrypt/Redirect   None
console-custom   my-customized.apps.foo.bar.com                                                console     https   reencrypt/Redirect   None
downloads        downloads-openshift-console.apps.foo.bar.com          downloads   http    edge/Redirect        None
```

### Optional: 客製化的URL不在apps.foo.bar.com的subdomain

需要在DNS加上一筆record，指向Ingress VIP

```
my-customized.bar.com <Ingress VIP>
```