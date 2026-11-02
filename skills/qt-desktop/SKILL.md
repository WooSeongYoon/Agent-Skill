---
name: "qt-desktop"
description: "PySide6/PyQt 기반 Qt GUI, Widgets/QML, signal-slot, QThread, 백그라운드 작업, UI 멈춤, 취소와 종료 문제에 사용한다. 기존 바인딩을 유지하고 GUI 스레드와 작업 수명주기를 검증한다. 일반 웹 UI에는 사용하지 않는다."
---

# Qt 데스크톱

1. Qt/Python 버전, PySide/PyQt, Widgets/QML, UI 생성 방식과 앱 진입점을 확인한다. 바인딩을 임의로 교체하거나 혼합하지 않는다.
2. 사용자 동작, GUI 스레드, 작업 스레드/프로세스, 모델·파일 I/O 사이의 흐름을 추적한다.
3. 위젯 변경은 GUI 스레드에서 수행한다. 긴 연산을 GUI 콜백에서 직접 실행하지 않는다. worker의 결과·진행·오류를 signal로 전달하고 GUI 객체를 worker에 넘기지 않는다.
4. 지속적인 queued slot 처리가 필요하면 QObject worker + moveToThread 방식을 우선한다. QThread 서브클래스 자체가 금지된 것은 아니다. 선택한 방식의 affinity와 event loop를 설명한다.
5. 시작·중복 실행·오류·취소·창 닫기·작업 종료를 함께 설계한다. 작업 객체 참조를 유지하고 finished/deleteLater 연결을 확인한다.
6. block된 worker slot에는 queued cancel slot이 제때 도착하지 않을 수 있다. 협력적 interruption 검사 또는 thread-safe 취소 신호를 작업 구간에서 확인한다. quit()만으로 실행 중 연산이 중단된다고 가정하지 않는다.
7. 기존 Qt 테스트 도구로 결과와 오류 signal, 연속 실행, 취소와 종료를 확인한다. offscreen 테스트는 실제 화면 렌더링과 플랫폼 통합을 대체하지 않는다.

수명주기 검증은 [스레드와 종료](references/lifecycle.md)를 따른다.

## 결과

GUI 응답성, 스레드 소유권, 취소·종료 처리, 실행한 검증과 플랫폼 한계를 보고한다.
