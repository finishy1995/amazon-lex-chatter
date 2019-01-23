# Lex 聊天机器人

使用 Amazon Lex 快速制作聊天机器人，DEMO 如下场景：
- 语句模糊识别
- 条件判断
- 聊天顺序切换
- 问题指引和重试机制
- 设置机器人喜好，根据喜好选择答案

## 使用方式

- 在 Amazon Lex 中导入 Bots 文件 Chatter_Export.json
- 在 Amazon Lambda 中导入 lambda 函数文件 lambda_function.py，并设置运行环境为 python 2.7

## 其他文件

- main.py 用于本地测试
- sample.py AWS 官方 Lex lambda 示例
- YesNo_Export.json 自定义 Slots 模版
- Zoo_Export.json Intent 模版
