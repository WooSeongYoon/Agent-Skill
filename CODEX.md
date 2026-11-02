# Codex·Claude 사용 안내

이 파일은 **사람을 위한 설명서**입니다. `CODEX.md`, `codex.md`, `agent.md`가 Codex의 기본 자동 지침 파일이라고 가정하지 않습니다. 공통 지침은 정확한 이름 `AGENTS.md`를 사용합니다.

## 호스트별 인식 위치

| 내용 | Codex | Claude Code |
|---|---|---|
| 프로젝트 지침 | AGENTS.md, 필요한 하위 경로 지침 | CLAUDE.md 및 지원 버전/설정의 AGENTS.md |
| 프로젝트 스킬 | .agents/skills/name/SKILL.md | .claude/skills/name/SKILL.md |
| 사용자 스킬 | ~/.agents/skills | ~/.claude/skills |
| 프로젝트 전문 에이전트 | .codex/agents/name.toml | .claude/agents/name.md |
| 스킬 UI 메타데이터 | 스킬 안의 agents/openai.yaml | 공통 SKILL.md 사용 |

스킬 내부의 `agents/openai.yaml`은 스킬의 표시/호출 메타데이터이며 독립 subagent 정의가 아닙니다. 루트 `AGENTS.md`도 에이전트 목록이 아니라 프로젝트 지침입니다.

Codex는 전역 지침 이후 저장소 루트에서 현재 작업 디렉터리까지 지침을 구성하며, 같은 디렉터리에서는 `AGENTS.override.md`가 `AGENTS.md`보다 우선합니다. 무조건 모든 하위 폴더 지침이 로드된다고 가정하지 말고 실행 경로를 확인합니다.

현재 Claude Code는 조건에 따라 AGENTS.md를 직접 지원합니다. 이 하네스는 버전·설정 차이를 줄이기 위해 명시적인 `CLAUDE.md`의 `@AGENTS.md` import를 유지합니다. 최신 버전에서도 이 방식을 지원한다는 공식 문서를 확인했습니다.

## 스킬과 에이전트 확인

설치한 프로젝트에서 Codex 스킬 목록을 확인하고 `$qt-desktop`처럼 명시적으로 요청할 수 있습니다. Claude에서는 `/qt-desktop`처럼 호출합니다. 호스트의 사용 가능한 명령과 UI는 설치 버전에 맞게 확인합니다.

전문 에이전트는 `--with-agents`로 선택 설치합니다. 3개 역할은 code-reviewer, failure-analyst, ml-reviewer입니다. 모델 이름과 reasoning effort를 강제하지 않아 현재 세션 설정을 따릅니다.

Claude 정의는 Read/Grep/Glob만 허용합니다. Codex 정의의 '수정하지 않는다'는 역할 지침은 읽기 전용 샌드박스를 만드는 설정이 아닙니다. Codex custom agent는 부모의 권한을 상속하므로 실제 접근 제어는 부모 세션에서 설정해야 합니다. 이 설치기는 권한을 변경하지 않습니다.

## 예시 요청

- `qt-desktop과 python-engineering을 사용해 이 취소 버튼 문제를 재현하고 최소 수정해줘. 창 종료까지 검증해줘.`
- `deep-learning을 사용해 train/validation/test 분할과 전처리 누수를 확인해줘. 전체 학습은 실행하지 마.`
- `code-reviewer에게 이 diff의 실제 회귀 위험만 검토하도록 맡겨줘. 수정은 하지 마.`

## 출처

2026-11-02 확인:

- [Codex 프로젝트 지침](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [스킬 작성·검색 위치](https://learn.chatgpt.com/docs/build-skills)
- [Codex 전문 에이전트](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Claude 프로젝트 메모리](https://code.claude.com/docs/en/memory)
- [Claude 스킬](https://code.claude.com/docs/en/skills)
- [Claude 전문 에이전트](https://code.claude.com/docs/en/sub-agents)
