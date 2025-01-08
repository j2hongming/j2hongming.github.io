---
title: 更新Blog文章產製流程
comments: true
date: 2025-01-08 13:37:52
description:
categories: lab
tags:
- blog
- hexo
---

最近更新了如何產生一篇blog文章的流程與環境，趁著記憶猶新時紀錄一下

目前產生文章的流程整理如下

![](blog_post_flow.png)

## 1.0.0
在家裡的筆電上利用VirtualBox開一台VM安裝Ubuntu且有圖形介面，在VM內安裝hexo, vs code，亦即write, generate和deploy都在VM內部進行

![](blog_post_flow_1-0-0.png)

### 缺點
- 只能使用家裡筆電，其他環境無法產生文章與部屬
- VM圖形介面體感速度慢

### 需求
1. 能夠在任何環境都能簡單的撰寫文章，且環境越單純越好，以利於快速建置新環境
2. 我只需要專注在產生文章的原始資料(markdown)，commit後部屬自動化

## 2.0.0
首先，針對任何環境的需求，想到了vs code，搭配Remote SSH plugin，要寫一篇markdown的source很方便。此外，搭配git管理source，也能方便地和github.com同步。只要有安裝git的機器就能夠開始寫作，處理了環境越單純越好的需求，若需要測試與驗證，則僅需額外安裝hexo即可。

感恩github action, 只要透過撰寫yml就可以在github上完成部屬，滿足了commit後部屬自動化的需求。

![](blog_post_flow_2-0-0.png)

### 缺點
- AWS EC2或VPS Machine需要額外成本，可能考慮試試看github codespace