# Agent-Skill

Claude, Codex AI 워크플로우를 맞춤 설정하는 데 유용한 Claude 스킬, 리소스 및 도구를 엄선하여 정리한 목록에서 출발한 **Python · Qt · Docker · 웹 · 딥러닝 프로젝트용 에이전트 하네스**입니다.

공통 규칙, 필요한 분야의 스킬, 선택적인 전문 에이전트, 검증 절차를 프로젝트 단위로 설치합니다. 모델 런타임이나 실제 앱을 대신하는 제품은 아닙니다. 조사 기준일은 **2026-11-02**, 하네스 버전은 **0.1.0**입니다.

## 빠른 시작

설치 도구는 **Python 3.11 이상**, 외부 Python 패키지 없이 실행됩니다. 대상 애플리케이션의 Python 버전은 기존 설정을 따릅니다.

```sh
git clone https://github.com/WooSeongYoon/Agent-Skill.git
cd Agent-Skill
python scripts/validate.py
python -m unittest discover -s tests -v

# 실제 프로젝트 경로로 바꿉니다. 첫 실행은 파일 변경 없는 미리보기입니다.
python scripts/install.py --target ../my-project --profiles qt ml docker

# 미리보기와 같은 선택에 --apply를 추가합니다.
python scripts/install.py --target ../my-project --profiles qt ml docker --apply
```

PR이 아직 main에 병합되지 않았다면 clone 후 `git switch feat/project-agent-harness`로 구현 브랜치를 선택하세요. 경로에 공백이 있으면 따옴표로 감쌉니다. Windows에서는 환경에 따라 `python` 대신 `py -3.11`을 사용할 수 있습니다.

모든 분야와 선택적 전문 에이전트를 설치하려면:

```sh
python scripts/install.py --target ../my-project --profiles full --with-agents
python scripts/install.py --target ../my-project --profiles full --with-agents --apply
```

기본 도구는 Codex와 Claude 둘 다입니다. 하나만 쓸 경우 `--tools codex` 또는 `--tools claude`를 추가합니다. 전체 프로필을 항상 설치하기보다 프로젝트에 필요한 프로필을 고르는 편이 좋습니다.

## 프로필

모든 프로필에 `project-discovery`, `debug-root-cause`, `verify-change`가 포함됩니다.

| 프로필 | 추가 스킬 | 예시 |
|---|---|---|
| python | python-engineering | Python 라이브러리, CLI, 백엔드 |
| qt | python-engineering, qt-desktop | PySide/PyQt GUI |
| docker | docker-workflow | Dockerfile, Compose |
| web | web-development | 기존 웹 UI/API 프로젝트 |
| ml | python-engineering, deep-learning | 학습·평가·추론 |
| full | 위 분야 전체 | 여러 분야를 관리하는 프로젝트 |

`--profiles web python docker`처럼 조합합니다. 공통 Python 스킬은 중복 설치되지 않습니다. Qt 바인딩, 웹 프레임워크, ML 프레임워크, 모델 이름과 GPU를 설치기가 임의로 결정하지 않습니다.

## 설치 결과

| 경로 | 역할 |
|---|---|
| `AGENTS.md` | 공통 작업 규칙과 스킬 선택 기준 |
| `CLAUDE.md` | `@AGENTS.md`로 공통 규칙을 불러오는 Claude 진입점 |
| `.agents/skills/` | Codex 프로젝트 스킬 |
| `.claude/skills/` | Claude 프로젝트 스킬 |
| `.codex/agents/*.toml` | 선택적 Codex 전문 에이전트 |
| `.claude/agents/*.md` | 선택적 Claude 전문 에이전트 |
| `.harness/project.json` | 확인할 프로젝트 사실과 검증 명령 |
| `.harness/instructions.md` | 기존 지침과 수동 병합할 때 사용할 공통 규칙 |
| `.harness/installed.json` | 설치 버전·선택 사항·파일 SHA-256 기록 |

설치 후 에이전트에게 다음처럼 요청하세요.

> project-discovery를 사용해 이 프로젝트의 기술 스택과 CI를 확인하고 .harness/project.json에 검증된 사실과 명령을 기록해줘. 미확인 값은 추측하지 말아줘.

파일이 설치되었다는 사실과 호스트가 스킬을 인식했다는 사실은 다릅니다. Codex의 스킬 목록, Claude의 스킬/에이전트 목록에서 확인하고 대표 요청을 실행하세요. 자세한 경로와 호환성은 [CODEX.md](CODEX.md)에 있습니다.

## 기존 프로젝트와 업데이트

설치기는 **미리보기 기본**, **기존 파일 덮어쓰기 금지**, **동일 파일 재실행 시 변경 없음** 정책입니다. 충돌이 하나라도 있으면 쓰기 전에 중단합니다. 심볼릭 링크와 경로 이탈은 거부합니다. 사용자 전역 설정, MCP 서버, API 키, 권한 모드, Git 상태를 자동 변경하지 않습니다.

이미 AGENTS.md/CLAUDE.md가 있다면 다음 옵션으로 스킬만 추가하고 `.harness/instructions.md`의 필요한 규칙을 기존 지침에 수동 병합합니다.

```sh
python scripts/install.py --target ../my-project --profiles qt ml --skip-instructions
python scripts/install.py --target ../my-project --profiles qt ml --skip-instructions --apply
```

`--skip-instructions`에서는 새 공통 규칙의 자동 로딩을 보장하지 않습니다. 기존 AGENTS.md에 규칙을 통합하고, Claude에는 기존 CLAUDE.md에서 필요한 파일을 import하세요. 기존 스킬과 `.harness` 파일의 충돌까지 우회하는 옵션은 아닙니다.

사용자가 프로젝트 사실이나 스킬을 수정한 뒤에는 재설치가 충돌을 보고할 수 있습니다. 업데이트/프로필 추가는 **빈 임시 대상에 새 버전을 설치 → diff 검토 → 프로젝트 브랜치에서 필요한 변경만 병합**합니다. 강제 덮어쓰기나 자동 삭제는 제공하지 않습니다. 전원 차단까지 보장하는 다중 파일 트랜잭션은 아니므로 중단된 설치는 diff를 확인하세요.

## 문서와 검증

- [설계 분석 및 참고 저장소 비교](docs/analysis.md)
- [실제 프로젝트 적용 절차](docs/project-adoption.md)
- [평가 방법과 현재 검증 범위](evals/README.md)
- [참고 자료와 사용 방식](THIRD_PARTY_NOTICES.md)
- [조사 revision 기록](docs/sources.json)

```sh
python scripts/render_agents.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
```

역할 원본 `agents/*.md`를 바꾸면 `python scripts/render_agents.py`로 두 호스트용 파일을 생성합니다. CI는 Linux/Windows, Python 3.11/3.12에서 구조 검사와 설치 테스트를 실행하도록 구성되어 있습니다. CI 설정의 존재만으로 실행 성공을 주장하지 않습니다.

실제 Qt GUI·Docker daemon·브라우저·CUDA·전체 학습은 이 저장소의 단위 테스트 대상이 아닙니다. 각 애플리케이션에 적용한 뒤 그 프로젝트의 테스트와 수용 기준으로 검증해야 합니다.
