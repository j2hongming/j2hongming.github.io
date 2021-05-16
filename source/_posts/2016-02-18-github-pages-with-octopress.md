---
layout: post
title: "Github Pages with Octopress"
date: 2016-02-18 17:29:01 +0800
comments: true
categories: software_development
tags:
- github
- octopress 
---

- 建置Octopress
- 設定佈署到 github
- 網站設定
- 內容管理
<!-- more -->

## 建置Octopress

## 設定佈署到 github
    rake setup_github_pages
輸入自己的Github Pages repository url
git@github.com:your_username/your_username.github.io.git

## 網站設定
[Configuring Octopress](http://octopress.org/docs/configuring/)

## 內容管理
Octopress的網頁內容是使用[Markdown語法](http://markdown.tw/)
Blog的文章會被存放在source/_posts, 以Jekyll's naming conventions:YYYY-MM-DD-post-title.markdown來命名

### 如何在Octopress分享程式碼
#### markdown方法
    若為區塊程式碼, 使用4個空白或1個tab
    若為行內程式碼, 使用反引號 `
#### octopress方法
[Sharing Code Snippets in Octopress](http://octopress.org/docs/blogging/code/)


### 常用指令
建立新文章

    rake new_post["標題"]
    #保存在 source/_posts/日期-標題.markdown

建立新頁面

    rake new_page[super-awesome]
    #creates /source/super-awesome/index.markdown
    #保存在anywhere in your blog source directory

    rake new_page[super-awesome/page.html]
    # creates /source/super-awesome/page.html 

產生網站檔案

    rake generate
    # Generates posts and pages into the public directory

發佈到 GitHub

    rake deploy
