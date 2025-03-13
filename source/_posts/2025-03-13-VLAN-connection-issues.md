---
title: 從VLAN不通的問題反思UX的價值
comments: true
date: 2025-03-13 02:46:24
description:
categories: software_development
tags:
- vlan
---

遇到虛擬機和實體機VLAN不通的問題，花了一些時間測試和找問題
- 確認Hypervisor的網路VLAN ID並重新綁定虛擬機網卡
- 不透過DHCP分派IP，直接設定Static IP互相ping

最後被告知是Switch上的port settings上有設定正確的VLAN ID但是實際上該VLAN ID並沒有被定義在Switch的設定內。
檢查了一下Swtich的介面，設定port的VLAN ID是使用Text field，所以即使是不存在的VLAN ID也可以被設定...

反思這邊的UX若改為"只有已被定義的VLAN之下拉式選單"，就可以不用花那麼多時間去找問題了QQ