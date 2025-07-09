---
title: VMWare的VM遇到硬碟空間不足
comments: true
date: 2025-07-09 06:15:39
description:
categories: software_development
tags:
- disk
- vm
- vmware
- lvm
---

發現VMWare的VM遇到硬碟空間不足，紀錄一下擴充的步驟

- VMware VM
- Guest OS use the LVM

## 增加虛擬機硬碟容量

注意虛擬機需要先關機且不能有snapshot

若有snapshot時，會看到以下錯誤訊息

> Disks that belong to virtual machines with snapshots cannot be expanded. To expand this disk, first remove snapshots.

## 增加Partition, LVM和Filesystem的容量

參考[這一篇](https://blog.jks.coffee/linux-lvm-disk-extend-expand-redhat/)，寫得十分詳細且附圖

### Partition

從84.2GB到106GB

``` bash
[root@foo ~]# parted
GNU Parted 3.5
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) print
Model: VMware Virtual disk (scsi)
Disk /dev/sda: 107GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name                  Flags
 1      1049kB  630MB   629MB   fat32        EFI System Partition  boot, esp
 2      630MB   1704MB  1074MB  xfs
 3      1704MB  85.9GB  84.2GB                                     lvm

(parted) resizepart 3 100%
(parted) print
Model: VMware Virtual disk (scsi)
Disk /dev/sda: 107GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name                  Flags
 1      1049kB  630MB   629MB   fat32        EFI System Partition  boot, esp
 2      630MB   1704MB  1074MB  xfs
 3      1704MB  107GB   106GB                                      lvm

(parted) quit
Information: You may need to update /etc/fstab.

[root@foo ~]#
```

### LVM - Physical Volume, Logical Volume

Physical Volume
新增後可以看到Free PE數量從0到5120

``` bash
[root@foo ~]# pvdisplay -v
  --- Physical volume ---
  PV Name               /dev/sda3
  VG Name               vg_root
  PV Size               78.41 GiB / not usable 2.00 MiB
  Allocatable           yes (but full)
  PE Size               4.00 MiB
  Total PE              20073
  Free PE               0
  Allocated PE          20073
  PV UUID               Qnf8NM-g5Qe-zGLr-tGkG-hD1N-nIZ1-EqpbBl

[root@foo ~]# pvresize /dev/sda3
  Physical volume "/dev/sda3" changed
  1 physical volume(s) resized or updated / 0 physical volume(s) not resized
[root@foo ~]# pvdisplay -v
  --- Physical volume ---
  PV Name               /dev/sda3
  VG Name               vg_root
  PV Size               98.41 GiB / not usable 1.98 MiB
  Allocatable           yes
  PE Size               4.00 MiB
  Total PE              25193
  Free PE               5120
  Allocated PE          20073
  PV UUID               Qnf8NM-g5Qe-zGLr-tGkG-hD1N-nIZ1-EqpbBl

[root@foo ~]#
```

Logical Volume
想要增加Logical Volume(/dev/vg_root/lv_root)的容量，新增後可以看到Free  PE / Size從20.00 GiB變成10.00 GiB，原因是使用+50%FREE的設定，之後若有需求還可以直接用剩下的50%，不需再從partition開始處理

注意`/`還是37GB
> /dev/mapper/vg_root-lv_root xfs        37G   37G  283M 100% /

``` bash
[root@foo ~]# vgdisplay -v
  --- Volume group ---
  VG Name               vg_root
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  6
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                4
  Open LV               4
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               98.41 GiB
  PE Size               4.00 MiB
  Total PE              25193
  Alloc PE / Size       20073 / 78.41 GiB
  Free  PE / Size       5120 / 20.00 GiB
  VG UUID               BnvIou-XqN8-sc92-49H9-xxQr-GSWR-Q9Fh3q

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_swap
  LV Name                lv_swap
  VG Name                vg_root
  LV UUID                IqhY2J-cOGY-JVvo-Veoh-zgh8-Grfk-xIDedM
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:17 -0500
  LV Status              available
  # open                 2
  LV Size                2.00 GiB
  Current LE             512
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_tmp
  LV Name                lv_tmp
  VG Name                vg_root
  LV UUID                K30WD7-Sfzh-Ltzy-jSzz-cQ2K-xSjR-vn8OKn
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:17 -0500
  LV Status              available
  # open                 1
  LV Size                30.00 GiB
  Current LE             7680
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_home
  LV Name                lv_home
  VG Name                vg_root
  LV UUID                gKGzVT-9494-yDce-3aPX-Gr00-aYEb-I4dIiC
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:18 -0500
  LV Status              available
  # open                 1
  LV Size                10.00 GiB
  Current LE             2560
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:3

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_root
  LV Name                lv_root
  VG Name                vg_root
  LV UUID                2jqRPu-YCdK-wOMD-fTGe-3vlO-fBYm-5DcZGI
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:18 -0500
  LV Status              available
  # open                 1
  LV Size                36.41 GiB
  Current LE             9321
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0

  --- Physical volumes ---
  PV Name               /dev/sda3
  PV UUID               Qnf8NM-g5Qe-zGLr-tGkG-hD1N-nIZ1-EqpbBl
  PV Status             allocatable
  Total PE / Free PE    25193 / 5120

[root@foo ~]# lvextend -l +50%FREE /dev/vg_root/lv_root
  Size of logical volume vg_root/lv_root changed from 36.41 GiB (9321 extents) to 46.41 GiB (11881 extents).
  Logical volume vg_root/lv_root successfully resized.
[root@foo ~]# vgdisplay -v
  --- Volume group ---
  VG Name               vg_root
  System ID
  Format                lvm2
  Metadata Areas        1
  Metadata Sequence No  7
  VG Access             read/write
  VG Status             resizable
  MAX LV                0
  Cur LV                4
  Open LV               4
  Max PV                0
  Cur PV                1
  Act PV                1
  VG Size               98.41 GiB
  PE Size               4.00 MiB
  Total PE              25193
  Alloc PE / Size       22633 / 88.41 GiB
  Free  PE / Size       2560 / 10.00 GiB
  VG UUID               BnvIou-XqN8-sc92-49H9-xxQr-GSWR-Q9Fh3q

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_swap
  LV Name                lv_swap
  VG Name                vg_root
  LV UUID                IqhY2J-cOGY-JVvo-Veoh-zgh8-Grfk-xIDedM
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:17 -0500
  LV Status              available
  # open                 2
  LV Size                2.00 GiB
  Current LE             512
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_tmp
  LV Name                lv_tmp
  VG Name                vg_root
  LV UUID                K30WD7-Sfzh-Ltzy-jSzz-cQ2K-xSjR-vn8OKn
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:17 -0500
  LV Status              available
  # open                 1
  LV Size                30.00 GiB
  Current LE             7680
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_home
  LV Name                lv_home
  VG Name                vg_root
  LV UUID                gKGzVT-9494-yDce-3aPX-Gr00-aYEb-I4dIiC
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:18 -0500
  LV Status              available
  # open                 1
  LV Size                10.00 GiB
  Current LE             2560
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:3

  --- Logical volume ---
  LV Path                /dev/vg_root/lv_root
  LV Name                lv_root
  VG Name                vg_root
  LV UUID                2jqRPu-YCdK-wOMD-fTGe-3vlO-fBYm-5DcZGI
  LV Write Access        read/write
  LV Creation host, time us-elmerh-nb.bar.com, 2024-12-25 23:58:18 -0500
  LV Status              available
  # open                 1
  LV Size                46.41 GiB
  Current LE             11881
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0

  --- Physical volumes ---
  PV Name               /dev/sda3
  PV UUID               Qnf8NM-g5Qe-zGLr-tGkG-hD1N-nIZ1-EqpbBl
  PV Status             allocatable
  Total PE / Free PE    25193 / 2560

[root@bar ~]# df -hT
Filesystem                  Type      Size  Used Avail Use% Mounted on
devtmpfs                    devtmpfs  4.0M     0  4.0M   0% /dev
tmpfs                       tmpfs     7.7G   84K  7.7G   1% /dev/shm
tmpfs                       tmpfs     3.1G   14M  3.1G   1% /run
efivarfs                    efivarfs  256K   28K  224K  11% /sys/firmware/efi/efivars
/dev/mapper/vg_root-lv_root xfs        37G   37G  283M 100% /
/dev/mapper/vg_root-lv_tmp  xfs        30G  4.7G   26G  16% /tmp
/dev/sda2                   xfs       960M  347M  614M  37% /boot
/dev/sda1                   vfat      599M  7.1M  592M   2% /boot/efi
/dev/mapper/vg_root-lv_home xfs        10G  6.4G  3.6G  65% /home
shm                         tmpfs      63M  336K   63M   1% /var/lib/containers/storage/overlay-containers/c6f86549ddc0cc3d3b7a7806afa72b8c870127a0d04c5e34b49b5e4f23717134/userdata/shm
overlay                     overlay    37G   37G  283M 100% /var/lib/containers/storage/overlay/86af4839a4f8284ed47884d8a36db2643858cc0b2d02146b9634805d223be178/merged
overlay                     overlay    37G   37G  283M 100% /var/lib/containers/storage/overlay/2f7ab5db365f8310894e5f26b340a536fafb4b9d3c220fd8e959564880cd2cdb/merged
overlay                     overlay    37G   37G  283M 100% /var/lib/containers/storage/overlay/ba39df3b093f81c42630ebced664f7454612b41529fe76e0c8c5a4b1943aab0a/merged
tmpfs                       tmpfs     1.6G  104K  1.6G   1% /run/user/1000
[root@foo ~]#
```

### Filesystem - XFS

針對xfs增加，完成後變成47G
> /dev/mapper/vg_root-lv_root xfs        47G   37G   11G  78% /

``` bash
[root@foo ~]# xfs_growfs /dev/vg_root/lv_root
meta-data=/dev/mapper/vg_root-lv_root isize=512    agcount=4, agsize=2386176 blks
         =                       sectsz=512   attr=2, projid32bit=1
         =                       crc=1        finobt=1, sparse=1, rmapbt=0
         =                       reflink=1    bigtime=1 inobtcount=1 nrext64=0
data     =                       bsize=4096   blocks=9544704, imaxpct=25
         =                       sunit=0      swidth=0 blks
naming   =version 2              bsize=4096   ascii-ci=0, ftype=1
log      =internal log           bsize=4096   blocks=16384, version=2
         =                       sectsz=512   sunit=0 blks, lazy-count=1
realtime =none                   extsz=4096   blocks=0, rtextents=0
data blocks changed from 9544704 to 12166144
[root@foo ~]# df -hT
Filesystem                  Type      Size  Used Avail Use% Mounted on
devtmpfs                    devtmpfs  4.0M     0  4.0M   0% /dev
tmpfs                       tmpfs     7.7G   84K  7.7G   1% /dev/shm
tmpfs                       tmpfs     3.1G   14M  3.1G   1% /run
efivarfs                    efivarfs  256K   28K  224K  11% /sys/firmware/efi/efivars
/dev/mapper/vg_root-lv_root xfs        47G   37G   11G  78% /
/dev/mapper/vg_root-lv_tmp  xfs        30G  4.7G   26G  16% /tmp
/dev/sda2                   xfs       960M  347M  614M  37% /boot
/dev/sda1                   vfat      599M  7.1M  592M   2% /boot/efi
/dev/mapper/vg_root-lv_home xfs        10G  6.4G  3.6G  65% /home
shm                         tmpfs      63M  336K   63M   1% /var/lib/containers/storage/overlay-containers/c6f86549ddc0cc3d3b7a7806afa72b8c870127a0d04c5e34b49b5e4f23717134/userdata/shm
overlay                     overlay    47G   37G   11G  78% /var/lib/containers/storage/overlay/86af4839a4f8284ed47884d8a36db2643858cc0b2d02146b9634805d223be178/merged
overlay                     overlay    47G   37G   11G  78% /var/lib/containers/storage/overlay/2f7ab5db365f8310894e5f26b340a536fafb4b9d3c220fd8e959564880cd2cdb/merged
overlay                     overlay    47G   37G   11G  78% /var/lib/containers/storage/overlay/ba39df3b093f81c42630ebced664f7454612b41529fe76e0c8c5a4b1943aab0a/merged
tmpfs                       tmpfs     1.6G  104K  1.6G   1% /run/user/1000
[root@foo ~]# 
```