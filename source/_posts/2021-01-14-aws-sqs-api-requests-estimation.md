---
title: 預估AWS SQS API Requests的使用量
comments: true
date: 2021-01-14 00:37:00
description: 利用CloudWatch Metrics的NumberOfMessagesSent預估AWS SQS API Requests的使用量
categories: software_development
tags:
- AWS
- SQS
---

AWS SQS計費的其中一個來源是monthly requests的數量, 這邊的request根據說明就是SQS的API Action

> API Actions: Every Amazon SQS action counts as a request.

最近剛好使用Cost Explorer查詢SQS的API使用量, 發現會等於使用CloudWatch Metrics的四個Metric
- NumberOfMessagesSent
- NumberOfMessagesReceived
- NumberOfMessagesDeleted
- NumberOfEmptyReceives

SQS的API使用量 = NumberOfMessagesSent + NumberOfMessagesReceived + NumberOfEmptyReceives + NumberOfMessagesDeleted

![](cost_explorer.png)
![](cloudwatch_metrics.png)

我自己的理解是假設不使用Batch操作的情況, 使用SQS的一個message從進去到出來至少要使用3個API Requestsi(Send, Receive and Delete)

所以可以使用NumberOfMessagesSent * 3 預估SQS API Requests的使用量

## 參考
- [Amazon SQS pricing](https://aws.amazon.com/sqs/pricing)
- [Available CloudWatch metrics for Amazon SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-available-cloudwatch-metrics.html)
- AWS SQS Batch Operations
  - [SendMessageBatch](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_SendMessageBatch.html)
  - [ReceiveMessage](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_ReceiveMessage.html)
  - [DeleteMessageBatch](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_DeleteMessageBatch.html)
