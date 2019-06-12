
# Papers

## Natural Language Understanding 自然语言理解

自然语言理解任务（Natural Language Understanding），也被称为SLU（Spoken LU）或者（LU），或语义解码（Semantic Decoding）。

NLU一般分为两个子任务：意图识别（Intent Detection）、槽识别（Slot Filling）。

意图识别是一个分类任务，所以总体思路和一般的文本分类（Text Classification）或者短文本分类（Short TC）的解决思路基本一致。

槽识别是一个识别任务，类似抽取任务，所以一般方法和命名实体识别（Named Entity Recognization）任务基本一致。

### 发展（2019）

主流的发展方向有以下几个：

1. 联合意图识别和槽识别，放入同一模型，互相增加准确率
2. 从语音开始，而不是从文字开始，因为对话系统往往基于语音，语音识别本身就带来了很多错误，联合语音信息可以保留更多信息
3. End-to-End的方式进行Fine-Tune，即不仅仅联合意图识别和槽识别，也同时连接后面的DST、DPL甚至NLG模型，共同训练。

## Dialog State Tracking 对话状态跟踪

也叫Belief Tracking

Neural Belief Tracker: Data-Driven Dialogue State Tracking
[Nikola Mrksić et al., 2016]

Fully Statistical Neural Belief Tracking
[Nikola Mrksić et al., 2018]


    In slot-based spoken Dialogue systems, tracking the entities in context can be cast as slot carryover task - only the relevant slots from the dialogue context are carried over to the current turn.

[Improving Long Distance Slot Carryover in Spoken Dialogue Systems](https://arxiv.org/pdf/1906.01149.pdf)
[Chen et al., 2019]

## Dialog Policy 对话策略

## Natural Language Generation 自然语言生成

## Question Answering System 问答系统

[Training Neural Response Selection for Task-Oriented Dialogue Systems](https://arxiv.org/pdf/1906.01543.pdf)
[Henderson et al., 2019]

对于简单的FAQ问答，也可以被称为 Question Answering Pairing 或者 Neural Response Selection 问题

[One-Shot Learning for Text-to-SQL Generation](https://arxiv.org/pdf/1905.11499.pdf)
[Lee et al., 2019]

[FAQ Retrieval using Query-Question Similarity and BERT-Based Query-Answer Relevance](https://arxiv.org/pdf/1905.02851.pdf)
[Wataru Sakata et al., 2019]


[A Context-aware Natural Language Generator for Dialogue Systems](https://arxiv.org/pdf/1608.07076.pdf)
[Duˇsek et al., 2016]

### Knowledge Based Question Answering 基于知识的问答

## End-to-End System 端对端系统

