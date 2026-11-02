---
name: "docker-workflow"
description: "Dockerfile, Compose, 컨테이너 빌드·실행 오류, 이미지 크기, Python/웹/ML 실행 환경을 다룰 때 사용한다. 빌드와 런타임 검증을 분리한다. Kubernetes나 외부 서비스 배포를 요청 없이 추가하지 않는다."
---

# Docker 작업

1. 기존 Dockerfile, Compose, CI, 잠금 파일, 진입점과 필요한 포트·볼륨·장치를 확인한다.
2. 개발/운영 이미지, CPU/GPU, 호스트 플랫폼, Qt 디스플레이 의존성을 구분한다. GUI 앱을 서버 컨테이너처럼 실행 가능하다고 가정하지 않는다.
3. 작은 신뢰 가능한 베이스와 필요한 패키지만 사용한다. 프로젝트 정책에 맞게 버전이나 digest를 고정하고 갱신 방법을 남긴다.
4. .dockerignore와 COPY 범위를 줄인다. 빌드 의존성이 런타임에 필요 없을 때 multi-stage를 사용한다. 캐시를 위해 잠금 파일과 의존성 설치를 소스보다 먼저 배치한다.
5. 런타임은 가능한 경우 비루트 사용자로 실행한다. 시크릿은 ARG/ENV/COPY로 이미지에 넣지 않고 BuildKit secret 또는 런타임 주입을 사용한다.
6. Compose 설정 검사 → 이미지 빌드 → 격리된 smoke test 순서로 검증한다. health check는 실제 준비 상태를 확인한다. SIGTERM 종료와 파일 권한도 확인한다.
7. 임시 컨테이너를 정리한다. 사용자 볼륨이나 데이터는 삭제하지 않는다. 실행하지 못한 단계는 미검증으로 표시한다.

[실행 조건](references/runtime.md)을 해당 환경에 맞게 확인한다.
