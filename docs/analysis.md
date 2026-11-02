# Python·Qt·Docker·웹·딥러닝용 에이전트 하네스 설계 분석

분석 기준일: **2026-11-02**. 실제 확인한 저장소 revision은 [sources.json](sources.json)에 기록했습니다. 사용자의 저장소는 main에 짧은 README만 있는 상태에서 시작했습니다. 실제 애플리케이션 저장소와 운영 조건은 제공되지 않았습니다.

## 1. 목표와 완료 기준

목표는 여러 프로젝트에서 Codex와 Claude가 일관되게 작업하도록 공통 원칙과 분야별 실행 절차를 제공하는 것입니다. 이 하네스는 모델 실행 엔진, 자동 배포 시스템, 데이터셋 또는 완성된 Qt/웹 앱을 포함하지 않습니다.

첫 버전의 완료 기준은 다음과 같습니다.

1. Python·Qt·Docker·웹·딥러닝 작업에 맞는 스킬을 선택 설치할 수 있다.
2. 공통 지침과 호스트별 파일 경로가 실제 공식 동작에 맞는다.
3. 기존 프로젝트 지침과 사용자 수정을 덮어쓰지 않는다.
4. 설치·구조·참조·에이전트 설정을 자동 검증할 수 있다.
5. 대표 요청에서 스킬이 유용한 판단을 유도하는지 별도 평가한다.
6. 참고한 자료와 확인한 revision, 실제 실행하지 못한 범위를 기록한다.

## 2. 참고 저장소 비교

