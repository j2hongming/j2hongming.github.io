---
title: 從source安裝python並記錄遇到的問題
comments: true
date: 2021-08-26 23:55:58
description: 相依和空間不足問題
categories: software_development
tags:
- python
---
安裝pip和virtualenv
```bash=
sudo apt update
curl -o get-pip.py https://bootstrap.pypa.io/get-pip.py 
python3 get-pip.py --user
sudo apt install virtualenv

# Ubuntu 16.04(default python 3.5)
sudo apt update
curl -O https://bootstrap.pypa.io/pip/3.5/get-pip.py
python3 get-pip.py --user
sudo apt install virtualenv
```

從source安裝python3.7
```bash=
sudo apt update
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget
ver=3.7.10
ver_under_score=$(echo $ver | sed -e 's/\./_/g')
tmp_build_dir=/tmp/${ver_under_score}
mkdir ${tmp_build_dir} && cd ${tmp_build_dir}
wget https://www.python.org/ftp/python/${ver}/Python-${ver}.tar.xz
tar xvf Python-${ver}.tar.xz -C ${tmp_build_dir}
cd ${tmp_build_dir}/Python-${ver}/
./configure --enable-optimizations
sudo make altinstall
```

將原本的python3換成python3.7
```bash=
python3 -V
update-alternatives --install /usr/bin/python3 python3 /usr/local/bin/python3.7 1
python3 -V
```

