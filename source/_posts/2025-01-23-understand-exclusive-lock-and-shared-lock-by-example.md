---
title: 透過一個例子理解Exclusive lock和Shared lock的概念
comments: true
date: 2025-01-23 07:27:27
description:
categories: software_development
tags:
- lock
---

想像有一間高級廁所，內部都是黃金打造而成，門上有一道門鎖且有一把專用鑰匙(Exclusive lock)。

因為內裝華麗，開放給持有參觀門票(Shared lock)的一般民眾參觀廁所內部(Read operation)。此外，這間廁所還是可以使用(Write operation)，需注意的是有生理需求的人拿到專用鑰匙進去上廁所後就暫時停止發售參觀門票，等到使用完畢後才會重新開放售票。

當還有持票民眾在參觀時，不開放廁所使用，亦即不能外借專用鑰匙，需等到沒有人在參觀時才會重新開放出借專用鑰匙給有生理需求的民眾。

- 有參觀需求的民眾
- 有生理需求的民眾
- 門鎖與專用鑰匙
- 參觀門票


## 參考
- [複習資料庫的 Isolation Level 與圖解五個常見的 Race Conditions | by Chester Chu | Medium](https://medium.com/@chester.yw.chu/%E8%A4%87%E7%BF%92%E8%B3%87%E6%96%99%E5%BA%AB%E7%9A%84-isolation-level-%E8%88%87%E5%B8%B8%E8%A6%8B%E7%9A%84%E4%BA%94%E5%80%8B-race-conditions-%E5%9C%96%E8%A7%A3-16e8d472a25c)