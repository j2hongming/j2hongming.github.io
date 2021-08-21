---
title: 透過AWS S3 Static Web設定Redirect
comments: true
date: 2021-07-30 01:13:37
description:
categories: software_development
tags:
- AWS
- S3
---
因為時間的關係, 工作上有一個需求, 希望使用自家domain先預留能夠接住已經發布的版本所送出的請求, 以避免後期使用者不想升版所造成的影響, 其中一個方向是透過redirect, 另一個方向是proxy

利用AWS S3 Static Web的功能設定Redirect, 有以下的限制
- 僅能使用http only的方式存取 s3 url (http://abc.com/api/v2/test)
  - S3的前面設定CloudFront, 就能夠使用HTTPS
- allow method: GET, HEAD, OPTIONS
- 預設HTTP 301 redirects, 不過可以利用Redirection rules作客製化

```json=
[
    {
        "Condition": {
            "KeyPrefixEquals": "api"
        },
        "Redirect": {
            "HostName": "awesome.com",
            "HttpRedirectCode": "307",
            "Protocol": "https"
        }
    }
]
```
## 參考
- [Configuring a webpage redirect](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-page-redirect.html)
- [HTTP 307](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/307)
