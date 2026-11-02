# 참고 자료와 작성 방식

이 저장소의 구현과 지침은 사용자 요구에 맞게 독립적으로 작성되었습니다. 아래 프로젝트의 개념과 구조를 비교했으며 외부 스킬·스크립트 원본을 vendoring하지 않았습니다. 외부 초기화/검증 도구는 작성 과정에만 사용하고 저장소에는 포함하지 않았습니다.

- [Karpathy 지침 모음](https://github.com/multica-ai/andrej-karpathy-skills): 코딩 행동 원칙 참고. 이는 해당 저장소의 정리이며 Karpathy의 공식 배포물이라고 가정하지 않습니다.
- [Composio 스킬 카탈로그](https://github.com/ComposioHQ/awesome-claude-skills): 스킬 분류와 웹 테스트 사례 비교.
- [Anthropic 스킬](https://github.com/anthropics/skills): 공통 포맷과 스킬별 리소스 구조 참고.
- [Superpowers](https://github.com/obra/superpowers): 디버깅·검증·리뷰 흐름 참고.
- [OpenAI Skills](https://github.com/openai/skills), [OpenAI Plugins](https://github.com/openai/plugins): 기존 자료의 폐기 안내와 현재 배포 구조 비교.
- [Agent Skills](https://github.com/agentskills/agentskills): 공개 포맷과 검증 기준 참고.

확인한 revision은 [sources.json](docs/sources.json)에 있습니다. 링크는 원본 라이선스를 변경하지 않습니다. 추후 실제 파일을 복사한다면 해당 파일의 라이선스, 저작권 표시와 NOTICE 요구를 확인하고 보존해야 합니다. 특히 공식 스킬 저장소도 모든 하위 디렉터리에 동일한 라이선스를 적용하지 않습니다.

원본 저장소에는 루트 LICENSE가 없었습니다. 이번 변경에서 소유자를 대신해 공개 라이선스를 새로 부여하지 않았습니다.
