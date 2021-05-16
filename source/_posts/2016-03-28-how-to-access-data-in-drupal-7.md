---
layout: post
title: "How to access data in Drupal 7"
date: 2016-03-28 10:05:52 +0800
comments: true
categories: software_development
tags:
- drupal7 
---

- Basic API
- Database API
    - Dynamic Query
    - Static Query
    - Show Query String and Arguments
- EntityFieldQuery

<!-- more  -->
## Basic API
    node_load, user_load, taxonomy_term_load, comment_load
    主要帶入參數為node id, user_id, term id, comment id


## Database API
### Dynamic Query
#### db_select
    $query = db_select('node', 'n');
    // access node table, alias is n

#### codition
    $query->condition($field, $value = NULL, $operator = '=')
    // 基本型態
    
    $query->condition('node.type', array('node_type_name'),'IN');
    // 使用In
    
    $query->condition('node.title',  '%'.db_like($key_word).'%', 'LIKE');
    // 使用Like
    
    $query->where('now() >  TIMESTAMPADD( DAY , 9, FROM_UNIXTIME( field_data_field_timefield.field_timefield_value  ) )');
    // 使用where而非condition的寫法
    
    $or = db_or();
    $or->condition('node.title','%'.db_like($key_word).'%', 'LIKE');
    $or->condition('comment.subject','%'.db_like($key_word).'%', 'LIKE');
    $query->condition($or);
    // 使用OR連接過濾條件

    
#### fields, addField
差別在於是否要使用欄位別名和一次可以存取的欄位數量
    $query->fields('node', array('nid', 'title'));
    // 一次存取多個欄位但無法使用欄位別名
    
    $query->addField('node','title','node_title');
    // 一次存取一個欄位，可以使用欄位別名

#### addExpression

    $query->addExpression('IFNULL(count1, 0)+IFNULL(count2, 0)','total_count');
    
    $query->addExpression('SUM(clickCount)', 'total_count');

#### join
預設join的型態為inner join, 有提供`join()`, `innerJoin()`, `leftJoin()`, or `rightJoin()`的方法

    $query = db_select('node', 'n');
    $table_alias = $query->join('users', 'u', 'n.uid = u.uid AND u.uid = :uid');
    // node table join user talbe on uid

#### SubQuery

    $subquery_customlog = db_select('customlog', 'clg')->fields('clg', array('nid'));
    $subquery_customlog->addExpression('COUNT(*)', 'count');
    $subquery_customlog->groupBy('clg.nid');
    $query = db_select('node','n')->fields('n', array('nid','title'));
    $query->leftJoin( $subquery_customlog, 'c_count' ,'c_count.nid = n.nid');
    ...
    // 自行產生所需的table後, 再Join到另一個table


#### Extender
tablesort和pager

    $query->extend('TableSort')
          ->orderByHeader($header);
    // Sorting Extender, 依照表格的Header排序
    
    $query->extend('PagerDefault')
          ->limit(10);
    // Pager Extender

### Static Query

    $result = db_query("SELECT nid, title FROM {node} WHERE type = :type", array( ':type' => 'page',));


### Show Query String and Arguments
顯示Drupal產生的SQL子句和參數

    echo $query->__toString() . "\n";
    // Get query string
    $args = $query->getArguments();
    var_dump($args);
    // Get the arguments passed to the string

## EntityFieldQuery
取得Entity相關的資料, 在Drupal中Entity指的是node, user, taxonomy term, comment...等。回傳值是和entity相關的ID值，必須另外使用entity_load讀取entity其他資料。

和Basic API相比，優勢在於能使用較複雜的過濾條件得到想要的entity資料；和Database API相比，優勢在於直接以entity觀點看資料，直覺性較強，有一個小缺點是EntityFieldQuery若要同時取得兩個entity的資訊，很難使用join的概念處理。

    $query = new EntityFieldQuery();
    
    $query->entityCondition('entity_type', 'node')
          ->entityCondition('bundle', 'article')
          ->propertyCondition('status', NODE_PUBLISHED)
          ->fieldCondition('field_news_types', 'value', 'spotlight', '=')
          ->fieldCondition('field_news_publishdate', 'value', $year . '%', 'like')->fieldCondition('field_news_publishdate', 'value', $year . '%', 'like')
          ->fieldOrderBy('field_photo', 'fid', 'DESC')
          ->range(0, 10);
    
    $result = $query->execute();
    
    if (isset($result['node'])) {
      $news_items_nids = array_keys($result['node']);
      $news_items = entity_load('node', $news_items_nids);
    }

## Ref.
- [node_load](https://api.drupal.org/api/drupal/modules%21node%21node.module/function/node_load/7)
- [user_load](https://api.drupal.org/api/drupal/modules%21user%21user.module/function/user_load/7)
- [taxonomy_term_load](https://api.drupal.org/api/drupal/modules%21taxonomy%21taxonomy.module/function/taxonomy_term_load/7)
- [comment_load](https://api.drupal.org/api/drupal/modules%21comment%21comment.module/function/comment_load/7)
- [Dynamic queries](https://www.drupal.org/dynamic-queries)
- [Static queries](https://www.drupal.org/node/310072)
- [How to use EntityFieldQuery](https://www.drupal.org/node/1343708)
