---
layout: post
title: "Config Static IP in Ubuntu"
date: 2016-03-02 16:48:33 +0800
comments: true
categories: 
- linux
- ubuntu
- command
- network
---

- 設定network interface
- 重新讀取網路設定
<!-- more -->

## 設定network interface
    $ vim /etc/network/interfaces
    # 加上下面IP設定(address, netmask, gateway要看當時環境而定)
    iface eth0 inet static
    address 192.168.7.151
    netmask 255.255.255.0
    gateway 192.168.7.1


## 重新讀取網路設定
    $ sudo /etc/init.d/networking restart

- [凍仁的筆記: Ubuntu 網路設定 - 固定 IP](http://note.drx.tw/2008/02/ubuntu-ip.html)
- [Ubuntu 如何設定固定 IP ( 設定網路 )](http://www.arthurtoday.com/2010/08/ubuntu-ip.html)
