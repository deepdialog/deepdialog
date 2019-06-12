# DST 模块

这部分也被称为Belief Tracking

首先我们问自己一个问题，为什么需要DST？

这个问题是因为我们需要一种对话状态，或者至少我们觉得，如果对话流程有一种状态性的东西比较合理，至于是否能够“无状态”，我们最后再讨论。

## 对话状态的目的

我们可以简单的认为，多个时间点（多个回合，每个回合代表用户和系统的一次交互）的多个对话状态组成了对话状态的历史，而系统的下一个部件DPL，使用对话状态历史进行系统的决策。

## DST的目的

首先我们看对话状态有什么用，它通过用户行为的刺激而改变，它的目的是用于决策系统的行为，这比较符合类似控制论的思想。我们假设流程是这样的：

```math
用户行为 = NLU（当前用户的发言）
历史状态t+1 = DST（历史状态t，用户行为）
系统行为 = DPL（历史状态t+1）
```

也就是说，DST的目标是根据历史状态t和用户行为，生成新的历史状态t+1。

历史状态可以认为是N个对话状态的集合，也可以认为：

```math
历史状态t+1 = 历史状态t + 对话状态t+1
```

## 什么是对话状态

对话状态至少包括两部分，对DST来收只读的部分和可变的。

### 什么是对DST只读的

例如用户行为是用户决定的，系统应该不改变（但是可以增强或修正），所以对DST来说就是只读的。

例如系统行为是DPL发出的，是系统已经做过的决策，这个自然也是只读的。

### 什么是对DST可变的

对于基于帧（Frame）的对话系统来说，可变的部分基本上是已经定义了的帧中的内容。

例如我们设计这样的一个对话帧，用来实现返回天气预报。我们假设这个系统只能回答某一天的某个城市的天气，那么就有两个必要变量：城市和日期。

那么我设计语义帧可以这么做：

```
{
    "city": null,
    "date": null
}
```

也就是说当用户inform了系统的所有必要条件，这里是city和date之后，并且DST也填充更新了语义帧，那么DPL应该就能给出对应的天气的回答，所以整个问答会类似这样：

- 用户：我要查天气
- 系统：好的要查哪个城市的？
- 用户：北京
- 系统：那么查哪天的？
- 用户：明天
- 系统：明天北京的天气是xxx

在这个过程中我们可以认为有三轮交互（用户到系统），如果写成用户行为和系统行为那么是这样的：

- User: requestWeather()
- Sys: request(city)
- User: inform(city=北京)
- Sys: request(date)
- User: inform(date=明天)
- Sys: informWeather(city=北京, date=明天)

我们分成3轮，看看语义帧的变化：

- User: requestWeather()
- State Before DST:
  - user_action_t = null
  - sys_action_t_1 = null
  - city = null
  - date = null
- State After DST:
  - user_action_t = requestWeather
  - sys_action_t_1 = null
  - city = null
  - date = null
- Sys: request(city)

在通过DST之前，我们可以认为系统是一片空白，都是null（空）

在DST之后我们可以认为DST更新了user_action，而用户行为也可以认为是自动更新的而不是DST的功劳

---

- User: inform(city=北京)
- State Before DST:
  - user_action_t = requestWeather
  - sys_action_t_1 = null
  - city = null
  - date = null
- State After DST: 
  - user_action_t = requestWeather
  - sys_action_t_1 = null
  - city = 北京
  - date = null
- Sys: request(date)

在通过DST之前，State和前一轮通过DST之后是一致的。

然后因为用户提供了“北京”这个信息，所以DST更新了city这个项。所以本质上DST在这里的作用只有一个，决定某个语义帧的一项，要不要更新。

我们的例子很简单，但是DST是有很多不能更新的时候，例如用户输入的系统没理解，或者理解的概率很低，那么DST就不应该被更新。当然此时应该有其他的语义帧来标识这种状态。

---

- User: inform(date=明天)
- State Before DST:
  - user_action_t = requestWeather
  - sys_action_t_1 = null
  - city = 北京
  - date = null
- State After DST:
  - user_action_t = requestWeather
  - sys_action_t_1 = null
  - city = 北京
  - date = 明天
- Sys: informWeather(city=北京, date=明天)

这一轮的对话基本同上。

---

我们假设一种情况，用户会说错，或者是一些重要选项其实可能是需要用户确认的情况。例如用户如果买票，但是要么语音识别出错，要么NLU出错，把“北京市”识别成了“北海市”（广西的一个市），例如用户想说：“我想去北京看北海，请问天气怎么样”，但是错误的被NLU理解成了想去北海市，或者NLU同时识别了北京市和北海市，或者这两者的置信度都比较低（NLU不确定用户想要什么），那么就应该作出一个让用户确认的操作，一般这个操作被称为confirm。我们看一下假设对话行为和状态包含了confirm会如何。

```
{
    "city": null,
    "city_confirmed": false,
    "date": null,
    "date_confirmed": false
}
```

- 用户：我要查天气
- 系统：好的要查哪个城市的？
- 用户：我想去北京看北海
- 系统：请问是北京市吗？
- 用户：是的
- 系统：那么查哪天的？
- 用户：明天
- 系统：明天北京的天气是xxx

在这个过程中我们可以认为有三轮交互（用户到系统），如果写成用户行为和系统行为那么是这样的：

- User: requestWeather()
- Sys: request(city)
- User: inform(city=北京), inform(city=北海) # 这两个行为是并列的，但是置信度不同
- Sys: confirm(city=北京)
- 用户: confirm
- Sys: request(date)
- User: inform(date=明天)
- Sys: informWeather(city=北京, date=明天)

主要变化的是下面这一步

- User: inform(city=北京), inform(city=北海) # 这两个行为是并列的，但是置信度不同
- Sys: confirm(city=北京)
- 用户: confirm

我们可以认为逻辑是这样的：假设NLU输出的结果，出现了太多不确定的内容，或者不确定性大于某个阈值，系统就可以反问用户来确定答案。

当然从系统设计上来说，系统反问次数越多，系统状态正确的可能性越大，但是系统反问越多，系统的可用性就越低，因为太长的对话本身会导致用户体验的下降。

## 是否可以无状态？

首先答案，基本上是可以的。

实际上在一些研究上的End-to-End系统中，DST本身只是以一种向量分布或者类似完全记忆化的形式存储在神经网络中，而不需要直接的定义。这不能算无状态，但是也可以算隐藏状态。

但是缺点也是显而易见的，因为并不知道状态，至少不知道状态的实际意义（因为它可能只是一个分布），所以假设它输入DPL导致错误的系统行为，我们也很难调试。
