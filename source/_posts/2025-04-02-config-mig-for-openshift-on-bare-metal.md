---
title: 使用安裝於裸機的openshift設定Nvidia GPU MIG(Multi-instance GPU)
comments: true
date: 2025-04-02 05:56:13
description:
categories: software_development
tags:
- openshift
- mig
- nvidia
- bare_metal
---

共享Nvidia GPU資源有幾種方式，其中一種是Multi-instance GPU (MIG)。根據[Chapter 2. NVIDIA GPU architecture | Red Hat Product Documentation](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/hardware_accelerators/nvidia-gpu-architecture)，安裝於裸機的openshift可以使用MIG，此外，在雲端供應商上的Openshift也可以使用MIG，記得需要先安裝GPU Operator，目前(2025/04/02)支援型號如下: A30, A100, A100X, A800, AX800, H100, H800

我對於Multi-instance GPU (MIG)概念的理解，類似虛擬機，透過設定可以將一張實體GPU隔離成多張邏輯上的GPU使用，目前最多可以隔離成7張。

預設提供不同隔離粒度的profiles可供選擇，檢視方式如下

``` bash
oc rsh  -n nvidia-gpu-operator  $(oc get pods -n nvidia-gpu-operator | grep -E 'nvidia-dcgm-exporter.*' | awk '{print $1}') nvidia-smi mig -lgip

# if not all gpu nodes support the MIG
oc get pods -n nvidia-gpu-operator | grep -E 'nvidia-dcgm-exporter.*' | awk '{print $1}
oc rsh  -n nvidia-gpu-operator nvidia-dcgm-exporter-dln49  nvidia-smi mig -lgip
```

For NVIDIA A100 40GB
```
Defaulted container "nvidia-dcgm-exporter" out of: nvidia-dcgm-exporter, toolkit-validation (init), init-pod-nvidia-node-status-exporter (init)
+-----------------------------------------------------------------------------+
| GPU instance profiles:                                                      |
| GPU   Name             ID    Instances   Memory     P2P    SM    DEC   ENC  |
|                              Free/Total   GiB              CE    JPEG  OFA  |
|=============================================================================|
|   0  MIG 1g.5gb        19     7/7        4.75       No     14     0     0   |
|                                                             1     0     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.5gb+me     20     1/1        4.75       No     14     1     0   |
|                                                             1     1     1   |
+-----------------------------------------------------------------------------+
|   0  MIG 1g.10gb       15     4/4        9.75       No     14     1     0   |
|                                                             1     0     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 2g.10gb       14     3/3        9.75       No     28     1     0   |
|                                                             2     0     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 3g.20gb        9     2/2        19.62      No     42     2     0   |
|                                                             3     0     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 4g.20gb        5     1/1        19.62      No     56     2     0   |
|                                                             4     0     0   |
+-----------------------------------------------------------------------------+
|   0  MIG 7g.40gb        0     1/1        39.38      No     98     5     0   |
|                                                             7     1     1   |
+-----------------------------------------------------------------------------+
```

## 啟用MIG
注意prefix，nvidia.com/mig.config=**all-1g.5gb**，一開始用nvidia.com/mig.config=**1g.5gb**啟用會失敗。有趣的是只要設定node的label後，GPU Operator看起來會自動根據label的值啟用對應的功能。

``` bash
# config the mig to node/worker-1(has a GPU A100) which is based on your environment
oc label  node/worker-1 nvidia.com/mig.config=all-1g.5gb --overwrite=true

# check the log
oc logs -n nvidia-gpu-operator $(oc get pods -n nvidia-gpu-operator -l app=nvidia-mig-manager -o jsonpath='{.items[0].metadata.name}')

# check the node
oc describe node worker-1
oc describe nodes | grep -A 6 "Capacity" 
oc get nodes -o=custom-columns='Node:metadata.name,GPU:status.capacity.nvidia\.com/gpu'
```

``` bash
Node        GPU
control-1   <none>
control-2   <none>
control-3   <none>
worker-1    7 # equals 1 before MIG enable
worker-2    1
```

``` bash
# show the mig
oc rsh -n nvidia-gpu-operator \
$(oc get pods -n nvidia-gpu-operator | grep -E 'nvidia-driver-daemonset.*' | awk '{print $1}') nvidia-smi mig -lgi

# if not all gpu nodes support the MIG
oc get pods -n nvidia-gpu-operator | grep -E 'nvidia-driver-daemonset.*' | awk '{print $1}'
oc rsh  -n nvidia-gpu-operator nvidia-driver-daemonset-417.94.202412180008-0-rzp8x nvidia-smi mig -lgi
```

以all-1g.5gb為例
```
+-------------------------------------------------------+
| GPU instances:                                        |
| GPU   Name             Profile  Instance   Placement  |
|                          ID       ID       Start:Size |
|=======================================================|
|   0  MIG 1g.5gb          19        7          4:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19        8          5:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19        9          6:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19       11          0:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19       12          1:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19       13          2:1     |
+-------------------------------------------------------+
|   0  MIG 1g.5gb          19       14          3:1     |
+-------------------------------------------------------+
```

## 測試

沒啟用MIG之前只能使用**nvidia.com/gpu: 1**

``` bash
cat << EOF | oc create -f -

apiVersion: v1
kind: Pod
metadata:
  name: cuda-vectoradd
spec:
 restartPolicy: OnFailure
 containers:
 - name: cuda-vectoradd
   image: "nvcr.io/nvidia/k8s/cuda-sample:vectoradd-cuda12.5.0-ubi8" 
   resources:
     limits:
       nvidia.com/gpu: 4
EOF
```

## 關閉MIG

``` bash
# disalbe the mig on node/worker-1
oc label  node/worker-1 nvidia.com/mig.config=all-disabled --overwrite=true
```

## 參考
- [Sharing is caring: How to make the most of your GPUs part 2 - Multi-instance GPU](https://www.redhat.com/en/blog/sharing-caring-how-make-most-your-gpus-part-2-multi-instance-gpu)

