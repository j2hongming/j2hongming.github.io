---
title: 虛擬機器時間飄移造成openshift安裝異常
comments: true
date: 2025-03-28 05:44:31
description:
categories: software_development
tags:
- virtual_machine
- esxi
- openshift
- clock
---

使用三台虛擬機器和兩台裸機(bare metal)安裝openshift 4.17時，出現下列的log

> updated status from known to insufficient (Host cannot be installed due to following failing validation(s): Host clock is not synchronized, service time is ahead of host's at least for 20.0 minutes, please configure an NTP server via DHCP. Service time: 2025-03-28 03:29:28.867434383 +0000 UTC ; Host couldn't synchronize with any NTP server)


透過ssh登入其中一台虛擬機器檢查，發現系統時間比當前時間還要快
``` bash
sudo hwclock -v
```

進一步確認ESXi Host的時間設定，發現和虛擬機器一樣，有時間較快的狀況
``` bash
esxcli hardware clock get
```

確認後，決定使用NTP服務修正ESXi Host的時間
![ESXi Config NTP](esxi_config_ntp.png)

![ESXi Start NTP](esxi_start_ntp.png)

並在該虛擬機器的設定中，開啟主客體時間同步的設定
![ESXi Config VM](esxi_config_vm.png)