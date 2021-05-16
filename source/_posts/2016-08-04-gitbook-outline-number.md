---
layout: post
title: "如何設定gitbook側邊欄大綱顯示階層數字"
date: 2016-08-04 16:03:23 +0800
comments: true
categories: software_development
tags:
- gitbook
---

開心地開了一本gitbook，然後用線上編輯器做了初版的大綱，正當我準備檢視一下Build好的書長什麼樣子時...咦?

為什麼大綱左邊沒有出現階層數字，印象中之前看過的gitbook有。第一個想法是會不會我的`SUMMARY.md`寫法有誤，看了一下官方文件的範例好像也沒有提到關於出現階層數字的寫法...，只好呼喚Google大神，翻了gitbook教學文似乎也沒有特別提到相關的資料，不死心看看別人的範例，發現[Explore Gitbook](https://www.gitbook.com/explore)內的書有些有出現，有些沒有...
<!-- more -->

花了幾個小時測試和Google，毫無頭緒，正準備放棄的時候突然靈光一閃，想說gitbook最後也是根據某些模板產生相對應的html，既然如此會不會是有特別的模板提供這功能

看了[官方文件](https://toolchain.gitbook.com/themes/)發現gitbook 3.0.0之後有提供預設的模板，但在線上編輯器中卻沒看到相關設定，打開線上編輯器的Plugins Store搜尋`theme default`才發現預設沒被載入與啟用...，找到[theme default的說明頁面](https://plugins.gitbook.com/plugin/theme-default)，看到有個setting是`showLevel`，恩，就是它了吧!

以下為線上編輯器的設定畫面：

1. 點選`Plugins Store`。未設定前，右下方沒有出現`book.json`
![設定畫面1](/images/gitbook-snapshot/gitbook-plugin-theme-default-1.png)

2. 搜尋列輸入`theme default`，找到之後按下+號加入此plugin
![設定畫面2](/images/gitbook-snapshot/gitbook-plugin-theme-default-2.png)

3. 加入成功會顯示綠色並出現設定按鈕
![設定畫面3](/images/gitbook-snapshot/gitbook-plugin-theme-default-3.png)

4. 進入theme default設定畫面將**Show level indicator in TOC**開關打開
![設定畫面4](/images/gitbook-snapshot/gitbook-plugin-theme-default-4.png)

5. 回到編輯主畫面發現右下方出現了book.json，內容是剛剛設定的plugin，這邊要注意的是若沒有客製化的css，不須設定styles這個屬性，直接刪掉即可。
![設定畫面5](/images/gitbook-snapshot/gitbook-plugin-theme-default-5.png)

6. 要確認plugin是否載入成功，需到最近一次UPDATE的Build頁面確認
![設定畫面6](/images/gitbook-snapshot/gitbook-plugin-theme-default-6.png)

檢視一下新build出來的書，呼，總算出現階層數字啦!