| 자료 | 확인한 내용 | 채택한 설계 판단 | 그대로 적용하지 않은 부분 |
|---|---|---|---|
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | 짧은 코딩 행동 원칙, CLAUDE.md와 스킬 형태 | 요구·가정·완료 기준, 최소 수정, 단순성 | 원문 전체 복사, 모든 작은 작업에서 질문으로 중단 |
| [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) | 광범위한 스킬 카탈로그, 앱 연동, webapp-testing 사례 | 스킬 탐색과 비교의 출발점, 독립적인 작업 단위 | 대량 설치, 사용하지 않는 외부 서비스 연결과 자격 증명 |
| [anthropics/skills](https://github.com/anthropics/skills) | 공식 스킬 구조, 문서/웹 테스트 사례, 스킬별 라이선스 차이 | SKILL.md와 필요한 참고 파일을 분리 | 문서용 스킬 등 현재 개발 범위 밖의 기능 |
| [obra/superpowers](https://github.com/obra/superpowers) | 개발 계획·디버깅·검증·리뷰를 연결하는 작업 방식 | 재현 가능한 디버깅, 검증 근거, 역할 분리 | 작은 수정까지 일률적인 승인·TDD·병렬 에이전트 강제 |
| [openai/skills](https://github.com/openai/skills) | README에서 deprecated 및 openai/plugins 이전 안내 | 기존 자료를 현재 권장 경로와 구분 | 오래된 설치 안내를 최신 사실로 사용 |
| [openai/plugins](https://github.com/openai/plugins) | 최신 Codex 플러그인 예제, skill/agent/connector 묶음 구조 | 향후 배포 단위로 확장 가능한 구조 | 현재 필요 없는 marketplace, MCP, 훅 자동 설치 |
| [agentskills/agentskills](https://github.com/agentskills/agentskills) | Agent Skills 표준과 참조 검증 구현 | name·description, 폴더 명명, 점진적 로딩 | 제품 확장을 공통 표준 필드로 오해 |

이 비교는 별점 순위표가 아닙니다. 인기 있는 자료도 기술적 정확성, 현재 유지 상태, 라이선스와 프로젝트 적합성을 별도로 확인해야 합니다. 이 저장소의 문장과 코드는 목적에 맞게 독립적으로 작성했으며 외부 저장소를 통째로 복제하지 않았습니다.

실제 비교 중 Composio/Anthropic webapp-testing 예제에서 networkidle 대기를 강하게 요구하는 지침을 확인했습니다. [Playwright 공식 API](https://playwright.dev/docs/api/class-page#page-wait-for-load-state)는 테스트 준비 상태를 web assertion으로 확인하도록 안내합니다. 따라서 이 하네스는 locator와 관측 가능한 상태 검증을 채택했습니다. 카탈로그의 권장 절차를 공식 API와 대조해야 하는 구체적인 사례입니다.

## 3. 파일의 역할을 구분하는 이유

| 계층 | 담을 내용 | 담지 않을 내용 |
|---|---|---|
| AGENTS.md | 공통 작업 원칙, 검증·보고 기준 | 모든 프레임워크의 장문 매뉴얼 |
| CLAUDE.md | 공통 지침 import, Claude 탐색 위치 | AGENTS.md와 별도로 관리하는 중복 정책 |
| SKILL.md | 특정 요청의 입력, 작업 순서, 결과, 실패 처리 | 프로젝트와 무관한 기능 모음 |
| references/ | 필요할 때 읽는 상세 조건과 공식 링크 | 매 작업에 항상 주입할 대량 문서 |
| agents/ | 별도 역할의 분석 범위·출력 계약 | 실제 존재하지 않는 도구나 권한 |
| 프로젝트 사실 | 실제 버전, 실행 명령, 장치·서비스 조건 | 추정한 프레임워크와 성공하지 않은 명령 |
| 검증/CI | 결정적으로 검사 가능한 규칙 | 프롬프트 문장만으로 강제된다고 주장하는 보안 |

`CODEX.md`는 자동 로딩 파일이 아니라 사용 안내입니다. 공식 자동 지침 이름은 AGENTS.md이며, custom agent 정의와 스킬 UI 메타데이터는 별개의 형식입니다. 최신 Claude의 AGENTS.md 지원과 과거 버전의 차이도 고려해 명시적 import를 사용합니다. 상세 경로는 [CODEX.md](../CODEX.md)를 참고하세요.

## 4. 원본과 설치본

원본 스킬은 `skills/`, 원본 역할은 `agents/`에만 작성합니다. 설치 시 Codex에는 `.agents/skills/`, Claude에는 `.claude/skills/`로 복사합니다. 역할은 원본에서 TOML/Markdown 어댑터를 생성합니다.

이 방식은 심볼릭 링크가 필요한 Windows 권한 문제를 피합니다. 대신 설치본은 독립 복사본이므로 자동으로 최신화되지 않습니다. 같은 설치는 내용이 같으면 변경하지 않고, 다른 내용이 있으면 중단합니다. 업데이트는 새 디렉터리에 생성한 뒤 diff를 검토하여 병합합니다. 하나의 원본을 유지하는 이점과 명시적인 업데이트 비용을 선택한 설계입니다.

프로필은 설치 단계에서 필요한 분야를 고르는 장치입니다. 모델을 대신해 매 요청을 강제로 분류하는 라우터가 아닙니다. 실제 스킬 선택은 호스트의 metadata 검색과 사용자 명시 호출을 따릅니다.

## 5. 분야별 설계

### Python

Python 3, 프로젝트 지원 버전, 기존 패키지 관리자·잠금 파일을 기준으로 합니다. 함수·dataclass·합성, 명시적인 속성 접근, f-string/join, 필요한 타입 힌트와 좁은 예외 처리를 기본으로 합니다. Mixin과 다중 상속을 기본 구조로 도입하지 않습니다.

테스트는 실행 경계와 계약을 확인합니다. 버그 수정에는 재현 조건을, API 변경에는 호출자 호환성을 검사합니다. 프로젝트에 없는 lint/type 도구를 무조건 설치하는 대신 기존 CI를 먼저 읽습니다.

### Qt

PySide와 PyQt, Widgets와 QML을 먼저 구분합니다. 긴 추론·I/O·연산은 GUI 이벤트 루프에서 분리하고 위젯 갱신은 GUI 스레드에 둡니다. QThread 객체의 affinity와 실제 실행 스레드를 혼동하지 않도록 합니다.

단순히 worker를 추가하는 것으로 끝내지 않습니다. 중복 실행, 진행률, 실패, 취소, 창 닫기, 객체 해제까지 하나의 수명주기로 봅니다. blocking slot이 실행 중이면 queued cancel이 늦어질 수 있으므로 협력적인 취소를 확인합니다. [Qt 공식 QThread 문서](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html)를 근거로 합니다.

### Docker

Python/웹 실행 환경과 GUI 배포 환경을 나눕니다. 잠금 파일, 작은 베이스, .dockerignore, 필요한 경우 multi-stage, 비루트 실행과 signal 종료를 확인합니다. 빌드 시크릿을 ARG/ENV/COPY에 넣지 않습니다.

Compose 문법 검사, 이미지 빌드, 실제 기동은 각각 다른 성공 기준입니다. GPU 환경은 호스트 드라이버·CUDA·프레임워크의 호환 조건을 확인해야 하며 임의 버전을 고정하지 않습니다. [Docker 권장 사항](https://docs.docker.com/build/building/best-practices/)과 [시크릿 문서](https://docs.docker.com/build/building/secrets/)를 참고합니다.

### 웹

React/Next/Vue/FastAPI 등 특정 프레임워크를 강제하지 않습니다. 기존 라우트, API 계약, 디자인과 잠금 파일을 유지합니다. loading/empty/error/success, 키보드·초점·반응형 동작을 수용 기준에 넣습니다.

빌드와 정적 검사 뒤에 실제 브라우저의 변경 흐름을 검증합니다. API 권한 검사와 클라이언트 표시를 구분하며, 클라이언트 번들에 시크릿이 들어가지 않게 합니다.

### 딥러닝

PyTorch를 예시로 상세 규칙을 제공하되 TensorFlow 등 기존 프레임워크를 우선합니다. 데이터/모델/실험/추론을 분리하고 데이터 분할과 전처리 누수를 먼저 검사합니다.

shape/dtype/device/loss 계약 → 작은 배치의 forward/backward → 작은 데이터 학습 → checkpoint 복원 → 추론 → 정해진 예산의 전체 실험 순으로 검증 범위를 넓힙니다. seed만으로 버전·장치 간 동일 결과를 보장하지 않습니다. [PyTorch 재현성 문서](https://docs.pytorch.org/docs/stable/notes/randomness.html)를 참고합니다.

### Qt + AI + Docker를 함께 쓸 때

GUI는 작업 요청과 결과 표시를 담당하고 모델 코어는 Qt 위젯에 의존하지 않게 합니다. 모델 로딩, 취소 가능한 추론 작업, 결과 변환을 명시적으로 연결합니다. Python의 CPU 연산, GPU 연산, 네트워크 I/O를 같은 병렬 처리 방식으로 다루지 않습니다.

컨테이너 안의 headless 테스트와 데스크톱 OS의 화면 검증은 별개입니다. CPU 테스트를 CUDA 검증으로, 작은 데이터 수렴을 실제 모델 품질로 확대 해석하지 않습니다.

## 6. 전문 에이전트는 선택 기능

기본 작업은 한 에이전트가 이해→수정→검증까지 수행합니다. 독립 검토가 필요할 때 code-reviewer, 실패 분석량이 많을 때 failure-analyst, 데이터·평가 코드의 검토가 필요할 때 ml-reviewer를 사용합니다.

역할을 늘리는 것만으로 품질이 높아지지는 않습니다. 파일 소유권 충돌, 중복 조사, 결과 검증 비용이 생깁니다. 분리된 요청과 근거 반환이 있어야 유용합니다. 이 세 역할은 분석용이고 제품 코드를 수정하지 않도록 작성했습니다. Claude의 도구 제한과 Codex의 부모 권한 상속 차이는 [사용 안내](../CODEX.md)에 명시했습니다.

## 7. 검증 구조

검증은 네 층을 구분합니다.

1. **형식:** 메타데이터, 스킬 목록, 로컬 링크, 본문 크기, 어댑터의 원본 일치 여부.
2. **설치 동작:** 미리보기 무변경, 동일 설치 재실행, 충돌 시 무변경, 사용자 파일 보존, 링크·경로 보호.
3. **모델 행동:** 실제 요청과 예제 코드로 스킬 선택과 판단을 관찰. 자동 형식 검사가 이 평가를 대신하지 않음.
4. **제품 수용:** 사용자의 실제 Qt/웹/ML/Docker 환경에서 실행해 기능과 성능을 검증.

현재 저장소의 CI는 1·2를 자동화합니다. 3을 위한 14개 평가 시나리오와 Qt/ML 정적 코드 사례를 포함합니다. 현재 관측 결과와 미검증 범위는 [평가 문서](../evals/README.md)에 기록합니다. 실제 앱이 제공되어야 4를 완료할 수 있습니다.

## 8. 유지보수와 다음 확장 기준

- 실패 사례가 반복되면 관련 스킬 한 곳만 보완하고 해당 평가를 추가합니다.
- 공식 호스트 문서가 바뀌면 경로/스키마와 어댑터를 먼저 점검하고 조사 revision을 기록합니다.
- 어떤 스킬이 과도하게 발동하면 description의 경계와 부정 사례를 수정합니다.
- 팀 배포와 버전 관리가 필요해지면 현재 스킬을 검증된 plugin manifest로 포장합니다.
- 실제로 반복 실행할 명령이 확정되면 프로젝트 CI나 hook에 연결합니다. 일반 셸 문자열 차단 목록을 보안 경계처럼 추가하지 않습니다.
- 버전별 API, 모델 이름, GPU 조합을 확인 없이 하드코딩하지 않습니다.

첫 버전에서 가장 중요한 추가 입력은 실제 프로젝트의 의존성/CI, Qt 바인딩과 대상 OS, 웹 프레임워크, ML 프레임워크·GPU·데이터 분할 기준입니다. 이 값이 채워져야 범용 지침이 프로젝트의 구체적인 실행 규칙으로 완성됩니다.
