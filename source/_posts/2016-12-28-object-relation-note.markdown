---
layout: post
title: "類別的關係"
date: 2016-12-28 00:05:08 +0800
comments: true
categories:
- object
- relation 
---

從組成類別的結構開始，有兩大主體:`屬性`(instance variable, attribute)和`操作`(method, operation)。

因此，類別和類別之間接合的地方可能會出現在屬性或者操作當中。
<!-- more -->

## 出現在屬性

- 關聯關係: 一個類別被當作是另一個類別的變數。( [1]page 8-17 )
- 聚合關係: 表達整體和部分的關係。( [1] page 8-18 )
- 組合關係: 聚合關係且整體的消失會造成部分的消失。( [1] page 8-18 )

``` java
public class Car{
  private Driver driver;
  private Tire[] tires;
}
```

Car和Driver有關聯關係。Car和Tire有聚合關係。

## 出現在操作

- 相依關係: 一個類別使用(use)其他類別所提供的服務，意即類別A呼叫了類別B的操作。 ( [1]page 8-22 )

因為操作的本體其實是函式(function)，函式的結構包含`帶入參數`和`函式本體`，所以帶入參數可能是其他的類別物件；函式本體可能包含宣告其他類別物件的`區域變數`或是直接使用其他類別物件的`static function`。以上皆代表類別A呼叫了類別B的操作可能產生的情形。

### 帶入參數

``` java
public class KFC{
  
  public Chicken makeChicken( Meat m){
      m.disinfect();
      ...
  } 
}
```

### 函式本體-區域變數

``` java
public class KFC{

  public void preProcess(){
      
      Oil oil = new Oil();
      oil.fry( );
      ...
  }
}
```

### 函式本體-static method

``` java
public class KFC{

  public void postProcess(){

      // clean is a static function
      CleanMachine.clean();
      ...
  }
}

```

## 其他

- 一般化(抽象化)
- 具體化

在Java中，一般化用`extends`;具體化用`implements`。

## 總結

類別的關係總共有五種，其中透過類別屬性傳遞資料的關係為`關聯`、`聚合`以及`組合`。透過類別操作傳遞資料的關係為`相依`。其他為`一般化`和`具體化`。

## Ref
1. [UML物件導向系統分析與設計[第二版] / 游峰碩](http://www.books.com.tw/products/0010509593)
2. [BGP - Part1: Software design principles for Agile 敏捷 軟體設計原則 / James Hsieh](https://www.youtube.com/watch?v=mzaTpKZm54A)
