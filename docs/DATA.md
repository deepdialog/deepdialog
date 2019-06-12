# 数据

## 前言

数据分三种：

- NLU数据，需要提供一句话到意图和槽值的数据
- DM数据，即对话流程，是用户行为和系统行为的流程
- NLG数据，系统行为到自然语言的过程

## NLU数据

```yaml
- domain: ''
  intent: hello
  data:
    - text: 你好
- domain: ''
  intent: bye
  data:
    - text: 再见
- domain: ''
  intent: thankyou
  data:
    - text: 谢谢
- domain: weather
  intent: inform
  data:
    - text: 北京市
      start: 0
      end: 3
      name: 城市
    - text: 今天
      start: 3
      end: 5
      name: 时间
    - text: 的天气
```

每句话有三个主要部分：

1. 这句话本身
2. 这句话的领域和意图
3. 这句话包含的槽值（包括位置信息）

如果我们单看一部分数据：

```yaml
- domain: weather
  intent: inform
  data:
    - text: 北京市
      start: 0
      end: 3
      name: 城市
    - text: 今天
      start: 3
      end: 5
      name: 时间
    - text: 的天气
```

这句话原本是：`北京市今天的天气`

而其中**北京市**和**今天**是需要提取的槽值

这句话的领域`weather`，意图是`inform`

领域可以理解为，这句话的场景，这里是谈论天气。

意图可以理解为，不考虑场景的情况下，这句话的本质意义，这句话的本质意义是用户**提供**了一些信息给系统，希望系统能给出在**天气领域内**的回复。

这里的**提供**就变成了**inform**意图。

## DM数据

```yaml
hello:
- user: hello
- sys: hello
bye:
- user: bye
- sys: bye
CLOSE_TODO2:
- user: todo::closeTodo()
- sys: requestNumber
- user: informNumber(数字)
- sys: closeTodo(数字)
```

首先对话流程中有一些一对一的回答，例如用户说**你好**，系统也给出相应的问候信息。

其次系统有一些**多轮**机制，例如我们要关闭（设置完成）一条TODO，我们需要给出具体TODO的编号。那么当我们告诉系统**我想关闭一条TODO**之后，系统应该问用户：**要关闭哪一条**，然后用户给出编号（数字）之后，系统才真的执行关闭某一条TODO。

## NLG

```yaml
None:
- 我不知道怎么理解
meetingStart:
- 开会会议记录
meetingEnd:
- 会议记录结束
hello:
- 你好啊，我是帕蒂安
bye:
- See You
```

NLG是系统行为到自然语言的转换，绝大部分时候和绝大部分情况，模板方法就足够了。
