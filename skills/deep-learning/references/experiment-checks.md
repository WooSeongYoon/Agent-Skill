# 실험과 추론 점검

- 분류/회귀/시계열/검출 등 문제에 맞게 지표를 선택한다. 클래스 불균형에서는 accuracy 하나로 성능을 결론 내리지 않는다.
- PyTorch의 eval()은 dropout/batchnorm 등의 동작을 바꾸며 gradient 기록을 끄지 않는다. inference_mode()/no_grad()는 eval()을 대신하지 않는다.
- CPU smoke test 통과는 CUDA, AMP, 분산 학습 성공을 의미하지 않는다. 장치별 미검증 범위를 남긴다.
- GPU 지연 시간을 측정할 때 warmup과 동기화, 배치 크기를 기록한다. peak memory 측정 범위를 명시한다.
- DataLoader worker의 난수 상태와 shuffle generator를 확인한다. 결정적 연산 선택은 성능 저하나 미지원 연산 오류를 동반할 수 있다.
- 학습 재개에는 모델뿐 아니라 optimizer, scheduler, scaler, step과 필요한 난수 상태도 검토한다. 단순 추론 checkpoint와 재개 checkpoint를 구분한다.
- 신뢰하지 않는 pickle 기반 모델 파일을 실행하지 않는다. 프로젝트 프레임워크의 안전한 로딩 경로와 출처를 확인한다.
- 모델·대용량 원본 데이터·비공개 샘플은 일반 Git 커밋에서 제외하고 참조와 메타데이터를 남긴다.

[PyTorch 재현성](https://docs.pytorch.org/docs/stable/notes/randomness.html), [추론 모드](https://docs.pytorch.org/docs/stable/generated/torch.autograd.grad_mode.inference_mode.html)
