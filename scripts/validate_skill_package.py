#!/usr/bin/env python3
"""Run deterministic, offline checks for this Skill package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(1)


def read(relative: str) -> str:
    path = ROOT / relative
    if not path.is_file():
        fail(f"missing {relative}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    skill = read("SKILL.md")
    if not skill.startswith("---\n"):
        fail("SKILL.md has no YAML front matter")
    if "name: is-han-tara-ai-career" not in skill:
        fail("unexpected skill name")
    if "description:" not in skill:
        fail("missing skill description")

    markdown_targets = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", skill)
    for target in markdown_targets:
        if not (ROOT / target).is_file():
            fail(f"broken SKILL.md link: {target}")

    queries = read("eval/real-user-queries.md")
    question_numbers = [
        int(value)
        for value in re.findall(r"(?m)^(\d+)\.\s", queries)
    ]
    expected_numbers = list(range(1, 37))
    if question_numbers != expected_numbers:
        fail(f"query numbering is {question_numbers}, expected 1..36")

    scenarios = read("eval/conversation-scenarios.md")
    scenario_count = len(re.findall(r"(?m)^## 场景", scenarios))
    if scenario_count != 7:
        fail(f"found {scenario_count} scenarios, expected 7")

    rubric = read("eval/expected-properties.md")
    rubric_numbers = [
        int(value)
        for value in re.findall(r"(?m)^(\d+)\.\s\*\*", rubric)
    ]
    if rubric_numbers != list(range(1, 18)):
        fail(f"rubric numbering is {rubric_numbers}, expected 1..17")

    corpus = "\n".join(
        [
            skill,
            read("references/onboarding-and-dialogue.md"),
            read("references/diagnosis-framework.md"),
            read("references/output-patterns.md"),
            read("references/domain-exploration.md"),
            read("references/human-handoff.md"),
        ]
    )
    required_phrases = {
        "one-question pacing": "默认每轮只问一个",
        "domain routing": "先让 AI 进入自己的专业与创作",
        "source verification": "权威来源",
        "privacy boundary": "隐私",
        "human handoff": "Tara ID：942086",
        "no repeated unanswered question": "不得在后续轮次再次询问同一未知项",
        "goal is not result": "不得把“为了降低标注歧义，更新了手册”改写为",
        "multi-turn checkpoint": "阶段性路径快照",
        "no workflow inference": "不把“这类项目通常会做”当成“用户做过”",
        "checkpoint evidence action": "1–3 天能完成的最小证据动作",
        "no repeated handoff": "不要因为给了阶段性快照就再次展示真人入口",
        "no follower-count cold-start inference": "账号有粉丝不等于做过冷启动",
        "preserve team voice": "默认保留团队口径",
        "turn-four checkpoint": "最晚在第 4 个用户回合的回复中",
    }
    for label, phrase in required_phrases.items():
        if phrase not in corpus:
            fail(f"missing {label}: {phrase}")

    print(
        "PASS: valid package links; 36 queries; 7 scenarios; "
        "17 rubric items; core safety, evidence, pacing, and handoff directives present."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
