---
layout: post
title: "Notes for Vim"
date: 2016-02-19 11:28:15 +0800
comments: true
categories: software_development
tags:
- vim
---

- 概念Concept
- 基本Basic
- 組合技Combo
<!--more-->
## 概念Concept
- 模式
- 單檔案
- 單行
- 單詞
- 單檔案

### 模式
Command Line mode, Normal mode, Insert mode, 預設在Normal mode

Nm to Im: `i`

Nm to CLm:`:`

Im to Nm:`esc`

## 基本Basic

### 存檔
#### CL mode
    w #存檔
    q #離開
    wq #存檔並離開
    q! #不存檔強制離開

### 瞬間移動
#### N mode
##### 搜尋
    / #搜尋
    n #下一個符合
    N #上一個符合

##### 檔案觀點
    gg #檔頭
    G #檔尾
    j5 #往下移動5行, 5可改為任意數字

##### 行觀點
    0 #行內移動: 行首
    ^ #行內移動: 行首
    $ #行內移動: 行尾
    f #行內字元搜尋: 往後
    F #行內字元搜尋: 往前

##### 詞觀點
    w #單詞移動: 下一單詞之詞頭
    e #單詞移動: 下一單詞之詞尾
    b #單詞移動: 上一單詞之詞頭

#### CL mode
    0 #檔頭
    $ #檔尾
    n #跳到第n行

### 標記與複製

#### N mode
    v #選取
    V #標記行
    Ctrl + v #標記區塊
    y #複製標記內容
    yy #複製游標行
    p #在下一行貼上複製或刪除的內容
    P #在上一行貼上複製或刪除的內容

### 刪除與復原

#### N mode
    dd #刪除一行
    D #刪除至行尾
    u #復原
    Ctrl + r #重做

## 組合技Combo
### N mode
#### CP大法
    yy p #複製單行貼上

#### 快速刪除
    d f 字元 #刪除當時游標所在到到該字元前

## 參考資源
- [vim超基礎入門](http://www.slideshare.net/BruceLi2/008-vim)
- [爽爽快快學Vim(1)](http://blog.eddie.com.tw/2012/04/27/screencast-1-learning-vim-from-the-beginning/)
- [給程式設計師的Vim入門圖解說明](http://blog.vgod.tw/2009/12/08/vim-cheat-sheet-for-programmers/)
- [vi / vim 圖解鍵盤指令](http://blog.linux.org.tw/~jserv/archives/001675.html)
- [寫程式？那些老師沒教的事](http://www.slideshare.net/taichunmin/ss-16096723)
