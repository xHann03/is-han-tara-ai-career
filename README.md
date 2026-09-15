# is-han-tara-ai-career

面向文科、文商科、艺术类和其他非技术背景用户的 AI 职业路径咨询 Skill。它也能处理“先用 AI 赋能原专业、研究或自媒体”的探索请求，并在用户准备求职时把实践翻译成职业证明。

## 安装

把整个文件夹复制到：

```text
~/.codex/skills/is-han-tara-ai-career
```

安装后重启 Codex。在对话中可以直接描述背景，也可以明确说“使用 `$is-han-tara-ai-career`”。

## 主要入口

- `SKILL.md`：触发范围、路由和核心工作流。
- `references/`：岗位地图、诊断、对话风格、探索边界与真人接力。
- `eval/`：36 个真实问题、7 个多轮场景和 17 项评估标准。
- `scripts/validate_skill_package.py`：不上传资料、不调用模型的本地检查。

## 本地验证

先检查 Skill 格式：

```bash
python3 ~/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/is-han-tara-ai-career
```

再检查包内链接、测试集编号和关键边界：

```bash
python3 scripts/validate_skill_package.py
```

这两项只验证结构和指令覆盖，不能代替真实对话测试。行为回归应使用不含预期答案的用户问题独立生成回答，再由 `eval/expected-properties.md` 评分；涉及内部资料时优先使用本地模型或人工盲评，不把整个资料库发送给未经确认的第三方服务。

## 当前边界

- 不提供算法工程学习路线。
- 不把模型输出当实时招聘、薪资或公司信息。
- 不提供医疗、法律等专业决策；相关内容必须回到权威来源并由人复核。
- 不编造 is涵 的经历、邀请码、回复时间、内推或录用承诺。
