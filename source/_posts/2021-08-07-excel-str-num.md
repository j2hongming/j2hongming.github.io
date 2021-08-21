---
title: Excel的數值與文字
comments: true
date: 2021-08-07 00:41:31
description:
categories: software_development
tags:
- excel
---
使用python程式parse一個Excel發生錯誤, 看了log發現下列訊息
> TypeError: cannot concatenate 'str' and 'float' objects

後來查了一下Excel的儲存格有分為為數值和文字

> 格式設定為文字的數值在儲存格中會靠左對齊，而不是靠右對齊，而且通常會標有錯誤指標

![](excel_format.png)

## 參考
- [套用數值格式以修正文字格式數值](https://support.microsoft.com/zh-tw/office/%E5%A5%97%E7%94%A8%E6%95%B8%E5%80%BC%E6%A0%BC%E5%BC%8F%E4%BB%A5%E4%BF%AE%E6%AD%A3%E6%96%87%E5%AD%97%E6%A0%BC%E5%BC%8F%E6%95%B8%E5%80%BC-6599c03a-954d-4d83-b78a-23af2c8845d0)
- [將數字格式化為文字](https://support.microsoft.com/zh-hk/office/%E5%B0%87%E6%95%B8%E5%AD%97%E6%A0%BC%E5%BC%8F%E5%8C%96%E7%82%BA%E6%96%87%E5%AD%97-583160db-936b-4e52-bdff-6f1863518ba4)
