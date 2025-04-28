---
title: 初步理解 NVIDIA AI Enterprise
comments: true
date: 2025-04-28 07:55:22
description:
categories: software_development
tags:
- nvidia
- ai
- gpu
- openshift
---

剛開始看到這個概念對我來說蠻抽象，不曉得到底涵蓋以及處理哪些部分，使用了生成式AI也無法解決我的困惑。

https://chatgpt.com/share/680f3652-a80c-8009-b30d-17df27dbfe67
> NVIDIA AI Enterprise is a software platform designed to help businesses easily build, deploy, and manage AI workloads on NVIDIA hardware, either on-premises (your own servers) or in the cloud.

以後見之明來看，上述這段描述沒有問題，但沒有實際跑過一次相關的流程，腦袋還是一頭霧水。有一個最關鍵的問題剛開始很難想通: 

NVIDIA AI Enterprise到底想賣什麼?

稍微嘗試過以及搭配這一篇[Quick Start Guide](https://docs.nvidia.com/ai-enterprise/release-6/latest/getting-started/quick-start-guide.html#installing-nvidia-ai-enterprise-software-components)，目前的理解NVAIE主要涵蓋以及處理的部分如下:
- Infrastructure management and orchestration software
    - 如[這邊](https://docs.nvidia.com/ai-enterprise/release-6/latest/getting-started/quick-start-guide.html#accessing-the-nvidia-ai-enterprise-infrastructure-software)所描述，如:GPU Operator, vGPU...等
- Tools for AI development and use cases
    - NGC平台上針對NVIDIA GPU調教過的container image
    - NGC平台上的模型(給NIM使用)
- Support service

## 部屬方式

非常多樣性，本質上需要搭建可以跑container的環境。有Quick Start Guide上提的[bare-metal, single-node deployment of NVIDIA AI Enterprise using Docker](https://docs.nvidia.com/ai-enterprise/release-6/latest/getting-started/quick-start-guide.html#installing-nvidia-ai-enterprise-on-bare-metal-ubuntu-22-04)

也有搭建在Openshift上，底層架構可以有[6種類型的方式](https://docs.redhat.com/en/documentation/openshift_container_platform/4.17/html/hardware_accelerators/nvidia-gpu-architecture#nvidia-gpu-enablement_nvidia-gpu-architecture)，仔細想想本質上就是就是bare-metal, private cloud by virtual machine(VMware, KVM), public cloud

![Figure 2.1. NVIDIA GPU enablement](https://access.redhat.com/webassets/avalon/d/OpenShift_Container_Platform-4.17-Hardware_accelerators-en-US/images/ab8a6807e4b1b8561dd9cf7d895315fc/512_OpenShift_NVIDIA_GPU_enablement_1223.png)

## GPU Operator
在Kubernetes和Openshift會出現的概念，實際上負責處理兩個關鍵部分: [NVIDIA Driver](https://docs.nvidia.com/ai-enterprise/release-6/latest/getting-started/quick-start-guide.html#installing-nvidia-ai-enterprise-using-the-trd-driver-on-ubuntu-22-04-from-a-run-file)和[NVIDIA Container Toolkit](https://docs.nvidia.com/ai-enterprise/release-6/latest/getting-started/quick-start-guide.html#installing-the-nvidia-container-toolkit)

> The NVIDIA Container Toolkit allows users to build and run GPU-accelerated Docker containers.