---
title: 使用github action搭配HackMD API和mkdocs產生可線上存取的文件
comments: true
date: 2025-01-23 08:26:27
description:
categories: software_development
tags:
- github_action
- hackmd
- mkdocs
---

最初的想法是能不能把在HackMD寫的markdown可以變成在線上存取且有簡單搜尋功能的文件。

這個時間點是LLM的時代，當然要請ChatGPT幫忙，加上一點修改，很快就可以使用，需要注意的是HackMD內的markdown內容會完全公開在網路上，若有隱私需求就不太適合。

使用以下的prompt，給出的範例算很完整，很讚，可惜只能產生一篇且需帶入HackMD的某一篇筆記的ID。

```
Use github action to fetch article by HackMD API and use mkdocs to build the github project page
```

沒有滿足我目前的需求，需求是能夠透過HackMD API自動取得多篇筆記的ID且下載後當作mkdocs的輸入，產生文件

補上以下的prompt後，大概完成90%的需求了，讚讚。

```
Use https://hackmd.io/@hackmd-api/user-notes-api#Get-a-list-of-notes-in-the-users-workspace
```

第一個碰到的狀況是jq產生的資料並非list，另外開了一個prompt去問

```
jq to create list of objects
jq -c '.[] | {id: .id, title: .title}'
```

最後有得到可用的指令: `jq -c '[.[] | {id: .id, title: .title}]'`

第二個碰到的狀況是下載後解析失敗的狀況，剛開始以為是markdown內容有特殊字元，根據筆記ID找到相關markdown並修改了覺得有可能會造成解析失敗的字元後跑了2-3次，發現不太對，感覺是沒有下載成功

![](github_action_fetch_notes.png)

想了一下，202x這個年代的服務應該都會有限流機制，查了一下[限制](https://hackmd.io/@hackmd-api/api-policy#API-limits)如下

> There is a quota of 2000 calls per month and the rate limit is 100 calls every 5 minutes.

因為隱私需求，想了一下還是暫時先停止這個專案，所以最後並沒有處理這個問題。後續可以思考一下
- 能否利用過濾的方式讓想要的markdown變成文件
- 把原本Chatgpt給的範例當中shell script的部分改為python

## 參考
- [Getting Started - HackMD API](https://hackmd.io/@hackmd-api/developer-portal/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2FrkoVeBXkq)