---
title: ssh connection pending
comments: true
date: 2025-03-04 04:15:48
description:
categories: software_development
tags:
- ssh
---

紀錄使用ssh連線時hang住的議題

## MaxStartups in sshd_config
參考[3410 – Since 8.9p1 MaxStartups >=1024, in sshd\_config, causes "error: ppoll: Invalid argument"](https://bugzilla.mindrot.org/show_bug.cgi?id=3410)

若在8.9p1的`/etc/ssh/sshd_config`，MaxStartups設定大於等於1024時。ssh client連線時會hang住，剛好Ubuntu 22.04所使用的版本是`OpenSSH_8.9p1 Ubuntu-3ubuntu0.11, OpenSSL 3.0.2 15 Mar 2022`

會碰到這個問題的情境是使用xCAT安裝Ubuntu 22.04，安裝完成後發現這個現象，可能是因為這個[設定](https://github.com/xcat2/xcat-core/blob/7cc8f8b9794f1228a38443f3f926ad0c075c1265/xCAT/postscripts/remoteshell#L65)
