---
title: docker and podman in the same host
comments: true
date: 2025-04-02 05:20:48
description:
categories: software_development
tags:
- docker
- podman
- ip_table
---

最近遇到一個特別的環境，需要在同一個Host上使用docker和podman，以下紀錄遇到的議題

## 環境(Environment)
- Host OS: Redhat 9.3
- podman 4.6.1
- docker

## 議題(Issue)
在已安裝docker的機器上部屬Quay Server，發現在同一個網段的其他機器無法存取到Quay

## 解決方案(Workaround)

修改設定`ip-forward-no-drop`並重啟docker daemon

> To stop Docker from setting the FORWARD chain's policy to DROP, include "ip-forward-no-drop": true in /etc/docker/daemon.json, or add option --ip-forward-no-drop to the dockerd command line.

## 臨時解決方案(Workaround)

``` bash
sudo podman network reload --all
sudo iptables -I FORWARD 1 -o podman0 -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT
sudo iptables -I FORWARD 2 -o podman0 -j ACCEPT
sudo iptables -I FORWARD 3 -i podman0 ! -o podman0 -j ACCEPT
sudo iptables -I FORWARD 4 -i podman0 -o podman0 -j ACCEPT
```

## 問題根源(Root cause)

docker將iptables中的`FORWARD CHANIN`設定為`DROP`

## 參考
- [Packet filtering and firewalls | Docker Docs](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-on-a-router)