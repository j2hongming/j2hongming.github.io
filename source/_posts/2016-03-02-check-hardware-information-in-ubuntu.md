---
layout: post
title: "Check Hardware Information in Ubuntu"
date: 2016-03-02 16:17:19 +0800
comments: true
categories: software_development
tags:
- linux
- ubuntu
- command
- hardware 
---

- CPU
- RAM
- HD
- MAC Adress
<!-- more -->

## CPU
    lscpu
    # Architecture:          x86_64
    # CPU op-mode(s):        32-bit, 64-bit
    # Byte Order:            Little Endian
    # ...
    
    cat /proc/cpuinfo
    # processor       : 0
    # vendor_id       : GenuineIntel
    # cpu family      : 6
    # model           : 37
    # model name      : Intel(R) Xeon(R) CPU E5-2670 0 @ 2.60GHz
    # ...

- [8 commands to check cpu information on Linux](http://www.binarytides.com/linux-cpu-information/)
- [Ubuntu: Find CPU Information / Speed](http://www.cyberciti.biz/faq/ubuntu-cpu-information/)
- [How to check processor and cpu details on Linux](http://www.binarytides.com/linux-check-processor/)

## RAM
### 可用記憶體大小
    free -m

### 詳細資料
    cat /proc/meminfo

### 時脈和DDR
    sudo dmidecode --type 17

- [HowTo: Check RAM Size In Ubuntu Linux](http://www.cyberciti.biz/faq/check-ram-in-ubuntu/)
- [Find Linux RAM Information Command](http://www.cyberciti.biz/faq/linux-ram-info-command/)

## Hard Drive
### Check Partitions
    fdisk -l

    df

### Lists out all the storage blocks
    lsblk

    hwinfo

### Other
    ls /dev/disk/by-id

    cat /sys/block/sda/device/model

- [Tech Tip: Retrieve Disk Info from the Command Line | Linux Journal](http://www.linuxjournal.com/content/tech-tip-retrieve-disk-info-command-line)
- [9 commands to check hard disk partitions and disk space on Linux](http://www.binarytides.com/linux-command-check-disk-partitions/)

## MAC Adress
    ifconfig -a
