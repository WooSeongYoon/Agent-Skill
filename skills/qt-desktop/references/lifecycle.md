# 스레드와 종료

- QThread 객체는 생성한 스레드에 속한다. run()이 실행되는 스레드와 다르다. queued slot을 QThread 서브클래스에 추가하면 기대한 worker 스레드에서 실행되지 않을 수 있다.
- parent가 있는 QObject는 moveToThread가 실패할 수 있다. worker 생성·이동·연결 순서를 확인한다.
- 작업 실패에서도 정리 경로가 실행되게 한다. UI에 사용자용 오류를 보내고 로그에 진단 정보를 남기되 비밀 값은 제외한다.
- 작업 중 창을 닫으면 종료 요청 → 작업의 협력적 중단 → finished → 정리 완료 순서를 확인한다. GUI에서 무기한 wait()로 응답을 막지 않는다.
- terminate()는 정상 취소 수단으로 쓰지 않는다. requestInterruption()도 worker가 확인해야 효과가 있다.
- Python CPU 작업의 병렬 속도 향상이 필요하면 프로세스 경계를 검토한다. QThread 도입만으로 GIL 제약이 사라지지 않는다.
- pytest-qt가 설정된 프로젝트에서는 waitSignal/waitUntil로 상태를 기다린다. 고정 sleep으로 타이밍 오류를 숨기지 않는다.
- 합성 데이터의 짧은 작업으로 UI 테스트를 실행한다. GPU 학습은 GUI 수명주기 테스트에 포함하지 않는다.

[Qt QThread 공식 문서](https://doc.qt.io/qtforpython-6/PySide6/QtCore/QThread.html)
