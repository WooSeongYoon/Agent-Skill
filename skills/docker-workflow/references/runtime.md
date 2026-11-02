# 실행 조건

- `docker compose config --quiet`로 구성을 검사할 수 있다. 환경 치환이 포함된 전체 config 출력을 공유하면 비밀 값이 노출될 수 있다.
- 빌드 성공은 서비스 기동 성공이 아니다. 명시적인 임시 이름과 로컬 포트로 실행하고 정상 응답·종료를 확인한다.
- 네트워크와 GPU를 사용할 권한이 없는 환경에서는 문법 검토 결과와 실제 실행 결과를 구분한다.
- CUDA 이미지 버전은 호스트 드라이버와 ML 프레임워크의 공식 호환 표를 확인해 선택한다. 태그를 추측하지 않는다.
- Qt GUI의 OS 배포, headless 테스트, 컨테이너 안의 실제 디스플레이 연결은 서로 다른 목표다.
- 호스트 Docker socket을 무조건 마운트하지 않는다. 필요한 접근만 프로젝트 조건에 따라 구성한다.
- `docker compose down -v`처럼 영구 데이터를 지우는 명령을 테스트 정리의 기본값으로 쓰지 않는다.

[빌드 권장 사항](https://docs.docker.com/build/building/best-practices/), [빌드 시크릿](https://docs.docker.com/build/building/secrets/)
