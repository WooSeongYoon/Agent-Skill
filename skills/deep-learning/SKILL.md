---
name: "deep-learning"
description: "딥러닝 모델, 학습·평가·추론 파이프라인, 데이터 분할, PyTorch/TensorFlow, CUDA 메모리, 재현성 문제에 사용한다. 기존 프레임워크를 먼저 확인한다. 일반 LLM 프롬프트 작성이나 단순 API 호출만 있는 작업에는 사용하지 않는다."
---

# 딥러닝 작업

1. 프레임워크/버전, 장치, 정밀도, 모델 입출력, 데이터 스키마, 지표와 baseline을 확인한다. PyTorch를 기존 TensorFlow 프로젝트에 임의로 도입하지 않는다.
2. 데이터 분할을 먼저 검토한다. 동일 사람/장비/원본의 파생 샘플과 미래 정보가 분할을 넘지 않게 한다. 전처리 통계는 훈련 데이터에만 fit한다.
3. shape, dtype, device, label 범위, loss 입력 계약을 작은 배치로 확인한다. NaN/Inf, gradient 흐름, 패딩과 mask를 점검한다.
4. 작은 합성/샘플 데이터로 forward → loss → backward → optimizer update를 확인한다. 가능하면 tiny-batch overfit로 학습 경로를 검사한다. 이를 모델 품질 검증으로 보고하지 않는다.
5. 훈련·평가 모드를 명시적으로 분리한다. PyTorch 추론은 eval()과 no_grad()/inference_mode()의 역할을 구분한다. 다른 프레임워크는 대응하는 공식 절차를 확인한다.
6. seed뿐 아니라 데이터/분할 버전, 코드 revision, 설정, 라이브러리, 장치와 지표를 기록한다. 다른 하드웨어·버전까지 완전 재현된다고 보장하지 않는다.
7. 학습 예산, 실행 시간과 GPU 사용 범위를 확인한다. 전체 학습은 요청에 포함된 범위에서만 실행한다. 먼저 CPU 또는 작은 GPU smoke test를 수행한다.
8. checkpoint 저장·복원과 추론 계약을 검증한다. 테스트 세트는 최종 평가에 사용하고 튜닝에 반복 사용하지 않는다.

[실험과 추론 점검](references/experiment-checks.md)을 필요한 항목만 적용한다.

## 결과

데이터/모델/실험 조건, 실제 실행한 단계와 지표, baseline 비교, 비용 및 재현성 한계를 보고한다.
