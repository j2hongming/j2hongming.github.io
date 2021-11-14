---
title: AWS Parameter Store to Bash Associative Arrays
comments: true
date: 2021-08-27 00:08:27
description: 擷取ssm回傳值在bash中轉為Associative Arrays使用
categories: software_development
tags:
- AWS
- Systems Manager
- bash
---
Parameter Store可以透過prefix的方式(get-parameters-by-path)取得多個值, 想要在bash進一步使用的話可以先轉換成Associative Arrays

```bash=
# sample
# [
# 	  {
# 	    "Name": "/alpha/test/a",
# 	    "Value": "a-data"
# 	  },
# 	  {
# 	    "Name": "/alpha/test/b",
# 	    "Value": "b-data"
# 	  }
# 	]
sample=$(aws ssm get-parameters-by-path --path /alpha/test --with-decryption --query "Parameters[*].{Name:Name,Value:Value}")

echo "${sample}" | jq -c '.[]'

declare -A test

for row in $(echo "${sample}" | jq -r '.[] | @base64'); do
    _jq() {
     echo ${row} | base64 --decode | jq -r ${1}
    }
#    echo $(_jq '.Name')
#    echo $(_jq '.Value')
   test[$(_jq '.Name')]=$(_jq '.Value')
done

echo ${test[/alpha/test/a]}
echo ${test[/alpha/test/b]}
```
## 參考
- [Working with parameter hierarchies](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-hierarchies.html)
- [get-parameters-by-path](https://docs.aws.amazon.com/cli/latest/reference/ssm/get-parameters-by-path.html)
- [BASH FOR LOOP OVER JSON ARRAY USING JQ](https://www.starkandwayne.com/blog/bash-for-loop-over-json-array-using-jq/)
- [BashGuide/Arrays](http://mywiki.wooledge.org/BashGuide/Arrays)

