---
title: 更換留言系統至utterances
comments: true
date: 2025-01-09 05:15:55
description:
categories: lab
tags:
- blog
- utterances
---

原本也是用Disqus，看到好幾個部落格的留言系統介面都轉為github issue，想說趁著這次重啟blog計畫一起更新。

目前看到唯一的缺點是留言時需要登入github帳號，不過因為這個blog大部分是自己做個紀錄，沒啥受眾，這點相對是小事


## 安裝utterances app
看到很多文章安裝utterances app時給的都是連結，現在看到連結都有點怕怕的，擔心是詐騙，想說紀錄一下怎麼從github介面到utterances app的安裝畫面

從Marketplace進入
![](utterances-1.png)

![](utterances-2.png)

![](utterances-3.png)

雖然是0元，還是需要輸入帳單資訊
![](utterances-4.png)

選擇需安裝的repository，參考資料中大部分人都選擇和github hosted site repository放一起，只有一篇有另外開一個repository，想了一下github issue的資料並不會影響到blog文章的markdown source code，所以決定不另開repository
![](utterances-5.png)

至repository頁面確認是否有utterances
![](utterances-6.png)

## 修改theme
這邊需要看所使用的theme是否有支援，這個blog使用的是[cactus](https://github.com/probberechts/hexo-theme-cactus)，看了一下README有支援

修改`themes/cactus/_config.yml`，可以參考[這邊](https://utteranc.es/)

``` yml
# Fill in your Utterances data to enable Utterances comments
utterances:
  enabled: true
  repo: j2hongming/j2hongming.github.io
  issue_term: pathname
  label: Comment
  theme: gruvbox-dark
```

## 參考
- [放棄 Disqus 開始使用 utterances 作為 GitHub Page 的留言板 · dw's 小站](https://dwye.dev/post/no-disqus-but-utterances/)
- [Utterances - 用 GitHub Issues 當文章留言區](https://blog.wei-lee.me/posts/tech/2022/02/use-github-issues-as-comment-system/)
- [使用 utterances 建置 Github Page 留言系統 | Byte and Ink](https://minglunwu.com/notes/2022/utteranc_on_github_page.html/)
- [Gatsby | 用 utterances 替 Gatsby 的 Blog 網站申裝 GitHub Issue 留言功能 | by 神Q超人 | Starbugs Weekly 星巴哥技術專欄 | Medium](https://medium.com/starbugs/gatsby-%E7%94%A8-utterances-%E6%9B%BF-gatsby-%E7%9A%84-blog-%E7%B6%B2%E7%AB%99%E7%94%B3%E8%A3%9D-github-issue-%E7%95%99%E8%A8%80%E5%8A%9F%E8%83%BD-e8593318e5a3)
    - 另外開一個repository