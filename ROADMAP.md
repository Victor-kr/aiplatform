# 🚀 AI-Driven Internal DevOps Platform 전체 로드맵

본 문서는 AI 기반 DevOps 플랫폼 구축을 위한 12주(3개월) 과정의 상세 진행 계획입니다.
각 단계(Phase)는 명확한 성공 기준(Goal)을 통과할 때까지 구조를 단순화하며 반복 검증하는 **Goal-driven execution** 원칙을 따릅니다.

## Phase 0: 기반 환경 셋업 (1주 차)

* **핵심 작업**: MacBook(24GB RAM) 환경에 최소 리소스로 인프라 뼈대 구축

* **구현 요소**:

  * RAM 3~4GB로 통제된 `GitLab Omnibus` (로컬 Docker 컨테이너)

  * 로컬 Kubernetes 클러스터 (`kind` + `OrbStack`)

  * K8s 모니터링 스택 (`Loki`, `Promtail`) 및 GitLab 내장 `Prometheus` 연동

* **🎯 성공 기준**: K8s 클러스터 구동 및 GitLab 로컬 웹에 접속하여, 내장 Grafana에서 K8s 노드와 Pod의 기본 메트릭(CPU/Memory)이 정상 조회되어야 함.

## Phase 1: K8s 에러 로그 AI 분석 & Slack Bot 연동 (2~4주 차)

* **핵심 작업**: 에러 발생 시 AI가 로그를 분석하고 조치 가이드를 Slack으로 제공

* **구현 요소**:

  * 고의 장애 유발용 SpringBoot Pod 구성 (예: OOMKilled, CrashLoopBackOff)

  * Slack Bot 백엔드 (`Python FastAPI` + `Slack Bolt API`)

  * Multi-LLM 연동 (`Ollama` 로컬 모델 / `Gemini Pro` 클라우드 모델)

* **🎯 성공 기준**: Pod를 강제로 종료하거나 장애를 발생시켰을 때, Slack에서 봇에게 질문하면 AI가 로그를 기반으로 원인을 요약하고, 즉시 실행 가능한 `kubectl` 조치 명령어를 복사하기 쉬운 마크다운 코드 블록 형태로 출력해야 함.

## Phase 2: AI Agent (Native Tool Calling) 및 Mini-RAG 도입 (5~8주 차)

* **핵심 작업**: AI가 수동적 로그 요약을 넘어, 스스로 시스템 지표를 조회하고 사내 규칙을 참고하도록 고도화

* **구현 요소**:

  * OpenAI / Gemini Native Tool Calling 적용 (무거운 LangChain 프레임워크 배제, 순수 Python 기반 제어)

  * 연동 도구(Tools) 개발: `query_prometheus()`, `query_loki()`, `search_runbook()`

  * 사내 운영 매뉴얼(`runbook.md`) 작성 및 컨텍스트 주입 (Mini-RAG)

* **🎯 성공 기준**: "최근 1시간 결제 API 상태 어때?"와 같은 자연어 질문 시, AI가 스스로 Prometheus/Loki API를 찔러 메트릭을 확인하고, 런북 규칙을 적용하여 복합적인 장애 대응 가이드(예: 서킷 브레이커 발동)를 답변해야 함.

## Phase 3: Web UI 통합 및 AWS 포팅 (9~12주 차)

* **핵심 작업**: 포트폴리오 시연을 위한 시각화 및 프로덕션 환경(클라우드) 배포

* **구현 요소**:

  * Slack Bot API 백엔드를 재활용한 `Streamlit` Web UI 구축

  * AWS 인프라 프로비저닝용 `Terraform` 코드 작성 (일반 CPU 인스턴스 사용)

  * AWS 배포 시 GPU 제약 회피 및 성능 최적화를 위한 `Gemini Pro` API 완벽 스위칭

* **🎯 성공 기준**: AWS 인프라를 Terraform으로 띄우고, 클라우드 환경에서도 Streamlit Web UI를 통해 전체 AI 분석 및 가이드 기능이 로컬 환경과 동일하게 작동하는 것을 성공적으로 시연(녹화)해야 함.
