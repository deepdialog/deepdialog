# Chatbot

这里Chatbot特指中文的闲聊机器人

闲聊机器人是带有一定“娱乐”意味的机器人。当然也可以用作例如心理辅导，心理帮助，婴幼儿教育，儿童陪伴等等内容。

这部分就不是完成一个任务，不是需要答案，而更多的是陪伴、娱乐、放松。一个Chatbot最简单的成功指标就是，本质是鼓励用户多和Chatbot交流，用户使用时长和用户下次继续使用的意愿，如果用户愿意一直陪着Chatbot聊天，那就成功了。

一般来说Chatbot只有两种技术，template-based，neural-based，另外我们可以认为一些类似FAQ的QA对也是闲聊机器人实现的一种基本方式，它本质上类似template-based系统。

## template-based

也就是根据模板来选择回答

最简单的模板例如：

```
用户：你喜欢 * 吗？
系统：我喜欢 * 啊，你喜欢吗？
系统：我喜欢 * 啊，你还喜欢什么别的吗？

用户：你吃过 * 吗？
系统：我是机器人，不吃 *
系统：* 好吃吗？你告诉我呗

用户：你觉得 * 怎么样？
系统：这取决于你对 * 的理解，我不好回答啊
系统：我觉得 * 还不错吧，你怎么看？
```

可以看出，上面模板的`*`可以代指很多东西

当然实际应用上，模板可能比上面复杂的多，可以解决更多问题，设置算术题，计算，递归等等

这方面比较完整的研究是AIML语言，即 Artificial Intelligence Markup Language 语言。

是一种XML格式的标记语言，这部分方法也曾经是试图解决图灵测试的主力研究方法。

更多内容可以参考：

[Wikipedia AIML](https://en.wikipedia.org/wiki/AIML)

[AIML tutorial](https://www.tutorialspoint.com/aiml/index.htm)

## neural-based

是以神经机器翻译模型为参考，用来生成对话的模型。即基于深度学习的 sequence-to-sequence 模型（或变种），来生成对话。

这类模型直接训练对话，得到端到端的结果。训练数据大部分来自于电影字幕、社交媒体，或者其他已有的对话数据。

这方便比较前沿的研究如

Deep Reinforcement Learning for Dialogue Generation [Li et al., 2016]

Adversarial Learning for Neural Dialogue Generation [Li et al., 2017]
