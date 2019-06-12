# DST

对话状态更新模块

输入一个当前对话状态和NLU的输出，输出一个新的对话状态

```python
class DialogStateTracker(object):
    def forward(self,
                init_state: DialogState,
                history: List[DialogState],
                user_action: UserAction) -> DialogState:
        new_ds = DialogState()
        return new_ds
```

DST的主要问题是如何更新当前对话状态
