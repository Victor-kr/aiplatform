Phase 0 작업 일지: 기반 환경 셋업 완료

작업일자: 2026-05-28
목표: 최소 리소스로 GitLab Omnibus와 로컬 K8s 연동 환경 구축

1. 수행 완료 작업

컨테이너 런타임 및 K8s 도구 설치: Mac(Apple Silicon) 환경에 맞춰 OrbStack 설치 및 Rosetta 호환성 세팅 완료. kind, kubectl, helm 설치 완료.

로컬 Kubernetes 구성: kind를 사용하여 ai-platform 클러스터 생성. 호스트 브라우저에서 K8s 내부 웹 UI에 접근 가능하도록 80번 포트 매핑(kind-config.yaml).

GitLab 로컬 구동 (RAM 최적화): docker-compose.yml을 통해 GitLab Omnibus 컨테이너 실행.

Puma worker 축소, Sidekiq 동시성 제한 등 메모리를 3~4GB 수준으로 억제.

K8s 모니터링 스택 (Loki/Promtail/Grafana/Prometheus) 설치: Helm을 이용하여 monitoring 네임스페이스에 loki-stack 설치 완료.

2. 주요 트레이드오프 및 아키텍처 결정 사항 (G 생각)

K8s 내부 설치 vs Docker Compose 분리

무거운 GitLab을 K8s 내부에 Helm으로 설치하면 수십 개의 Pod가 생성되어 로컬 RAM(24GB)에 심각한 오버헤드를 유발함.

이를 방지하기 위해 GitLab은 Docker Compose(단일 컨테이너)로 분리하고, K8s(kind)는 순수하게 애플리케이션 운영 및 장애 테스트용 타겟으로만 역할을 분리함.

GitLab 내장 Grafana 연동 포기 및 K8s 내부 Grafana 활성화 (Surgical Changes)

초기에는 메모리 절약을 위해 GitLab의 내장 Grafana를 사용하려 했으나, Docker 네트워크와 kind K8s 네트워크를 브릿지 시키는 작업의 복잡도가 매우 높음.

우리의 핵심 목표는 'AI의 데이터 조회'이므로, 네트워크 설정에 시간을 낭비하지 않고 loki-values.yaml에서 grafana: enabled: true로 단 한 줄만 수정하여 K8s 내부에 경량 모니터링 UI를 띄우는 것으로 단순하게 문제를 해결함.

GitLab 최신 버전(19.0+) 이슈 대응

gitlab.rb 설정 중 mattermost['enable'] = false 옵션으로 인해 reconfigure 에러가 발생함. (해당 기능이 패키지에서 완전히 제거됨)

에러 로그 분석 후 해당 라인만 삭제(최소한의 코드 수정)하여 정상 기동 확인.

3. 최종 상태 (성공 기준 달성)

http://localhost:8929 (GitLab) 정상 접속 및 로그인 확인.

kubectl port-forward를 통해 http://localhost:3000 (Grafana) 정상 접속 확인 및 K8s 파드(loki, promtail 등) Running 상태 확인.