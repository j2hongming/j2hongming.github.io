---
title: xCAT MTMS discovery常見問題
comments: true
date: 2025-02-20 06:13:24
description:
categories: software_development
tags:
- discovery
- xcat
---

目前遇過以下幾種:
1. gensis image缺少網卡驅動
2. BMC FRU的值為空(Manufacturer, Serial Number, Part Number)
3. ipmitool搭配lanplus選項造成連線失敗

### gensis image缺少網卡驅動
![xcat_mtms_discovery_gensis_image](xcat_mtms_discovery_gensis_image.png)

處理方式: 重新build一個包含相對應網卡驅動的gensis image

以下指令的測試環境為Redhat 9.3
``` bash
cd /tmp
git clone -b master https://github.com/xcat2/xcat-core.git
cd /tmp/xcat-core/xCAT-genesis-builder
# chnage the xcat-cmdline.sh, add all drivers
# Before:
# for line in `cat /lib/modules/$KERVER/modules.dep |grep -vE 'tunnel|ieee|ifb|bond|dummy|fjes|hv_netvsc|ntb_netdev|xen-netfront|hdlc_fr|dlci'| awk -F: '{print \$1}' | sed -e "s/\(.*\)\.ko.*/\1/"`; do
# After:
# for line in `cat /lib/modules/$KERVER/modules.dep | awk -F: '{print \$1}' | sed -e "s/\(.*\)\.ko.*/\1/"`; do

# for missing packages
dnf install dhclient rng-tools device-mapper
grep -irn '/lib/udev/rules.d/69-dm-lvm*' /tmp/xcat-core/xCAT-genesis-builder/install
# replace /lib/udev/rules.d/69-dm-lvm-metad.rules into /lib/udev/rules.d/69-dm-lvm.rules in the /tmp/xcat-core/xCAT-genesis-builder/install

# build the rpm
rm -rf /root/rpmbuild
./buildrpm

# remove the origin genesis-base and install the latest built genesis-base
rpm -qa | grep 'xCAT-genesis-base-x86_64'
rpm -e --nodeps $(rpm -qa | grep 'xCAT-genesis-base-x86_64')
cd /root/rpmbuild/RPMS/noarch
rpm -ivh xCAT-genesis-base*.rpm

# build the gensis image with suitable nic drivers
mknb x86_64
```

### BMC FRU的值為空

處理方式: 使用各家廠商自己的工具調整BMC FRU的值(Manufacturer, Serial Number, Part Number)

### ipmitool搭配lanplus選項造成連線失敗

處理方式: {% post_link ipmitool-issue-about-rcmp-plus-cipher-suite %}