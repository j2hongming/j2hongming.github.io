---
layout: post
title: "No Access-Control-Allow-Origin header is present on the requested resource"
date: 2016-04-28 11:25:22 +0800
comments: true
categories: software_development
tags:
- http
- cors 
---

- 問題描述
- 本質
- 解法
<!-- more -->

## 問題描述
使用jQuery AJAX發出Request時，console出現No 'Access-Control-Allow-Origin' header is present on the requested resource

``` javascript CORS.js
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script type="text/javascript">
// ERROR, and show error message in console 
var url = "http://data.tycg.gov.tw/api/v1/rest/datastore/a1b4714b-3b75-4ff8-a8f2-cc377e4eaa0f?format=json";
// SUCCESS
var url = 'http://ptx.transportdata.tw/MOTC/v1/Bus/EstimatedTimeOfArrival/Thb?%24format=json&$top=10';

$.ajax({
   url: url,
   type: "GET",
   dataType: "JSON",
   success: function(data, textStatus, request) {
     alert("SUCCESS!!!");
     console.log(data);
   },
   error: function() {
     alert("ERROR!!!");
   }
 });

</script>
```
{% gist 89c858fdf4fd510fd910787a64eb9f04 CORS.js %}

## 本質
基於同源策略(Same-origin policy)所形成的議題
根據MDN所描述，同源的定義必須`protocol`, `host`, `port`相同
所以若要取得不同網域的資源會受到限制。

## 解法
HTTP response header加上`Access-Control-Allow-Origin`屬性，若有機會碰到Server端的前提下。

使用JSONP溝通，Client端和Server端都要支援。

JQuery降版到1.4，只能動到Client端，Server端是別人家的。

## Ref.
- [No 'Access-Control-Allow-Origin' header is present on the requested resource](http://stackoverflow.com/questions/20035101/no-access-control-allow-origin-header-is-present-on-the-requested-resource)
- [HTTP access control (CORS):MDN](https://developer.mozilla.org/zh-TW/docs/HTTP/Access_control_CORS)
- [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
- [Cross Domain Ajax 跨網域抓取資料(JSONP)](http://ithelp.ithome.com.tw/question/10094915?tab=opinion)
- [$.ajax and JSONP. ParseError and Uncaught SyntaxError: Unexpected token :](http://stackoverflow.com/questions/10507345/ajax-and-jsonp-parseerror-and-uncaught-syntaxerror-unexpected-token)
