Phase 1 작업 일지: K8s 로그 AI 분석기 & Slack Bot 연동 완료

작업일자: 2026-05-29 ~ 2026-06-12
목표: 에러 로그를 Slack Bot을 통해 분석받고, 해결용 CLI 명령어를 추천받는다. (로컬 테스트 자동화 포함)

1. 수행 완료 작업

고의 장애 파드 배포: 리소스 낭비를 막기 위해 무거운 SpringBoot 이미지 대신 busybox를 사용하여 10초마다 가짜 OOM(OutOfMemory) 에러 로그를 뿜어내는 dummy-app K8s 파드 배포.

Slack App 연동: Slack API에서 'DevOps AI Bot' 앱 생성 및 권한(Scopes) 설정. 로컬 환경 테스트를 위해 ngrok 대신 Socket Mode를 활성화하여 앱 토큰(xapp-)과 봇 토큰(xoxb-) 발급.

Python 백엔드 구축: 무거운 LangChain 프레임워크를 배제하고, 순수 Python 기반으로 slack_bolt와 google-generativeai 패키지만을 사용하여 최소한의 코드로 봇 서버 구현 (src/bot/bot.py).

Loki 로그 수집 연동: 파이썬 코드 내에서 requests 라이브러리를 통해 로컬에 포트포워딩된 K8s Loki API(localhost:3100)를 찔러 dummy-app의 에러 로그를 텍스트로 추출.

[NEW] 테스트 자동화 스크립트 도입: 매번 로컬 테스트 시 인프라(Docker) 점검, 포트포워딩, 봇 실행을 수동으로 하는 번거로움을 없애기 위해 check_phase/start_phase1.sh 쉘 스크립트 작성.

2. 주요 트레이드오프 및 트러블슈팅 (G 생각)

진짜 앱 빌드 vs Dummy 스크립트 (RAM 최적화)

실제 Java 앱을 빌드하고 레지스트리에 푸시하는 것은 'AI 로그 분석'이라는 핵심 목표 달성에 불필요한 시간과 로컬 RAM을 소모함.

busybox 이미지에 쉘 스크립트를 주입하여 가짜 에러 로그를 남기는 방식으로 최소한의 변경(Surgical change)을 통해 장애 환경을 시뮬레이션함.

API 404 및 429 Quota 에러에 따른 모델 스위칭 (Goal-driven)

초기에는 gemini-1.5-pro 등을 명시했으나 구형 모델 지원 중단(404) 및 무료 티어(Free Tier)의 Pro 모델 할당량 한도(429 Quota Exceeded) 에러 발생.

의사 결정: 추가 결제 없이 파이프라인 검증이라는 목표를 달성하기 위해, 무료 할당량이 넉넉한 gemini-2.5-flash 모델로 즉시 우회(Fallback) 적용.

[NEW] GitHub Secret Scanning 보안 차단 및 .env 분리

.env 파일에 슬랙/Gemini API 토큰을 넣은 상태로 git push를 시도했으나, GitHub의 Secret Scanning이 이를 감지하여 푸시를 강제 차단함.

git reset으로 커밋을 되돌리고 .gitignore에 .env를 추가하여 보안 사고(토큰 유출)를 선제적으로 방지함. 환경변수(.env)와 가상환경(venv)의 역할을 명확히 분리하여 관리.

[NEW] 자동화 스크립트 경로 유연성 확보 (Surgical Change)

쉘 스크립트를 check_phase/ 하위 폴더로 이동시키면서 발생한 venv 및 파이썬 소스코드 경로 인식 문제 발생.

스크립트 내 모든 경로를 수정하는 대신, 스크립트 최상단에 cd "$(dirname "$0")/.." 한 줄을 추가하여 실행 위치와 무관하게 항상 프로젝트 루트를 기준으로 작동하도록 견고하게 개선.

[NEW] 로컬 호스트에서의 kubectl 제어 원리 이해

컨테이너 내부에 접속(docker exec -it)하지 않고도 로컬에서 kubectl이 동작하는 이유 파악. kind가 클러스터 생성 시 로컬 ~/.kube/config에 K8s API 서버(컨테이너 내부)로 통신할 수 있는 통로와 인증서를 자동 구성해 준 덕분임을 확인함.

3. 최종 상태 (성공 기준 달성)

Slack에서 봇을 멘션(@aiplatform-app)하여 질문 시, K8s 내부 Loki에서 에러 로그를 성공적으로 수집.

AI가 로그를 분석하여 장애 원인(메모리 부족)을 정확히 요약함.

개발자가 즉시 복사해서 실행할 수 있는 조치 명령어(kubectl set resources...)를 마크다운 코드 블록으로 정상 응답함.

./check_phase/start_phase1.sh 명령어 하나로 전체 인프라 점검 및 봇 실행 준비가 완료됨.
