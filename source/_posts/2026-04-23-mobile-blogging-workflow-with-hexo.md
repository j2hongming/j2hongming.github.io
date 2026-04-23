---
title: 降低發文摩擦力：我的行動部落格發布工作流
comments: true
date: 2026-04-23 21:46:20
description: 分享如何利用 GitHub Action 與 AI 工具優化 Hexo 發文流程，實現隨時隨地用手機寫作並發布。
categories: software_development
tags:
  - Hexo
  - Workflow
  - GitHub Actions
  - Gemini
---

自從成功在高鐵上使用手機成功發出{% post_link productivity-from-chef-to-intentional-living '針對生產力的一些想法' %}，隱約感覺發文的摩擦力有明顯地下降。

整理並記錄一下脈絡。

## 第一個階段

需要一台已經安裝hexo 和git 的機器，以及一個文字編輯器。

首先利用hexo new ”foo”產生初始markdown檔案與目錄，接著使用文字編輯器打好文章後，執行hexo generate指令產生靜態網頁內容並用hexo server稍微在本機稍微檢查一下，沒什麼問題後使用git commit，然後git push到GitHub 

想想就累了😓，也被至少需要一台機器給限制住。

## 第二個階段

導入[GitHub Action](j2hongming.github.io/.github/workflows/pages.yml)後，處理了產生靜態網頁內容的部分，但還是需要一台機器產生文章markdown，編輯文章和處理git相關操作

## 第三個階段

思考能不能直接在手機編輯並發文，構想是我只要專注在文章內容，markdown需要的檔案名稱和頁面前置資料可以從內容自動生成，剛好今年接觸了Gemini Gem，透過它幫忙，省了不少力。平常突然冒出的想法就先用iPhone 的備忘錄記錄。

最後利用手機瀏覽器打開GitHub網頁直接新增檔案並送出commit即可。

想法/念頭/內心旁白 => [iPhone 備忘錄] => [Gemini Gem] => 產生markdown檔案名稱與頁面前置資料 => 手機瀏覽器打開GitHub網頁直接新增檔案並送出 commit

完成，這就是目前看到的這個頁面背後的流程，iPhone 備忘錄和Gemini Gem可以使用其他替代的東西，不會被綁死。GitLab也有類似的page和action功能，減少被GitHub 綁死的機會。
