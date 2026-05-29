import os
import logging
import requests
import google.generativeai as genai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

# 디버그 로깅 활성화: 슬랙에서 이벤트가 들어오는지 터미널에 출력합니다.
logging.basicConfig(level=logging.INFO)

# 1. 환경 변수 로드
load_dotenv()

# 2. Gemini 설정 (무료 할당량이 넉넉한 2.5 Flash 모델로 우회 적용)
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.5-flash')

# 3. Slack App 초기화
app = App(token=os.environ["SLACK_BOT_TOKEN"])

def fetch_loki_logs():
    """K8s 내부의 Loki API를 찔러 dummy-app의 최근 에러 로그를 가져옵니다."""
    try:
        # 로컬 Mac에서 K8s 내부 Loki(3100)로 접속하기 위한 URL
        loki_url = "http://localhost:3100/loki/api/v1/query"
        query = '{app="dummy-app"}'
        response = requests.get(loki_url, params={'query': query, 'limit': 10})
        data = response.json()
        
        logs = []
        if 'data' in data and 'result' in data['data']:
            for result in data['data']['result']:
                for value in result['values']:
                    logs.append(value[1]) # value[0]은 타임스탬프, value[1]이 실제 로그
        return "\n".join(logs)
    except Exception as e:
        return f"Loki 로그 수집 실패: {e}"

# 4. 슬랙에서 봇이 멘션(@) 되었을 때 동작하는 이벤트 핸들러
@app.event("app_mention")
def handle_mentions(body, say):
    event = body["event"]
    # 스레드에 답변을 달기 위해 ts(timestamp) 추출
    thread_ts = event.get("thread_ts", event["ts"])
    
    say(text="🔍 K8s 에러 로그를 수집하고 분석 중입니다. 잠시만 기다려주세요...", thread_ts=thread_ts)
    
    # 1) 로그 수집
    logs = fetch_loki_logs()
    if not logs or "실패" in logs:
        say(text=f"⚠️ 로그를 가져오지 못했습니다. Loki 포트포워딩 상태를 확인해주세요.\n```{logs}```", thread_ts=thread_ts)
        return

    # 2) AI 프롬프트 구성 (목표 달성을 위한 엔지니어링)
    prompt = f"""
    당신은 숙련된 Kubernetes 인프라/DevOps 엔지니어입니다.
    현재 로컬 클러스터의 'dummy-app' 파드에서 다음과 같은 에러 로그가 반복해서 발생하고 있습니다.
    
    [에러 로그]
    {logs}
    
    위 로그를 분석하여 
    1. 장애의 원인을 간략히 요약하고,
    2. 개발자가 즉시 복사해서 실행할 수 있는 `kubectl` 조치 명령어를 **마크다운 코드 블록**으로 제시해주세요.
    (예시: OOM의 경우 `kubectl set resources deployment dummy-app --limits=memory=256Mi` 같은 방식)
    """
    
    # 3) Gemini API 호출 및 결과 전송
    try:
        response = model.generate_content(prompt)
        say(text=response.text, thread_ts=thread_ts)
    except Exception as e:
        say(text=f"⚠️ AI 분석 중 오류가 발생했습니다: {e}", thread_ts=thread_ts)

if __name__ == "__main__":
    print("⚡️ DevOps AI Bot이 시작되었습니다! (Socket Mode)")
    # SocketModeHandler가 Slack 서버와 웹소켓으로 통신을 유지합니다.
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
