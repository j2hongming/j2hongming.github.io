---
title: 啟動AWS EC2 instance遇到iam:PassRole的權限問題
comments: true
date: 2021-08-14 00:19:44
description:
categories: software_development
tags:
- AWS
- EC2
- IAM
---

測試部門的同事遇到一個問題: 在AWS EC2 instance(A)上執行ansible啟動其他新的instance(B)時會失敗, 同事告知已經試過在instace A上使用AWS CLI執行, 且結果是正常的

```
aws ec2 run-instances \
    --image-id ami-999999cabd34c712a \
    --instance-type t2.micro \
    --key-name abc
```

之後從log內發現可能是因為iam:PassRole這個權限的關係, 另一位開發同事協助檢查instace A上所掛載的IAM Role相關權限, 發現只有和ec2:RunInstance有關的權限, 補上iam相關的權限後, ansible執行結果就是正常的

## 小結
iam:PassRole從字面上有點難以理解, 從執行效果來看類似

> 賦予將某某Role掛載到某某Resource上的權限

回頭來看, 使用AWS CLI執行結果正常的原因是所啟動的EC2 instance並沒有掛載Role, 如圖下方

![](iam-passrole.png)

因此, 若要啟動一個有掛載IAM Role的EC2 instance, 可以參考官方文件的範例

```json=
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ec2:RunInstances",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::ACCOUNT-ID-WITHOUT-HYPHENS:role/Get-pics"
    }
  ]
}
```

## 參考
- [AWS EC2 instance create via Ansible IAM Roles instance_profile_name UnauthorizedOperation: Error](https://stackoverflow.com/questions/24401846/aws-ec2-instance-create-via-ansible-iam-roles-instance-profile-name-unauthorized)
- [Granting a user permissions to pass a role to an AWS service](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_passrole.html)
- [Why am I receiving the error message "You are not authorized to perform this operation" when I try to launch an EC2 instance?](https://aws.amazon.com/tw/premiumsupport/knowledge-center/ec2-not-auth-launch/)