## 參考
- [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html)
- [Ubuntu 16.04 更新 Python 3.7](https://medium.com/k2shouai/ubuntu-16-04-%E6%9B%B4%E6%96%B0-python-3-7-f08cee97a64b)
- [How to set Python3.5.2 as default Python version on CentOS](https://stackoverflow.com/questions/45542690/how-to-set-python3-5-2-as-default-python-version-on-centos)
- [pip is showing error 'lsb_release -a' returned non-zero exit status 1](https://stackoverflow.com/questions/44967202/pip-is-showing-error-lsb-release-a-returned-non-zero-exit-status-1)

## zlib1g-dev相依問題
出現linux-headers相依性問題, 看起來是linux-headers-4.4.0-169-generic尚未被安裝, 使用`uname -r` 確認目前版本並透過`ls -la /usr/src/`確認已下載的檔案, 最後利用系統提示的`sudo apt-get -f install`重新安裝linux-headers

```
$ sudo apt-get install -y zlib1g-dev
Reading package lists... Done
Building dependency tree
Reading state information... Done
You might want to run 'apt-get -f install' to correct these:
The following packages have unmet dependencies:
 linux-headers-generic : Depends: linux-headers-4.4.0-169-generic but it is not going to be installed
 zlib1g-dev : Depends: zlib1g (= 1:1.2.8.dfsg-2ubuntu4.3) but 1:1.2.8.dfsg-2ubuntu4 is to be installed

$ uname -r
4.4.0-166-generic

$ ls -la /usr/src/
total 132
drwxr-xr-x 33 root root 4096 Nov 13  2019 .
drwxr-xr-x 10 root root 4096 Feb 21  2017 ..
drwxr-xr-x 27 root root 4096 Dec 10  2018 linux-headers-4.4.0-140
drwxr-xr-x  7 root root 4096 Dec 10  2018 linux-headers-4.4.0-140-generic
drwxr-xr-x 27 root root 4096 Dec 21  2018 linux-headers-4.4.0-141
drwxr-xr-x  7 root root 4096 Dec 21  2018 linux-headers-4.4.0-141-generic
drwxr-xr-x 27 root root 4096 Feb  4  2019 linux-headers-4.4.0-142
drwxr-xr-x  7 root root 4096 Feb  4  2019 linux-headers-4.4.0-142-generic
drwxr-xr-x 27 root root 4096 Mar 15  2019 linux-headers-4.4.0-143
drwxr-xr-x  7 root root 4096 Mar 15  2019 linux-headers-4.4.0-143-generic
drwxr-xr-x 27 root root 4096 Apr  3  2019 linux-headers-4.4.0-145
drwxr-xr-x  7 root root 4096 Apr  3  2019 linux-headers-4.4.0-145-generic
drwxr-xr-x 27 root root 4096 May 16  2019 linux-headers-4.4.0-148
drwxr-xr-x  7 root root 4096 May 16  2019 linux-headers-4.4.0-148-generic
drwxr-xr-x 27 root root 4096 Jun  6  2019 linux-headers-4.4.0-150
drwxr-xr-x  7 root root 4096 Jun  6  2019 linux-headers-4.4.0-150-generic
drwxr-xr-x 27 root root 4096 Jun 20  2019 linux-headers-4.4.0-151
drwxr-xr-x  7 root root 4096 Jun 20  2019 linux-headers-4.4.0-151-generic
drwxr-xr-x 27 root root 4096 Jun 29  2019 linux-headers-4.4.0-154
drwxr-xr-x  7 root root 4096 Jun 29  2019 linux-headers-4.4.0-154-generic
drwxr-xr-x 27 root root 4096 Jul 25  2019 linux-headers-4.4.0-157
drwxr-xr-x  7 root root 4096 Jul 25  2019 linux-headers-4.4.0-157-generic
drwxr-xr-x 27 root root 4096 Aug 14  2019 linux-headers-4.4.0-159
drwxr-xr-x  7 root root 4096 Aug 14  2019 linux-headers-4.4.0-159-generic
drwxr-xr-x 27 root root 4096 Sep  4  2019 linux-headers-4.4.0-161
drwxr-xr-x  7 root root 4096 Sep  4  2019 linux-headers-4.4.0-161-generic
drwxr-xr-x 27 root root 4096 Sep 18  2019 linux-headers-4.4.0-164
drwxr-xr-x  7 root root 4096 Sep 18  2019 linux-headers-4.4.0-164-generic
drwxr-xr-x 27 root root 4096 Oct  2  2019 linux-headers-4.4.0-165
drwxr-xr-x  7 root root 4096 Oct  2  2019 linux-headers-4.4.0-165-generic
drwxr-xr-x 27 root root 4096 Oct 22  2019 linux-headers-4.4.0-166
drwxr-xr-x  7 root root 4096 Oct 22  2019 linux-headers-4.4.0-166-generic
drwxr-xr-x 27 root root 4096 Nov 13  2019 linux-headers-4.4.0-169
```

> sudo apt-get -f install

```
$ sudo apt-get -f install
Reading package lists... Done
Building dependency tree
Reading state information... Done
Correcting dependencies... Done
The following packages were automatically installed and are no longer required:
  linux-headers-4.4.0-140 linux-headers-4.4.0-140-generic linux-headers-4.4.0-141 linux-headers-4.4.0-141-generic linux-headers-4.4.0-142 linux-headers-4.4.0-142-generic
  linux-headers-4.4.0-143 linux-headers-4.4.0-143-generic linux-headers-4.4.0-145 linux-headers-4.4.0-145-generic linux-headers-4.4.0-148 linux-headers-4.4.0-148-generic
  linux-headers-4.4.0-150 linux-headers-4.4.0-150-generic linux-headers-4.4.0-151 linux-headers-4.4.0-151-generic linux-headers-4.4.0-154 linux-headers-4.4.0-154-generic
  linux-headers-4.4.0-157 linux-headers-4.4.0-157-generic linux-headers-4.4.0-159 linux-headers-4.4.0-159-generic linux-headers-4.4.0-161 linux-headers-4.4.0-161-generic
  linux-headers-4.4.0-164 linux-headers-4.4.0-164-generic linux-headers-4.4.0-169 linux-headers-4.4.0-64 linux-headers-4.4.0-64-generic linux-headers-4.4.0-66
  linux-headers-4.4.0-66-generic linux-headers-4.4.0-70 linux-headers-4.4.0-70-generic linux-headers-4.4.0-71 linux-headers-4.4.0-71-generic linux-headers-4.4.0-72
  linux-headers-4.4.0-72-generic linux-headers-4.4.0-75 linux-headers-4.4.0-75-generic linux-headers-4.4.0-78 linux-headers-4.4.0-78-generic linux-headers-4.4.0-79
  linux-headers-4.4.0-79-generic linux-headers-4.4.0-81 linux-headers-4.4.0-81-generic linux-headers-4.4.0-83 linux-headers-4.4.0-83-generic linux-headers-4.4.0-87
  linux-headers-4.4.0-87-generic linux-headers-4.4.0-89 linux-headers-4.4.0-89-generic linux-headers-4.4.0-91 linux-headers-4.4.0-91-generic linux-headers-4.4.0-92
  linux-headers-4.4.0-92-generic linux-headers-4.4.0-93 linux-headers-4.4.0-93-generic linux-headers-4.4.0-97 linux-image-4.4.0-140-generic linux-image-4.4.0-141-generic
  linux-image-4.4.0-142-generic linux-image-4.4.0-143-generic linux-image-4.4.0-145-generic linux-image-4.4.0-148-generic linux-image-4.4.0-150-generic
  linux-image-4.4.0-151-generic linux-image-4.4.0-154-generic linux-image-4.4.0-157-generic linux-image-4.4.0-159-generic linux-image-4.4.0-161-generic
  linux-image-4.4.0-164-generic linux-image-4.4.0-169-generic linux-image-4.4.0-64-generic linux-image-4.4.0-66-generic linux-image-4.4.0-70-generic linux-image-4.4.0-71-generic
  linux-image-4.4.0-72-generic linux-image-4.4.0-75-generic linux-image-4.4.0-78-generic linux-image-4.4.0-79-generic linux-image-4.4.0-81-generic linux-image-4.4.0-83-generic
  linux-image-4.4.0-87-generic linux-image-4.4.0-89-generic linux-image-4.4.0-91-generic linux-image-4.4.0-92-generic linux-image-4.4.0-93-generic linux-modules-4.4.0-143-generic
  linux-modules-4.4.0-145-generic linux-modules-4.4.0-148-generic linux-modules-4.4.0-150-generic linux-modules-4.4.0-151-generic linux-modules-4.4.0-154-generic
  linux-modules-4.4.0-157-generic linux-modules-4.4.0-159-generic linux-modules-4.4.0-161-generic linux-modules-4.4.0-164-generic linux-modules-4.4.0-169-generic
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  linux-headers-4.4.0-210 linux-headers-4.4.0-210-generic linux-headers-generic linux-headers-virtual linux-image-4.4.0-210-generic linux-image-virtual
  linux-modules-4.4.0-210-generic linux-virtual
Suggested packages:
  fdutils linux-doc-4.4.0 | linux-source-4.4.0 linux-tools
The following NEW packages will be installed:
  linux-headers-4.4.0-210 linux-headers-4.4.0-210-generic linux-image-4.4.0-210-generic linux-modules-4.4.0-210-generic
The following packages will be upgraded:
  linux-headers-generic linux-headers-virtual linux-image-virtual linux-virtual
4 upgraded, 4 newly installed, 0 to remove and 243 not upgraded.
9 not fully installed or removed.
Need to get 29.8 MB of archives.
After this operation, 147 MB of additional disk space will be used.
Do you want to continue? [Y/n] Y
Get:1 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-modules-4.4.0-210-generic amd64 4.4.0-210.242 [12.1 MB]
Get:2 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-image-4.4.0-210-generic amd64 4.4.0-210.242 [6,954 kB]
Get:3 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-virtual amd64 4.4.0.210.216 [1,780 B]
Get:4 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-image-virtual amd64 4.4.0.210.216 [2,462 B]
Get:5 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-headers-virtual amd64 4.4.0.210.216 [1,754 B]
Get:6 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-headers-4.4.0-210 all 4.4.0-210.242 [10.0 MB]
Get:7 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-headers-4.4.0-210-generic amd64 4.4.0-210.242 [786 kB]
Get:8 http://us-east-1.ec2.archive.ubuntu.com/ubuntu xenial-updates/main amd64 linux-headers-generic amd64 4.4.0.210.216 [2,290 B]
Fetched 29.8 MB in 0s (47.9 MB/s)
Selecting previously unselected package linux-modules-4.4.0-210-generic.
(Reading database ... 937136 files and directories currently installed.)
Preparing to unpack .../linux-modules-4.4.0-210-generic_4.4.0-210.242_amd64.deb ...
Unpacking linux-modules-4.4.0-210-generic (4.4.0-210.242) ...
Selecting previously unselected package linux-image-4.4.0-210-generic.
Preparing to unpack .../linux-image-4.4.0-210-generic_4.4.0-210.242_amd64.deb ...
Unpacking linux-image-4.4.0-210-generic (4.4.0-210.242) ...
Preparing to unpack .../linux-virtual_4.4.0.210.216_amd64.deb ...
Unpacking linux-virtual (4.4.0.210.216) over (4.4.0.169.177) ...
Preparing to unpack .../linux-image-virtual_4.4.0.210.216_amd64.deb ...
Unpacking linux-image-virtual (4.4.0.210.216) over (4.4.0.169.177) ...
Preparing to unpack .../linux-headers-virtual_4.4.0.210.216_amd64.deb ...
Unpacking linux-headers-virtual (4.4.0.210.216) over (4.4.0.169.177) ...
Selecting previously unselected package linux-headers-4.4.0-210.
Preparing to unpack .../linux-headers-4.4.0-210_4.4.0-210.242_all.deb ...
Unpacking linux-headers-4.4.0-210 (4.4.0-210.242) ...
Selecting previously unselected package linux-headers-4.4.0-210-generic.
Preparing to unpack .../linux-headers-4.4.0-210-generic_4.4.0-210.242_amd64.deb ...
Unpacking linux-headers-4.4.0-210-generic (4.4.0-210.242) ...
Preparing to unpack .../linux-headers-generic_4.4.0.210.216_amd64.deb ...
Unpacking linux-headers-generic (4.4.0.210.216) over (4.4.0.169.177) ...
Setting up libjpeg-turbo8:amd64 (1.4.2-0ubuntu3.3) ...
Setting up linux-headers-4.4.0-169 (4.4.0-169.198) ...
Setting up linux-modules-4.4.0-210-generic (4.4.0-210.242) ...
Setting up linux-image-4.4.0-210-generic (4.4.0-210.242) ...
I: /vmlinuz.old is now a symlink to boot/vmlinuz-4.4.0-166-generic
I: /initrd.img.old is now a symlink to boot/initrd.img-4.4.0-166-generic
I: /vmlinuz is now a symlink to boot/vmlinuz-4.4.0-210-generic
I: /initrd.img is now a symlink to boot/initrd.img-4.4.0-210-generic
Setting up linux-image-virtual (4.4.0.210.216) ...
Setting up linux-headers-4.4.0-210 (4.4.0-210.242) ...
Setting up linux-headers-4.4.0-210-generic (4.4.0-210.242) ...
Setting up linux-headers-generic (4.4.0.210.216) ...
Setting up linux-headers-virtual (4.4.0.210.216) ...
Setting up linux-virtual (4.4.0.210.216) ...
Setting up linux-modules-4.4.0-169-generic (4.4.0-169.198) ...
Setting up linux-image-4.4.0-169-generic (4.4.0-169.198) ...
I: /vmlinuz.old is now a symlink to boot/vmlinuz-4.4.0-210-generic
I: /vmlinuz is now a symlink to boot/vmlinuz-4.4.0-169-generic
I: /initrd.img is now a symlink to boot/initrd.img-4.4.0-169-generic
Setting up linux-libc-dev:amd64 (4.4.0-169.198) ...
Processing triggers for libc-bin (2.23-0ubuntu10) ...
Processing triggers for linux-image-4.4.0-210-generic (4.4.0-210.242) ...
/etc/kernel/postinst.d/initramfs-tools:
update-initramfs: Generating /boot/initrd.img-4.4.0-210-generic
W: mdadm: /etc/mdadm/mdadm.conf defines no arrays.
/etc/kernel/postinst.d/zz-update-grub:
Generating grub configuration file ...
Found linux image: /boot/vmlinuz-4.4.0-210-generic
...
done
```

### 參考
- [apt-get install fails to create dependency tree every time](https://askubuntu.com/questions/1079624/apt-get-install-fails-to-create-dependency-tree-every-time)

## 執行sudo apt-get install -f 發生錯誤

錯誤訊息訊息看起來是disk空間滿了, 但使用`df -sh`發現還有空間, 後來查了一篇文章所提示的線索可能是inode滿了, 透過`df -i`檢查的確已經100%, 最後透過手動刪除`/usr/src/`較舊的linux-header減少inode的使用量
> No apport report written because the error message indicates a disk full error

```
sudo apt-get -f install
Reading package lists... Done
Building dependency tree
Reading state information... Done
Correcting dependencies... Done
The following packages were automatically installed and are no longer required:
  linux-headers-4.4.0-154 linux-headers-4.4.0-154-generic linux-headers-4.4.0-64 linux-headers-4.4.0-64-generic linux-headers-4.4.0-66 linux-headers-4.4.0-66-generic
  linux-headers-4.4.0-70 linux-headers-4.4.0-70-generic linux-headers-4.4.0-71 linux-headers-4.4.0-71-generic linux-headers-4.4.0-72 linux-headers-4.4.0-72-generic
  linux-headers-4.4.0-75 linux-headers-4.4.0-75-generic linux-headers-4.4.0-78 linux-headers-4.4.0-78-generic linux-headers-4.4.0-79 linux-headers-4.4.0-79-generic
  linux-headers-4.4.0-81 linux-headers-4.4.0-81-generic linux-headers-4.4.0-83 linux-headers-4.4.0-83-generic linux-headers-4.4.0-87 linux-headers-4.4.0-87-generic
  linux-headers-4.4.0-89 linux-headers-4.4.0-89-generic linux-headers-4.4.0-91 linux-headers-4.4.0-91-generic linux-headers-4.4.0-92 linux-headers-4.4.0-92-generic
  linux-headers-4.4.0-93 linux-headers-4.4.0-93-generic linux-headers-4.4.0-97 linux-image-4.4.0-154-generic linux-image-4.4.0-64-generic linux-image-4.4.0-66-generic
  linux-image-4.4.0-70-generic linux-image-4.4.0-71-generic linux-image-4.4.0-72-generic linux-image-4.4.0-75-generic linux-image-4.4.0-78-generic linux-image-4.4.0-79-generic
  linux-image-4.4.0-81-generic linux-image-4.4.0-83-generic linux-image-4.4.0-87-generic linux-image-4.4.0-89-generic linux-image-4.4.0-91-generic linux-image-4.4.0-92-generic
  linux-image-4.4.0-93-generic linux-modules-4.4.0-154-generic
Use 'sudo apt autoremove' to remove them.
The following additional packages will be installed:
  linux-headers-4.4.0-204-generic
The following NEW packages will be installed:
  linux-headers-4.4.0-204-generic
0 upgraded, 1 newly installed, 0 to remove and 126 not upgraded.
10 not fully installed or removed.
Need to get 0 B/796 kB of archives.
After this operation, 7,743 kB of additional disk space will be used.
Do you want to continue? [Y/n] Y
(Reading database ... 601175 files and directories currently installed.)
Preparing to unpack .../linux-headers-4.4.0-204-generic_4.4.0-204.236_amd64.deb ...
Unpacking linux-headers-4.4.0-204-generic (4.4.0-204.236) ...
dpkg: error processing archive /var/cache/apt/archives/linux-headers-4.4.0-204-generic_4.4.0-204.236_amd64.deb (--unpack):
 unable to create '/usr/src/linux-headers-4.4.0-204-generic/include/config/keyboard/lm8323.h.dpkg-new' (while processing './usr/src/linux-headers-4.4.0-204-generic/include/config/keyboard/lm8323.h'): No space left on device
No apport report written because the error message indicates a disk full error
                                                                              dpkg-deb: error: subprocess paste was killed by signal (Broken pipe)
Errors were encountered while processing:
 /var/cache/apt/archives/linux-headers-4.4.0-204-generic_4.4.0-204.236_amd64.deb
E: Sub-process /usr/bin/dpkg returned an error code (1)
```

> df -i
```
df -i
Filesystem                                Inodes  IUsed  IFree IUse% Mounted on
udev                                      495812    365 495447    1% /dev
tmpfs                                     498134    529 497605    1% /run
/dev/nvme0n1p1                            655360 650717   4643  100% /
tmpfs                                     498134      1 498133    1% /dev/shm
tmpfs                                     498134      3 498131    1% /run/lock
tmpfs                                     498134     16 498118    1% /sys/fs/cgroup
tmpfs                                     498134      5 498129    1% /run/user/1004
```

## 參考
- [apt-get "no space left on device" even it is %97 free](https://ubuntuforums.org/showthread.php?t=2039786)
- [How to Free Inode Usage](https://stackoverflow.com/questions/653096/how-to-free-inode-usage)

