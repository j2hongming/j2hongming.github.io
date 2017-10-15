---
layout: post
title: "Get field names of Content Type in Drupal"
date: 2016-03-31 13:30:28 +0800
comments: true
categories:
- drupal7
- code snippet 
---

{% codeblock  lang:php %}

/**
* 取得ContentType的field name
* @see 
* @link http://drupal.stackexchange.com/questions/39850/get-all-fields-for-a-given-content-type-including-title
*/

function modulename_get_field_name($content_type){

            $fields = array();
            $field_map = field_info_field_map();
            $instances = field_info_instances('node', $content_type);
            $extra_fields = field_info_extra_fields('node', $content_type, 'form');

            // Fields.
            foreach ($instances as $name => $instance) {
              $field = field_info_field($instance['field_name']);
              $fields[$instance['field_name']] = array(
                'field_name' => $instance['field_name'],
                'title' => $instance['label'],
                'weight' => $instance['widget']['weight'],
                'type' => $field_map[$instance['field_name']]['type'],
              );
            }
           
            
            // Non-field elements. ex. title
            foreach ($extra_fields as $name => $extra_field) {
              $fields[$name] = array(
                'title' => $extra_field['label'],
                'weight' => $extra_field['weight'],
              );
            }
            
            return $fields;
}


{% endcodeblock %}
