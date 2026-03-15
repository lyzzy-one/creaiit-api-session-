"""
CRAI+IT API 세션 - 실습 1: Structured Output
목표: LLM 응답을 JSON 구조로 받아서 코드에서 바로 사용하기
"""

# ============================================
# Step 1: 필요한 라이브러리 불러오기
# ============================================
from openai import OpenAI
import json
import os
from dotenv import load_dotenv

# ============================================
# Step 2: 환경변수에서 API 키 로드
# ============================================
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("=" * 50)
    print("❌ 오류: OPENROUTER_API_KEY가 설정되지 않았습니다.")
    print()
    print("📝 해결 방법:")
    print("   1. .env.example 파일을 .env로 복사하세요")
    print("   2. .env 파일을 열어 실제 API 키를 입력하세요")
    print("   3. 이 코드를 다시 실행하세요")
    print("=" * 50)
    exit(1)

print(f"✅ API 키 로드 완료: {api_key[:15]}...")

# ============================================
# Step 3: OpenRouter 클라이언트 생성
# ============================================
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

print("✅ OpenRouter 클라이언트 준비 완료")

# ============================================
# Step 4: 입력 문장 정의
# ============================================
# 이 문장에서 이름과 나이를 추출할 거예요!
sentence = "Tom is 23 years old."

print()
print("=" * 50)
print("📝 입력 문장:", sentence)
print("=" * 50)

# ============================================
# Step 5: Structured Output으로 API 호출
# ============================================
print()
print("🤖 LLM에게 요청 중...")
print("   → 이름과 나이를 JSON 형식으로 추출해줘!")
print()

response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # 사용할 모델
    messages=[
        {
            "role": "system",
            "content": "Extract the person's name and age from the input sentence."
        },
        {
            "role": "user",
            "content": sentence
        }
    ],
    # ⭐ 여기가 핵심! Structured Output 설정
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_info",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"}
                },
                "required": ["name", "age"],
                "additionalProperties": False
            }
        }
    }
)

# ============================================
# Step 6: 응답 파싱 및 출력
# ============================================
# LLM 응답에서 content 추출
content = response.choices[0].message.content

# JSON 문자열을 Python 딕셔너리로 변환
data = json.loads(content)

print("=" * 50)
print("📤 LLM 응답 (JSON)")
print("=" * 50)
print(json.dumps(data, indent=2, ensure_ascii=False))
print("=" * 50)

# ============================================
# Step 7: 추출된 데이터 활용
# ============================================
print()
print("🎯 추출된 정보:")
print(f"   이름: {data['name']}")
print(f"   나이: {data['age']}")
print()

# 이제 코드에서 자유롭게 사용 가능!
if data["age"] >= 20:
    print(f"   → {data['name']}님은 성인입니다.")
else:
    print(f"   → {data['name']}님은 미성년자입니다.")

print()
print("✨ 실습 1 완료!")
print()
print("💡 미션: sentence 변수를 바꿔서 다시 실행해보세요!")
print('   예: "Alice is 27 years old and works at a startup."')
