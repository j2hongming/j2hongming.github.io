---
title: Ansible的host list inventory
comments: true
date: 2025-04-24 08:31:50
description:
categories: software_development
tags:
- ansible
- inventory
---

利用[mirror-registry](https://github.com/quay/mirror-registry)安裝quay時，因為hostname存在大寫字母，意外發現ansible的inventory除了檔案形式之外還有一種host list形式。

安裝quay失敗，訊息如下

```
root@FOO-Admin | UNREACHABLE! => {
    "changed": false,
    "msg": "Failed to connect to the host via ssh: ssh: Could not resolve hostname foo-admin: Name or service not known",
    "unreachable": true
}
```

發現安裝過程中使用了以下指令，覺得疑惑，因為過去使用inventory的經驗是用檔案的形式

``` bash
ansible-playbook -i root@FOO-Admin, --private-key /runner/env/ssh_key
```

查了一下Ansible文件沒找到，最後是透過以下prompt去問生成式AI，得到提示，似乎有個inline inventory的呼叫方式，再透過google搜尋去找
```
what parameter can be used by ansible-playbook -i
```

![](ansible_inventory.png)

最後在某一篇stackoverflow的問答找到這份[Ansible文件](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/advanced_host_list_inventory.html)，原來真正的名稱是**advanced_host_list inventory**

觸發條件如下，參數非路徑且包含一個逗號:

> This plugin only applies to inventory sources that are not paths and contain at least one comma.

``` bash
ansible-playbook -i 'localhost,' play.yml
```

![](/images/meme/weird.jpg)

## 結論
使用advanced_host_list inventory方式呼叫目前有一個限制，hostname內不能包含大寫字母。
使用inventory檔案目前沒有hostname大小寫的議題。