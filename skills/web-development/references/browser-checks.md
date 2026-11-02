# 웹 검증

| 대상 | 확인할 동작 |
|---|---|
| 폼 | 유효/무효 입력, 제출 중 중복 클릭, 오류 표시, 키보드 |
| API 화면 | 로딩, 빈 응답, 타임아웃, 실패 후 재시도, 권한 없음 |
| 라우트 | 직접 접근, 새로고침, 링크 이동, 뒤로 가기 |
| 레이아웃 | 모바일 폭, 데스크톱 폭, 긴 한국어, 확대, 초점 표시 |

E2E는 변경한 중요한 흐름에 집중한다. HTML 문자열 존재 검사만으로 상호작용을 입증하지 않는다. 실제 DOM을 확인한 뒤 locator를 정한다. 허용된 테스트 계정과 로컬/스테이징 환경을 사용한다.

[Playwright assertions](https://playwright.dev/docs/test-assertions), [페이지 준비 상태 API](https://playwright.dev/docs/api/class-page#page-wait-for-load-state)
