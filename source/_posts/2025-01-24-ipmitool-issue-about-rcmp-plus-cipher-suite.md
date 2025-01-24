---
title: 紀錄使用ipmitool遇到關於RCMP+連線的問題
comments: true
date: 2025-01-24 02:52:45
description:
categories: software_development
tags:
- ipmi
- rcmp+
- xcat
---


## 驗證過程
使用xCAT進行MTMS discovery時失敗，檢查了/opt/xcat/lib/perl/xCAT_plugin/bmcdiscover.pm，發現以下症狀

``` bash
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar mc info -N 1 -R 1
```

```
Error in open session response message : invalid role

Error: Unable to establish IPMI v2 / RMCP+ session
```

修改`-I lanplus`為`-I lan`，有回傳結果 
``` bash
/opt/xcat/bin/ipmitool-xcat  -I lan -H 192.168.1.41 -U foo -P bar mc info -N 1 -R 1
```

根據[ipmitool(1) - Linux man page](https://linux.die.net/man/1/ipmitool)的資訊，lanplus這個介面使用了RMCP+ protocol，而RMCP+看起來和加解密有關係，有一個參數`-C`可以幫忙指定cipher suite ID


> -I <interface>
     Selects IPMI interface to use.


> Lan Interface
The ipmitool lan interface communicates with the BMC over an Ethernet LAN connection using UDP under IPv4. UDP datagrams are formatted to contain IPMI request/response messages with a IPMI session headers and RMCP headers. 

> Lanplus Interface
Like the lan interface, the lanplus interface communicates with the BMC over an Ethernet LAN connection using UDP under IPv4. The difference is that the lanplus interface uses the RMCP+ protocol as described in the IPMI v2.0 specification. RMCP+ allows for improved authentication and data integrity checks, as well as encryption and the ability to carry multiple types of payloads.

> The -C option allows you specify the authentication, integrity, and encryption algorithms to use for for lanplus session based on the cipher suite ID found in the IPMIv2.0 specification in table 22-19. The default cipher suite is 3 which specifies RAKP-HMAC-SHA1 authentication, HMAC-SHA1-96 integrity, and AES-CBC-128 encryption algorightms. 


看一下[IPMI2.0的spec]([Intelligent Platform Management Interface Specification Second Generation v2.0](https://www.intel.com.tw/content/dam/www/public/us/en/documents/product-briefs/ipmi-second-gen-interface-spec-v2-rev1-1.pdf))，cipher suite ID如下

![ipmi2_spec_cipher_suite_id](ipmi2_spec_cipher_suite_id.png)


使用lan print確認狀態，看起來有提供2個Cipher Suites，3和17
``` bash
/opt/xcat/bin/ipmitool-xcat  -I lan -H 192.168.1.41 -U foo -P bar mc info -N 1 -R 1
```

```
RMCP+ Cipher Suites     : 3,17
Cipher Suite Priv Max   : aXXXXXXXXXXXXXX
                        :     X=Cipher Suite Unused
                        :     c=CALLBACK
                        :     u=USER
                        :     o=OPERATOR
                        :     a=ADMIN
                        :     O=OEM
```

加上verbose mode`-v`確認
``` bash
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan print -N 1 -R 1 -v
```

```
Using best available cipher suite 17

Error in open session response message : invalid role

Error: Unable to establish IPMI v2 / RMCP+ session
```

使用`-I lanplus`加上 `-C 3`，出現了回傳結果!
``` bash
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar mc info -N 1 -R 1 -C 3
```

> cipher_privs <privlist>
    Correlates cipher suite numbers with the maximum privilege level that is allowed to use it. In this way, cipher suites can restricted to users with a given privilege level, so that, for example, administrators are required to use a stronger cipher suite than normal users.

>    The format of privlist is as follows. Each character represents a privilege level and the character position identifies the cipher suite number. For example, the first character represents cipher suite 1 (cipher suite 0 is reserved), the second represents cipher suite 2, and so on. privlist must be 15 characters in length. 

測試了
``` bash
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan set 1 cipher_privs aaXXXXXXXXXXXXX -N 1 -R 1 -C 3
# it works
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan print -N 1 -R 1 -C 17
# has response

/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan set 1 cipher_privs aaaXXXXXXXXXXXX -N 1 -R 1 -C 3
# hang...

/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan set 1 cipher_privs XaXXXXXXXXXXXXX -N 1 -R 1 -C 3
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan print -N 1 -R 1 -C 17
# it works
/opt/xcat/bin/ipmitool-xcat  -I lanplus -H 192.168.1.41 -U foo -P bar lan print -N 1 -R 1 -C 3
# Error: Unable to establish IPMI v2 / RMCP+ session
```

經過理解和測試，上面的描述的概念應該如下圖
![ipmi2_cipher_suite_priv_max](ipmi2_cipher_suite_priv_max.png)

## 結論
/opt/xcat/bin/ipmitool-xcat 這個client用的預設cipher suite看起來是17，但server端針對17的權限是關閉的，所以會出現`Unable to establish IPMI v2 / RMCP+ session`