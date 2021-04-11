---
title: web 概觀
comments: true
date: 2021-01-28 23:53:37
description: 把到目前為止所認知的web想法紀錄於此
categories: software_development
tags: web
---

## 靜態資訊

- 不涉及運算規則和狀態儲存
- 無法透過運算規則和狀態儲存統一做客製化
- 僅解決資訊呈現問題
- 資訊較單純

例如: 我的2020推薦書單

可以使用幾種方法實現:
手寫拍照上傳社群網站
使用Google doc word
找一個部落格平台發表

若需要朝向DIY的方向, 可以自己架設伺服器或使用IaaS服務商, 例如: AWS
大方向是找一台機器, 有一個可以讓Internet存取的到的伺服器

找一台實體機器，申請固定ip和domain name, 安裝Apache => 維護實體機器, ip, domain, Apache升級和Vulnerability, 靜態資訊內容
使用AWS EC2, 申請domain name, 安裝Apache => 維護domain, Apache升級和Vulnerability, 靜態資訊內容
AWS S3 static web, no HTTPS => 維護domain, 靜態資訊內容
AWS Cloudfront + S3 => 維護domain, 靜態資訊內容

## 動態資訊
我的2020推薦書單, 這個資訊可以變動的地方有幾個: 我, 2020, 書單, 也就是`人`, `時間`, `資源`
推薦的部份會涉及運算規則

例如:
只在人的部份做變化: 比爾蓋茨的2020推薦書單
在人和資源的部份變化: 美食水水的2020推薦美食

- 涉及運算規則和狀態儲存
- 透過運算規則和狀態儲存統一做客製化
- 解決資訊呈現和管理問題

使用Web Framework搭建運算規則, 使用資料儲存空間處理狀態儲存, 例如: 關聯式資料庫
