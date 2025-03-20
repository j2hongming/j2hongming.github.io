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
2. BMC FRU/DMI的值為空(Manufacturer, Serial Number, Part Number)
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

### BMC FRU/DMI的值為空

處理方式: 使用各家廠商自己的工具調整BMC FRU的值(Manufacturer, Serial Number, Part Number)，有時候連DMI都要一起調整

以下為追查DMI的議題的脈絡:

利用IPMI Tool確認`ipmitool fru print`，結果有值，發現只改FRU無效

在`/var/log/xcat/cluster.log`發現以下log
log
```
Warning: Could not find any node for $mtms using mtms-based discovery
```

查到該log是從[/opt/xcat/lib/perl/xCAT_plugin/typemtms.pm](https://github.com/xcat2/xcat-core/blob/master/xCAT-server/lib/xcat/plugins/typemtms.pm)而來，找到相關變數$mtms並確認serial為空

``` perl
my $mtms       = $request->{'mtm'}->[0] . "*" . $request->{'serial'}->[0];
```

知道MTMS discovery是透過gensis image完成該行為，檢查[dodiscovery](https://github.com/xcat2/xcat-core/blob/7cc8f8b9794f1228a38443f3f926ad0c075c1265/xCAT-genesis-scripts/usr/bin/dodiscovery#L106)中serial是如何取得，檢查已載入gensis image的目標節點，利用BMC Console確認`/sys/devices/virtual/dmi/id/product_serial`的值確實為空


``` perl
SERIAL=`cat /sys/devices/virtual/dmi/id/product_serial`
```

### ipmitool搭配lanplus選項造成連線失敗

處理方式: {% post_link ipmitool-issue-about-rcmp-plus-cipher-suite %}