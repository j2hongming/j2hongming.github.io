---
title: 梳理所知的auto discovery
comments: true
date: 2025-02-05 07:40:21
description:
categories: software_development
tags:
- discovery
- xcat
- foreman
- maas
---

目前已知三種:
- [xCAT MTMS discovery](https://xcat-docs.readthedocs.io/en/stable/guides/admin-guides/manage_clusters/ppc64le/discovery/mtms/index.html)
- [Canonical MAAS Enlistment - automatic discovery or network discovery](https://maas.io/docs/about-the-machine-life-cycle#p-17317-enlistment)
- [Foreman Discovery](https://theforeman.org/plugins/foreman_discovery/14.0/index.html)

請LLM幫忙分析的[結果](https://chatgpt.com/share/67a31951-e3a0-8009-a348-eaff5c378db0)

看起來必要條件有幾個: 
1. PXE環境(DHCP+TFTP)
2. 機器需要設定為network boot
3. lightweight bootable image，這個image需要以某種方式將硬體資訊回傳至負責的Service(xCAT, MAAS, Foreman)，在xCAT內被稱作genesis image，在Foreman被稱為Discovery image

xCAT所使用的程式主要是這一個[bmcdiscover](https://github.com/xcat2/xcat-core/blob/f7e389a0c03fb18f8f1236cb4ad3fe8605765c51/xCAT-server/lib/xcat/plugins/bmcdiscover.pm#L619)，scan_process這個函式內提到了兩個工具:nmap和ipmitool-xcat，nmap看起來是用來取得live_ip，ipmitool-xcat用來取得BMC的`mc info`

大致操作流程如下
``` bash
bmcdiscover --range 192.168.62.85-87 -u foo -p bar -z -w
bmcdiscover --range 192.168.62.85-87 -u foo -p bar -z > predefined.stanzas
# edit the predefined.stanzas: change the node name and add the provision ip
cat predefined.stanzas | mkdef -z
nodels
# node-chiikawa-usagi-8888sg-s423750x1408652
# node-chiikawa-usagi-8888sg-s423750x1408664
# node85
# node87
makehosts node85
makehosts node87
rsetboot node-chiikawa-usagi-8888sg-s423750x1408652 net -u
rpower node-chiikawa-usagi-8888sg-s423750x1408652 reset
rsetboot node-chiikawa-usagi-8888sg-s423750x1408664 net -u
rpower node-chiikawa-usagi-8888sg-s423750x1408664 reset
```

MAAS和Foreman沒有用過，就不細究了