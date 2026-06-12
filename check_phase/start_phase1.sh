#!/bin/bash

# 스크립트가 위치한 디렉토리의 상위 폴더(프로젝트 루트)로 강제 이동
cd "$(dirname "$0")/.."

echo "🔍 Phase 1 테스트 환경 점검을 시작합니다..."

# 1. Docker/OrbStack 실행 여부 확인
if ! docker info > /dev/null 2>&1; then
  echo "❌ Docker(OrbStack)가 실행되어 있지 않습니다. OrbStack 앱을 먼저 켜주세요."
  exit 1
fi
echo "✅ Docker 동작 확인 완료"

# 2. Loki 포트포워딩 상태 확인 및 자동 실행
# nc(netcat) 명령어로 3100 포트가 열려있는지 확인합니다.
if ! nc -z localhost 3100; then
  echo "⏳ Loki 포트포워딩(3100)이 꺼져있습니다. 백그라운드에서 연결을 시도합니다..."
  kubectl port-forward -n monitoring svc/loki 3100:3100 > /dev/null 2>&1 &
  sleep 3 # 포트가 열릴 때까지 잠시 대기
else
  echo "✅ Loki 포트포워딩(3100) 동작 확인 완료"
fi

# 3. 가상환경 존재 여부 확인 (루트로 이동했으므로 정상적으로 venv를 찾음)
if [ ! -d "venv" ]; then
  echo "❌ venv 가상환경 폴더를 찾을 수 없습니다. 프로젝트 루트에서 실행했는지 확인해주세요."
  exit 1
fi

echo "================================================="
echo "🎉 모든 준비가 완료되었습니다!"
echo "👉 슬랙 채널로 이동하여 봇에게 대화를 걸어보세요."
echo "예시: @aiplatform-app 지금 시스템 상태 어때?"
echo "================================================="

# 4. 가상환경 활성화 및 봇 실행
source venv/bin/activate
python src/bot/bot.py
