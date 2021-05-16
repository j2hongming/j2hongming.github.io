---
layout: post
title: "Batch API Notes"
date: 2016-03-28 14:41:34 +0800
comments: true
categories: software_development
tags:
- drupal7
- batch 
---

- 設定operations
- 設定batch資訊
- 設定finish callback function
- 線上展示
- 其他批次處理可用模組

<!-- more -->

>Batch sets are used to spread processing (primarily, but not exclusively, forms processing) over several page requests. This helps to ensure that the processing is not interrupted due to PHP timeouts, while users are still able to receive feedback on the progress of the ongoing operations.
>[Batch operations](https://api.drupal.org/api/drupal/includes%21form.inc/group/batch/7)

## 設定operations
可依照需求切割一個operation內做的事，假設1000個node，可以一個operation處理一個node或一個operation處理多個node。Client端利用ajax對https://sitename/batch?id=[batch_id]&op=do發出HttpRequest。

    // 假設$data是從EXCEL中讀出的資料
    
    $split_rows = array_chunk($data, 50);
    
    foreach ($split_rows as $key => $rows) {
      $operations[] = array(
      	'import_batch_processing',  // The function to run on 50 row in one operation
      	array($rows),  // The rows in the Excel
      );
    }

## 設定batch資訊

    $batch = array(
      'title' => t('批次處理中...'),
      'operations' => $operations,  // Runs all of the queued processes from the while loop above.
      'file' => drupal_get_path('module', 'module_name_which_you_create') . '/import_batch_processing.inc',
      'finished' => 'import_batch_processing_finished', // Function to run when the import is successful
    'error_message' => t('The installation has encountered an error.'),
    'progress_message' => t('資料匯入中...'),
    );

- `file`: 若import_batch_processing和import_batch_processing_finished沒有定義在.module檔內，需設定有定義這兩個callback function的file。[Batch API process silently fails](http://data.agaric.com/batch-api-process-silently-fails-if-function-file-not-default-drupal-bootstrap-isnt-explicitly-inclu)
- `finished`: batch結束後須執行的callback function
- `error_message`:batch過程中若發生錯誤的回傳訊息
- `progress_message`: batch過程中顯示的訊息

## 設定finish callback function

    function import_batch_processing_finished( $success, $results, $operations ){
    if($success){
      ...
    }
    else {
      // An error occurred.
      // $operations contains the operations that remained unprocessed.
      $error_operation = reset($operations);
      drupal_set_message(
        t('An error occurred while processing @operation with arguments : @args',
          array(
            '@operation' => $error_operation[0],
            '@args' => print_r($error_operation[0], TRUE),
          )
        )
      );
    }


## 線上展示
1. [Evaluate Drupal projects online](https://simplytest.me/)
2. 安裝模組 Examples for Developers
3. 登入admin帳號後，開啟模組Devel generate和Batch example
4. 前往路徑 admin/config/development/generate/content，新增1000個測試Node
5. 前往路徑 examples/batch_example，開始測試

>可配合程式碼觀察
>[Batch example source code](http://cgit.drupalcode.org/examples/tree/batch_example/batch_example.module?id=refs/heads;id2=7.x-1.x)


## 其他批次處理可用模組
- [Views Data Export](https://www.drupal.org/project/views_data_export)
- [Node export](https://www.drupal.org/project/node_export)


## Ref.
- [Batch operations](https://api.drupal.org/api/drupal/includes%21form.inc/group/batch/7)
- [how to use the Batch API](https://www.drupal.org/node/180528)
- [Using Batch API to build huge CSV files for custom exports](http://www.jeffgeerling.com/blogs/jeff-geerling/using-batch-api-build-huge-csv)
