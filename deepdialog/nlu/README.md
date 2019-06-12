# NLU

输入一句用户的自然语句(utterance)，输出对应的Domain，Intent，Slots

```python
class NaturalLanguageUnderstanding(object):
    def forward(self, utterance: str) -> UserAction:
        user_action = UserAction()
        # 处理逻辑
        return user_action
```
