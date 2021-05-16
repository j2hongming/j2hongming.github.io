---
layout: post
title: "認證與授權筆記"
date: 2016-09-09 17:52:49 +0800
comments: true
categories: software_development
tags:
- authentication
- authorization 
---
- 認證(Authentication)
- 授權(Authorization)
<!-- more -->

## 認證(Authentication)
> 不要相信任何人!

對面走過來一個陌生人，「他是誰?」
對面走過來一個熟人，「是某某某阿」

為什麼會有如此差異呢?仔細想想，我們內建的第一道認證機制或許就是`臉孔`，透過這張臉我們可以瞬間知道走過來的人是誰。
等等...若是多胞胎的話呢?
若是這情況，第一道認證機制就會失效，此時就必須透過其他認證機制幫助我們辨識這個人是誰。`名牌`、`名片`、`身分證`、`指紋`、`暗號`...等等。

因此，回答「這個人是誰?」的問題就是`認證`。
幫助我們回答這問題的方法就是`認證機制`。

### 認證機制
#### Http Basic Authentication
參與元素：`Http Header`, `Username/Password`, `base64編碼`

一定要搭配SSL服用，否則會曝曬在陽光底下。

#### Token-base Authentication
回答以下三個問題

> 1. 如何運作
> 2. 有什麼好處
> 3. 有什麼壞處



#### OAuth

#### Json Web Token(JWT)

## 授權(Authorization)
> 朕不給﹐你不能搶

(未完待續...)
## 參考
- [REST API安全設計指南](http://blog.nsfocus.net/rest-api-design-safety/)
- [RESTful Api 身份認證中的安全性設計探討](https://mengkang.net/625.html)
- [How do I let users log into my RESTful API](http://restcookbook.com/Basics/loggingin/)
- [The Ins and Outs of Token Based Authentication](https://scotch.io/tutorials/the-ins-and-outs-of-token-based-authentication)
- [淺談RESTful API認證 Token機制使用經驗分享](http://www.slideshare.net/TunYuChang/restful-api-token)
