import os
import google.generativeai as genai
from dotenv import load_dotenv

# 1. 환경 변수 로드 (.env 파일에서 API 키 읽기)
load_dotenv()

# 2. Gemini 설정
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# 3. 사용 가능한 모델 목록 조회 및 출력
print("=== 현재 API Key로 사용 가능한 모델 목록 ===")
try:
    for m in genai.list_models():
        # 텍스트 생성(generateContent)을 지원하는 모델만 필터링해서 출력
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
except Exception as e:
    print(f"목록 조회 실패: {e}")
print("============================================")
