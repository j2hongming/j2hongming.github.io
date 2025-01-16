---
title: 關於openshift compact cluster topology的角色
comments: true
date: 2025-01-16 07:05:05
description:
categories: software_development
tags:
- openshift
---

根據[官方文件](https://docs.openshift.com/container-platform/4.12/installing/installing_with_agent_based_installer/preparing-to-install-with-agent-based-installer.html#recommended-resources-for-topologies)的描述，有三種topology，其中compact cluster的架構當中，ControlPlane同時也會有Worker node的角色

> A compact cluster that has three master nodes that are also worker nodes.

![](openshift_recommended_resources_for_topologies.png)

Compact cluster example
![](openshift_compact_cluster.png)

HA cluster example
![](openshift_ha_cluster.png)
