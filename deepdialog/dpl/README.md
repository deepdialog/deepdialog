# Dialog Policy

对话决策模块

输入一个当前对话状态，输出一个系统行为

```python
class DialogPolicyLearning(object):
    def forward(self,
                history: List[DialogState]) -> SystemAction:
        system_action = SystemAction()
        return system_action
```

## 输出

根据当前的DialogState要列出潜在是system action列表这个列表里面的action如果是基于system call的，还需要获取对应的程序返回结果，这个结果也要融合到决策过程里面