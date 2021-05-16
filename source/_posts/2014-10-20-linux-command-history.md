---
layout: post
title: "Linux指令歷史紀錄"
date: 2014-10-20 17:09:32 +0800
comments: true
categories: software_development
tags:
- linux
- command
- history
---
##方法一
`Ctrl + r`: 搜尋指令歷史紀錄，進入**(reverse-i-search)**模式
<!-- more -->
在**reverse-i-search**下，輸入關鍵字

- `Enter`: 直接執行此指令
- `左右鍵`: 跳回一般命令提示字元
- `Ctrl + r`: 下一個

##方法二
- `history | more`
- `!n`: n為history的輸出編號
- `!keyword`: keyword為指定之關鍵字
- `history n`:  列出最近n個使用的指令

##Ref.
1. [Linux 指令歷史紀錄（History）的操作教學與範例](http://www.gtwang.org/2013/10/mastering-linux-command-line-history.html)
