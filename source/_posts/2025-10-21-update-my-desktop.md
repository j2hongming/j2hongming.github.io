---
title: 睽違12年後換電腦
comments: true
date: 2025-10-21 23:04:34
description:
categories: lab
tags:
- desktop
---

上一台電腦是剛2013年成為職場新鮮人時購入的ASUS筆電，撐到2025年總算可以讓它休息了，當時Windows 8還是主流作業系統，現在已經Windows 11了XD

![](2025_update_desktop.png)

剛好搭上2025年Nvidia推出50系列的GPU，原本想在4月左右5070顯卡開始販售後更換，無奈顯卡缺貨潮並且在5月碰上報稅事件，現金有些不足

隔了快半年等到9月中看了一下顯卡供貨已經充足，報稅事件也處理告一段落，重啟停滯一段時間的需求

最後是請線上店家幫忙組裝，參考了以下規格並列出需求
- [規格參考1](https://ofeyhong.pixnet.net/blog/post/227142784)
- [規格參考2](https://ofeyhong.pixnet.net/blog/post/227156140)
- [規格參考3](https://ofeyhong.pixnet.net/blog/post/227248420)

## 需求
- 3D遊戲機，特效全開，遊戲如魔物獵人荒野、Cyberpunk 2077及未來的一些單機大作，希望效能能夠全開或是開到70~80%。
- 使用WSL，使用Hype-V開虛擬機器
- RTX 5070、記憶體至少64GB
- 雙SSD 2TB(系統+遊戲碟)+2TB(資料碟)

## 最終規格
- AMD R7-9700X【8核/16緒】3.8G(↑5.5G)/具RDNA內顯/65W (三年保)
- CPU塔型散熱器 FSP 全漢 MP7 Black (雙塔/12cm雙扇/6導管)
- 華碩 TUF GAMING B850-PLUS WIFI (ATX/Realtek2.5G+Wi-Fi 7/註五年)
- 金士頓 Fury Beast DDR5-5600 64G (32G*2條/白散熱片) 終身保
- 固態硬碟 金士頓 KC3000 2TB/M.2 PCIe Gen4  (五年保)   C槽系統碟
- 固態硬碟 金士頓 KC3000 2TB/M.2 PCIe Gen4  (五年保)   D槽資料碟
- 華碩 TUF-RTX5070-O12G-GAMING (三風扇/註冊五年保)
- 海韻 CORE GX-850 ATX3 白色 (80+金牌/ATX3.1/PCIe 5.1/全模組/十年保固)
- 君主 AIR 1000 LITE 玻璃透側/白色 (ATX/無RGB/內建風扇前2+後1)
- Win11 專業PRO彩盒版

## 到貨
從9/20開始溝通到9/30收到實體，中間發現有一種期待的心情，感覺這種期待感已經很久沒有出現了

## 開始初始化機器
收到的機器已經有作業系統Windows 11的狀態，以下是針對自己的需求作初始化

### 主機名稱(Hostname)、帳號與網路
Hostname: DESKTOP-J2HONGMING

需要和老婆共用一台電腦，新增2組帳號，並從中學習到Windows有分成local account和Microsofit account，此外local account的權限分為系統管理員與標準使用者
- [Windows 11 裡的標準使用者權限有哪些？ : r/Winsides](https://www.reddit.com/r/Winsides/comments/1fxlgq3/what_are_the_standard_user_permissions_in_windows/?tl=zh-hant)
- [你可以設定 Windows 開機時顯示所有使用者，而不是預設登入上次使用的帳戶嗎？ : r/Windows11](https://www.reddit.com/r/Windows11/comments/1gw1jrr/can_you_make_it_so_that_windows_shows_all_users/?tl=zh-hant)
- [How to Show all users on Login Screen in Windows 11? - Technoresult](https://technoresult.com/how-to-show-all-users-on-login-screen-in-windows-11/)
- [【問題】捷徑 釘選 ICON 圖示空白 @電腦應用綜合討論 哈啦板 - 巴哈姆特](https://forum.gamer.com.tw/C.php?bsn=60030&snA=629600)

網路部分，之前都是用無線網路，為了用到家中申請的300 Mbps/300 Mbps，決定接回有線網路，翻出抽屜裡2條塵封已久的網路線，稍微看了一下線上稍微模糊的印刷字: `Cat 5e`

心想:「Cat 5e速率有到1000 Mbps，OK吧」，結果Speed Test開下去，只有100 Mbps，臉都綠了，不死心改用另一條，GoGo，結果還是100 Mbps，臉歪掉了，心理有點忐忑，確認一下另一條線的規格: `Cat 5`，喔喔，那第二次的結果算是合理。可是第一條線的結果和規格不符，想說該不會網路孔有問題吧，但印象中之前驗屋時有測試過，理論上不會那麼快就故障吧， 隔天決定去買一條`Cat 6`測試，結果發現是第一條線的問題
- [為什麼我的 CAT5e 網路線只能跑到 100mbps？ : r/HomeNetworking](https://www.reddit.com/r/HomeNetworking/comments/1axrzc9/why_is_my_cat5e_cable_only_giving_off_100mbps/?tl=zh-hant)


Finally!!
![](speed_test.png)

### 系統備份還原測試
- [【客戶專用】易數一鍵還原：操作說明及注意事項 (2025年10月更新)－歐飛先生｜痞客邦](https://ofeyhong.pixnet.net/blog/post/214511678)
- Ventoy with Clonezilla and spare usb
    - [Ventoy教學：製作能當Linux＆Windows開機碟又當資料碟的USB隨身碟 · Ivon的部落格](https://ivonblog.com/posts/ventoy-linux-installation/)
        - [boot - How to turnoff or reboot at (initramfs) prompts/busybox? - Ask Ubuntu](https://askubuntu.com/questions/1366197/how-to-turnoff-or-reboot-at-initramfs-prompts-busybox)
- Clonezilla
    - [\*\*使用Clonezilla備份還原完整硬碟\*\* - HackMD](https://hackmd.io/@CreeperHua/HyAM9E8RV)
    - [外接裝置備份還原](https://hc.cyc.edu.tw/exe/clonezilla_live/__10.html)
    - - [[SOLVED] Clonezilla stuck on message 'syncing...' - Linux Mint Forums](https://forums.linuxmint.com/viewtopic.php?t=209359)

準備2個64GB的隨身碟。[在Ventoy的隨身碟放了Clonezilla和GParted](https://www.rocksaying.tw/archives/2022/CloneZilla_Gparted_Ventoy.html)，遇到了Ventoy的版本需要更新、[Enroll key](https://www.ventoy.net/cn/doc_secure.html)的議題。
![](ventoy.png)

使用再生龍(Clonezilla)測試了一次系統備份與還原，意外發現了一個無線藍牙鍵盤進BIOS/UEFI的議題，結論是準備一個有線鍵盤或是無線藍牙鍵盤可支援有線模式會比較保險。小提醒，再生龍要先設定target然後再選擇source是需要注意且小心的部分。
![](clonezilla_backup.png)

### 應用程式
- Chrome
    - 登入帳號
- Steam
- 開發
    - vscode
    - WSL
        - https://github.com/j2hongming/information_system
        - https://github.com/j2hongming/j2hongming.github.io
    - Mobaxterm
- Norton
    - [Microsoft Defender 防毒軟體與其他安全性產品的相容性 - Microsoft Defender for Endpoint | Microsoft Learn](https://learn.microsoft.com/zh-tw/defender-endpoint/microsoft-defender-antivirus-compatibility)
    - [【客戶詢問】我想自行安裝其他的防毒軟體，跟Windows內建的防毒會不會有衝突？ (2025年9月更新)－歐飛先生｜痞客邦](https://ofeyhong.pixnet.net/blog/post/223108254)

![](nvidia_5070.png)

### 資料備份策略
主要更新在[Github: information_map](https://github.com/j2hongming/information_system/tree/main/information_map)

- Dropbox
    - [如何設定忽略特定檔案或資料夾](https://help.dropbox.com/zh-tw/sync/ignored-files)
- OneDrive
    - [電腦版 OneDrive App的檔案隨選功能，分不清楚兩種綠色打勾狀態 - Microsoft Q&A](https://learn.microsoft.com/zh-tw/answers/questions/4972792/onedrive-app)
    - [變更 OneDrive 資料夾的位置 - Microsoft 支援服務](https://support.microsoft.com/zh-tw/office/%E8%AE%8A%E6%9B%B4-onedrive-%E8%B3%87%E6%96%99%E5%A4%BE%E7%9A%84%E4%BD%8D%E7%BD%AE-f386fb81-1461-40a7-be2c-712676b2c4ae)
- [Windows 版 iCloud](https://apps.microsoft.com/detail/9pktq5699m62?hl=zh-tw&gl=US)

Dropbox設定忽略特定檔案或資料夾
```
PS C:\Users\j2hongming> Set-Content -Path "D:\Dropbox\個人\娛樂" -Stream com.dropbox.ignored -Value 1
```

j2hongming可以改為自己的帳號或同一台裝置上的另一個帳號

- D:\Dropbox\個人
- D:\Dropbox\工作
- D:\OneDrive\j2hongming\回憶紀念
- D:\j2hongming\Pictures\iCloud Photos\Photos
- D:\j2hongming\Documents\iCloudDrive

## 總結
使用上很順暢，2077也可以特效全開，愉悅。預計使用8-10年，2025/10-2035/10