---
title: Hype V網路異常行為
comments: true
date: 2025-04-29 15:45:58
description:
categories: software_development
tags:
- hype-v
- network
- firewall
---

設定好共用並檢查eth0有拿到ip

![hype_v_network](hype_v_network.png)

```
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host 
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 00:15:5d:00:8b:11 brd ff:ff:ff:ff:ff:ff
    inet 192.168.137.129/24 metric 100 brd 192.168.137.255 scope global dynamic eth0
       valid_lft 603399sec preferred_lft 603399sec
    inet6 fe80::215:5dff:fe00:8b11/64 scope link 
       valid_lft forever preferred_lft forever
```

檢查`ping 8.8.8.8`和`ping www.google.com`可以通，但使用`curl -v www.google.com`或`sudo apt update`會失敗

ping gateway不通...

感覺是防火牆的問題，看了一下防毒軟體的紀錄有被封鎖的樣子，最後將`vEthernet (Internal vSwitch) #1`
類型改為`私人`即可

![firewall_log](firewall_log.png)

![firewall_config](firewall_config.png)