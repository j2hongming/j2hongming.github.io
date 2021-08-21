---
title: CloudFront使用Host Header決定distribution
comments: true
date: 2021-07-30 01:27:56
description:
categories: software_development
tags:
- AWS
- CloudFront
---
測試某個功能時, 本來想透過設定本地端的CNAME, 達成訪問測試站而非正式站的目的, 發現一直失敗, 會拿到正式站的資料, 原來是已經發布的版本內的寫法, 造成Host是固定的

驗證的方式如下

1. curl -v --output file http://abc.com/file
2. curl -v --output file http://beta.abc.com/file
3. curl -H "Host: abc.com" -v --output file http://beta.abc.com/file

3拿到和1相同的檔案
