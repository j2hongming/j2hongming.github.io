---
layout: post
title: "Java String 常用操作"
date: 2016-08-10 11:53:36 +0800
comments: true
categories:
- java
- string 
---

- 轉換(transform)-魔形女
- 比較(compare)
- 子集合(subset)
- 分割(split)-次元刀
- 合併(join)

<!-- more -->

## 轉換(transform)-魔形女

### Some Data Type -> String

Integer -> String
``` java
int number = 1234;

// public static String valueOf(int i)
String.valueOf(number)

// public static String toString(int i)
Integer.toString(number)

// Let JVM do it
"" + number

```

char -> String
``` java
char c = '0';
String.valueOf(char);
```

int Array -> String
``` java
int[] array = {1,2,3,4};
String strArr = Arrays.toString(array);
// strArr is "[1, 2, 3, 4]"
```

byte Array -> String
``` java
// bytes is byte[] type
String testString = new String(bytes, StandardCharsets.UTF_8);
```
- [Java Integer To String Examples](http://javadevnotes.com/java-integer-to-string-examples)
- [Java - Convert integer to string](http://stackoverflow.com/questions/5071040/java-convert-integer-to-string)
- [How to convert an int array to String with toString method in Java](http://stackoverflow.com/questions/10904911/how-to-convert-an-int-array-to-string-with-tostring-method-in-java)
- [Conversion to / from bytes](http://stackoverflow.com/documentation/java/109/strings/1862/conversion-to-from-bytes#t=201608100618202285977)
- [Oracle Docs: String](https://docs.oracle.com/javase/7/docs/api/java/lang/String.html)

### String -> Some Data Type

Some Data Type: int, long, BigInteger, BigDecimal, double, byte[], char[]
``` java
String number = "1234";
String bigDecimal = "1234.5678";
String doubleN = "3.14";

// String to int
int intNum = Integer.parseInt(number);

// String to long
long longNum = Long.parseLong(number);

// String to BigInteger
BigInteger bigIntegerNum = new BigInteger(number);

// String to BigDecimal
BigDecimal bigDecimalNum = new BigDecimal(bigDecimal);

// String to double
double doubleNum = Double.parseDouble(doubleN);

// Handle the "NumberFormatException"
```

``` java
// String to byte[]
byte[] bytes = "1234".getBytes(StandardCharsets.UTF_8);
```

``` java
// String to char[]
String s = "1234";
char[] charArray = s.toCharArray();

// if use 3rd party library (Apache commons-lang)
Character[] charObjectArray = ArrayUtils.toObject(charArray);
```

``` java
// Arrays.asList
String pokemon = "Bulbasaur,Charmander,Squirtle,Pikachu";
String[] pokemons = pokemon.split(",");
List<String> pokemonList = Arrays.asList(pokemons);

// new ArrayList
List<String> pokemonList2 = new ArrayList<String>(Arrays.asList(pokemons));

```
- [Converting String to other datatypes.](http://stackoverflow.com/documentation/java/109/strings/11480/converting-string-to-other-datatypes#t=201608100618128217497)
- [Conversion to / from bytes](http://stackoverflow.com/documentation/java/109/strings/1862/conversion-to-from-bytes#t=201608100618202285977)
- [Converting string to Character Array](http://stackoverflow.com/documentation/java/109/strings/1837/converting-string-to-character-array#t=201608100619012006559)
- [Java Split String Into ArrayList Examples](http://javadevnotes.com/java-split-string-into-arraylist-examples)


## 比較(compare)

`equals`, `equalsIgnoreCase`, `compareTo`, `compareToIgnoreCase`

``` java
String str1 = "abc";
String str2 = new String("abc");
String str3 = new String("aBc");

// True
str1.equals(str2)
// False
str1.equals(str3)
// False
str2.equals(str3)

// 0
str1.compareTo(str2)
// 32
str2.compareTo(str3)
// -32
str3.compareTo(str2)

```

- [Comparing Strings](http://stackoverflow.com/documentation/java/109/strings/453/comparing-strings#t=201608100648440805948)

## 子集合(subset)

`substring`, 使用開始(beginIndex)與結束標記(endIndex)取得不包含結束標記的子字串。

``` java
String str1 = new String("0123456789");

// 56789
str1.substring(5)

// 5678
str1.substring(5, 9)

```
- [Java Substring Examples](http://javadevnotes.com/java-substring-examples)
- [Stack Overflow: Java String: Substrings](http://stackoverflow.com/documentation/java/109/strings/545/substrings#t=201608100717465737842)

## 分割(split)-次元刀

`split` 或 `StringTokenizer`，注意escape character

split
``` java
// public String[] split(String regex)
String pokemon = "Bulbasaur,Charmander,Squirtle,Pikachu";
String[] pokemons = pokemon.split(",");

String pokemonCP = "Bulbasaur235Charmander167Squirtle3310Pikachu9527";
// {"Bulbasaur","Charmander","Squirtle","Pikachu"}
String[] pokemons = pokemonCP.split("\\d+");
```

StringTokenizer
``` java
// Default set of characters are empty spaces (\t\n\r\f)
String pokemon = "Bulbasaur Charmander Squirtle Pikachu";
StringTokenizer tokenizer = new StringTokenizer(pokemon);
while (tokenizer.hasMoreTokens()) {
    System.out.println(tokenizer.nextToken());
}
```

- [Java String Split Tutorial And Examples](http://javadevnotes.com/java-string-split-tutorial-and-examples)
- [Stack Overflow:Splitting Strings using split](http://stackoverflow.com/documentation/java/109/strings/3306/splitting-strings-using-split#t=201608100730280433428)
- [Stack Overflow:Splitting Strings using StringTokenizer](http://stackoverflow.com/documentation/java/109/strings/6346/splitting-strings-using-stringtokenizer#t=201608100730292621908)


## 合併(join)
`+`,String的`concat`, StringBuffer或StringBuilder的`append`

延伸議題：[StringBuilder vs String concatenation in toString() in Java](http://stackoverflow.com/questions/1532461/stringbuilder-vs-string-concatenation-in-tostring-in-java)

``` java
String str1 = "Pikachu is";
String str2 = " cute";

str1 = str1.concat(str2);

StringBuilder sb = new StringBuilder();
sb.append(str1);
sb.append(str2);
sb.toString();
```

