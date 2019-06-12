# DeepDialog

[![DeepDialog](https://img.shields.io/badge/-DeepDialog-blue.svg)](https://github.com/deepdialog/deepdialog)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.com/deepdialog/deepdialog.svg?branch=master)](https://travis-ci.com/deepdialog/deepdialog)
[![codecov](https://codecov.io/gh/deepdialog/deepdialog/branch/master/graph/badge.svg)](https://codecov.io/gh/deepdialog/deepdialog)

一个非常简易的，基于机器学习与数据驱动的对话系统原型

[对话标注工具](https://deepdialog.github.io/dialog-label/)
[简易的Wechaty-Python-Client](https://github.com/deepdialog/wechaty-as-a-service)

## Requirement

`Python >= 3.6`

### Python Dependency

```text
keras
tensorflow
pyyaml
joblib
scikit-learn
tqdm
numpy
pandas
scipy
```

## 系统流程

```
User --> LU --> DST
   \            /
     NLG <-- DP <-- DB
```

## Usage

可以clone整个项目，然后项目的`examples/simplest`是一个简单的对话机器人数据样例

训练：

```bash
$ python3 -m deepdialog.train ./examples/simplest/ /tmp/simplest_model
```

服务于控制台

```bash
$ python3 -m deepdialog.serve /tmp/simplest_model/
```
