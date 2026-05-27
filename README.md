AI-Driven Internal DevOps Platform 🚀

1. Project Overview

단순한 텍스트 챗봇이 아닌, 실제 운영 시스템(Kubernetes, CI/CD, 모니터링)과 직접 연동되어 장애 원인을 분석하고 조치 명령어(Actionable Command)까지 제시하는 AI 기반 DevOps 플랫폼 구축 프로젝트입니다.

개발자는 Slack Bot 또는 Web UI를 통해 자연어로 인프라 상태를 묻고, AI는 사내 운영 매뉴얼(Runbook)과 실시간 메트릭(Prometheus/Loki)을 스스로 조회하여 가장 적합한 트러블슈팅 가이드를 제공합니다.

2. Architecture & Tech Stack (Spec)

본 프로젝트는 비용 및 리소스 효율성을 위해 로컬 개발 환경(MacBook)과 프로덕션 환경(AWS)을 분리하는 투트랙(Two-track) 전략을 사용합니다.

2-1. Local Development Environment (MacBook Air 24GB RAM)

Container Runtime: OrbStack (Docker Desktop 대비 경량/고속)

Kubernetes: kind (Kubernetes IN Docker)

Source Code & CI/CD: GitLab Omnibus (로컬 Docker 구동)

RAM 최적화: 불필요한 데몬(Registry, Pages 등) 비활성화 및 Worker 최소화로 3~4GB 내 통제

Observability (모니터링/로그):

Metric: GitLab 내장 Prometheus + Grafana

Log: Promtail + Loki (K8s 내부 설치)

AI Backend:

Python (FastAPI): LangChain 등 프레임워크를 배제하고 OpenAI API Native Tool Calling을 직접 구현하여 완벽한 통제권 확보.

Interface: Slack Bot (Bolt API 기반 ChatOps)

Local LLM: Ollama (Llama3 8B)

2-2. Production / Portfolio Environment (AWS)

Infrastructure as Code (IaC): Terraform

Compute: AWS EKS, EC2 (일반 CPU 인스턴스 사용)

AI Inference: AWS 환경에서는 GPU 인스턴스 비용/제약을 피하기 위해 OpenAI API (gpt-4o-mini 등)로 환경변수 스위칭 적용.

Interface: Streamlit Web UI

3. Goal-Driven Roadmap & Success Criteria

본 프로젝트는 각 단계별로 명확한 '성공 기준'을 정의하고, 이를 통과할 때까지 구조를 단순화하며 반복 검증(Goal-driven execution)합니다.

Phase 0: 기반 환경 셋업

목표: 최소 리소스로 GitLab Omnibus와 로컬 K8s 연동 환경 구축.

성공 기준: GitLab 로컬 웹 접속 성공 및 내장 Grafana에서 kind K8s Node/Pod 기본 지표(CPU/Memory) 조회 성공.

Phase 1: K8s 로그 AI 분석기 & Slack Bot 연동

목표: 에러 로그를 Slack Bot을 통해 분석받고, 해결용 CLI 명령어를 추천받는다. (Read-Only + Command Print)

성공 기준: SpringBoot Pod 고의 장애(OOM 등) 발생 후 Slack에 원인 문의 시, 원인 설명과 함께 실행 가능한 명령어(예: kubectl set resources...)가 마크다운 코드 블록으로 출력됨.

Phase 2: Agent 기반 메트릭 조회 및 Mini-RAG 도입

목표: AI가 지표를 스스로 조회하고, 사내 런북(Runbook) 규칙을 참고해 복합적인 답변을 생성한다.

성공 기준: "결제 API가 느리다"고 질문 시, AI가 Tool Calling으로 Prometheus와 Loki를 조회하고, runbook.md를 참조하여 서킷 브레이커 발동 명령어를 추천함.

Phase 3: Web UI 통합 및 AWS 포팅

목표: 포트폴리오 시각화용 Web UI 완성 및 클라우드 환경 배포.

성공 기준: Terraform 코드로 AWS 인프라(일반 CPU 인스턴스)를 생성하고, Streamlit Web UI를 통해 K8s 상태 조회 및 AI 조치 가이드 정상 동작 확인.

4. Runbook & Knowledge Base (Mini-RAG)

프로젝트 내에 runbook.md (예: 트래픽 폭증 대응 가이드, CDN 캐시 무효화 규칙 등)를 구성하여, AI가 장애 판단 시 해당 문서의 '대응 규칙'과 '조치 명령어'를 최우선으로 참고하도록 System Context로 주입합니다.