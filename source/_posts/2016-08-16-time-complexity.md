---
layout: post
title: "時間複雜度筆記"
date: 2016-08-16 14:45:57 +0800
comments: true
categories: software_development
tags:
- algorithm
- time_complexity
---
閱讀完`ChiuCC`的文章[Complexity：Asymptotic Notation(漸進符號)](http://alrightchiu.github.io/SecondRound/complexityasymptotic-notationjian-jin-fu-hao.html)後整理的筆記。
<!-- more -->

時間複雜度(Complexity)旨在描述`時間`和`資料數量`的關係。漸進符號(Asymptotic Notation)是用來`評估`複雜度的工具，感覺上有種分類的味道。

複雜度有三兄弟: Theta, O, Omega。

漸進符號(Asymptotic Notation)本質上是`函數集合`，這裡的函數指的是f(n)，負責表現該算法的`趨勢`，並且經由找出趨勢的`邊界`，這裡的邊界指的是g(n)，來呈現該算法趨勢是屬於哪一類型的趨勢。

複雜度三兄弟中，Theta負責三明治的所有外層吐司；O負責三明治的上層吐司；Omega負責三明治的下層吐司。

上層吐司即為天花板，也就是上界(upper bound)，想得到的資訊為最差的情況需要花`多久`的時間。下層吐司即為地板，亦即下界(lower bound)，想取得的資訊為`至少`需花費多少時間。

### 其他資料
- [Big-O Algorithm Complexity Cheat Sheet](http://bigocheatsheet.com/)
