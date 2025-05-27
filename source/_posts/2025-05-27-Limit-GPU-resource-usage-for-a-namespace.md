---
title: Limit GPU resource usage for a namespace
comments: true
date: 2025-05-27 07:30:21
description:
categories: software_development
tags:
- openshift
- gpu
---

延伸以下兩篇的內容:
- {% post_link openshift-sso-with-keycloak-and-389-Directory-Server '紀錄Openshift介接Keycloak與389 Directory Server' %}
- {% post_link sync-groups-in-keycloak-to-openshift '同步keycloak的group至openshift' %}

User和Group的資料來源為Directory Service，權限設定的部分交由Openshift(ResourceQuota, ClusterRole, RoleBinding)，主要參考這一篇文章:[Kubernetes: Limit GPU resource usage for a namespace](https://kb.brightcomputing.com/knowledge-base/kubernetes-limit-gpu-resource-usage-for-a-namespace/)

![](concept.png)

## 目標
- gpu-project-1
    - Assign 1 gpu resource quota
- gpu-project-2
    - Assign 3 gpu resource quota
- user1 in Group bu-1 
    - Can use 1 gpu in namespace gpu-project-1
    - Can **NOT** use 2 gpus in namespace gpu-project-1
    - Can **NOT** use the gpu in namespace gpu-project-2

## 建立namespace和ResourceQuota

``` bash
oc new-project gpu-project-1
oc new-project gpu-project-2
oc apply -f gpu-projects-quota.yaml
oc describe quota -n gpu-project-1
oc describe quota -n gpu-project-2
```

gpu-projects-quota.yaml
``` yml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-project-1-quota
  namespace: gpu-project-1
spec:
  hard:
    requests.nvidia.com/gpu: 1
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: gpu-project-2-quota
  namespace: gpu-project-2
spec:
  hard:
    requests.nvidia.com/gpu: 3
```

## 建立ClusterRole

``` bash
oc apply -f gpu-projects-clusterrole.yaml
```

gpu-projects-clusterrole.yaml
``` yml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: gpu-project-deployment-and-pod-manager
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "watch", "list", "create", "update", "patch", "delete"]
```

## 創建RoleBinding

``` bash
oc apply -f gpu-projects-rolebinding.yaml
```

gpu-projects-rolebinding.yaml
``` yml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-manager-bu1-binding
  namespace: gpu-project-1
subjects:
- kind: Group
  name: bu-1
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: gpu-project-deployment-and-pod-manager
  apiGroup: rbac.authorization.k8s.io
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-manager-bu2-binding
  namespace: gpu-project-2
subjects:
- kind: Group
  name: bu-2
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: gpu-project-deployment-and-pod-manager
  apiGroup: rbac.authorization.k8s.io
```

## 驗證

使用oc auth
``` bash
oc auth can-i  create pods --as jdoe --as-group bu-1  -n gpu-project-1
# yes
oc auth can-i  create pods --as jdoe --as-group bu-1  -n gpu-project-2
# no
oc auth can-i  create pods --as william --as-group bu-2  -n gpu-project-1
# no
oc auth can-i  create pods --as william --as-group bu-2  -n gpu-project-2
# yes
```

啟動container
![](msg_about_limit_gpu_resource.png)