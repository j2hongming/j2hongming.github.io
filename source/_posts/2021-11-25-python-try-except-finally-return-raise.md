---
title: python try-except-finally, return and raise
comments: true
date: 2021-11-25 01:17:09
description:
categories: software_development
tags:
- python
- exception
---

利用request module呼叫外部服務時透過raise_for_status處理HTTPError, 遇到某一種HTTP code時需要再raise一個自定義的Exception出去, 但發現沒有發揮作用

``` python=
try:
    result = dict()
    r = requests.get('http://www.google.com/nothere')
    r.raise_for_status()
except requests.exceptions.HTTPError as err:
    raise MyCustomizedException(err)
finally:
    return result
```

先說結論, 因為finally內有return的語法, 所以MyCustomizedException不會被raise, python的官方文件說得很清楚

> If the finally clause executes a break, continue or return statement, exceptions are not re-raised.

第二次遇到這種情況, 嘗到沒好好地看文件和紀錄的苦果, 決定記錄下來關於`try-except-finally`, `return` 和 `raise`的關係

文件中提到以下注意事項
- If an exception occurs during execution of the try clause, the exception may be handled by an except clause. If the exception is not handled by an except clause, the exception is re-raised after the finally clause has been executed.
- An exception could occur during execution of an except or else clause. Again, the exception is re-raised after the finally clause has been executed.
- If the finally clause executes a break, continue or return statement, exceptions are not re-raised.
- If the try statement reaches a break, continue or return statement, the finally clause will execute just prior to the break, continue or return statement’s execution.
- If a finally clause includes a return statement, the returned value will be the one from the finally clause’s return statement, not the value from the try clause’s return statement.

沒有處理或處理過程中又發生其他Exception的時候, 一般來說會在finally block完成後re-raise 

在finally block包含`break`, `continue` 或 `return` 語法時, 不會re-raise

## try-except-finally and return

``` python=
try:
    # <= retrun here
except Exception as e:
    # handle exception
finally:
    # <= return here
```
有三種狀況
1. retrun in try
2. return in finally
3. return in both

``` python=
# 1. return in try
def return_in_try_with_finally():
    try:
        print('return in try with finally')
        print('try block')
        return 1
    except Exception as e:
        print('in exception block')
    finally:
        print('finally block')
        
if __name__ == '__main__':
    print(return_in_try_with_finally()
          
# return in try with finally
# try block
# finally block
# 1
```

``` python=
# 2. return in finally
def return_in_finally():
    try:
        print('return in finally')
        print('try block')
    except Exception as e:
        print('in exception block')
    finally:
        print('finally block')
        return 1

if __name__ == '__main__':
    print(return_in_finally()
    
# return in finally
# try block
# finally block
# 1
```

``` python=
# 3. return in both
def return_in_try_and_finally():
    try:
        print('return in try and finally')
        print('try block')
        return 1
    except Exception as e:
        print('in exception block')
    finally:
        print('finally block')
        return 3
    
if __name__ == '__main__':
    print(return_in_try_and_finally()
          
# return in try and finally
# try block
# finally block
# 3
```

## try-except-finally, return and raise

``` python=
def return_in_try_and_finally_and_no_raise():
    try:
        print('return in try with finally and no re-raise')
        print('try block')
        result = 1 / 0
        return result
    except Exception as e:
        print('in exception block')
        raise # <= no effect because there is a return statement in finally
    finally:
        print('finally block')
        return 3

if __name__ == '__main__':
    print(return_in_try_and_finally_and_no_raise()    

# return in try with finally and no re-raise
# try block
# in exception block
# finally block
# 3
```

``` python=
def return_in_try_with_finally_and_has_raise():
    try:
        print('return in try with finally and re-raise')
        print('try block')
        result = 1 / 0
        return result
    except Exception as e:
        print('in exception block')
        raise
    finally:
        print('finally block')

if __name__ == '__main__':
    print(return_in_try_with_finally_and_has_raise()  
        
# Traceback (most recent call last):
#   File "/home/j2hongming/labs/2018-ithome-ironman-python/exception/finally_return.py", line 103, in <module>
#     print(return_in_try_with_finally_and_has_raise())
#   File "/home/j2hongming/labs/2018-ithome-ironman-python/exception/finally_return.py", line 72, in return_in_try_with_finally_and_has_raise
#     result = 1 / 0
# ZeroDivisionError: division by zero
```

## reference
- [Defining Clean-up Actions](https://docs.python.org/3/tutorial/errors.html#defining-clean-up-actions)
- [Python try finally block returns](https://stackoverflow.com/questions/19805654/python-try-finally-block-returns)
- [Re-raising the exception doesn't work with "finally" clause](https://stackoverflow.com/questions/43830803/re-raising-the-exception-doesnt-work-with-finally-clause)
