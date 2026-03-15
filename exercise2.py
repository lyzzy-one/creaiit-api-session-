"""
CRAI+IT API 세션 - 실습 2: LLM -> UI 연결
목표: Structured Output을 받아서 HTML UI로 표시하기

흐름:
User input -> LLM API 호출 -> JSON 응답 -> 코드에서 파싱 -> HTML UI 출력
"""

# ============================================
# Step 1: 필요한 라이브러리 불러오기
# ============================================
from openai import OpenAI
import json
import os
import sys
import webbrowser
from dotenv import load_dotenv

# Windows 콘솔 UTF-8 출력 설정
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

# ============================================
# Step 2: 환경변수에서 API 키 로드
# ============================================
load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("[ERROR] OPENROUTER_API_KEY가 설정되지 않았습니다.")
    print("        .env 파일을 확인해주세요.")
    exit(1)

print(f"[OK] API 키 로드 완료: {api_key[:15]}...")

# ============================================
# Step 3: OpenRouter 클라이언트 생성
# ============================================
client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# ============================================
# Step 4: 사용자 입력 받기
# ============================================
print()
print("=" * 50)
print("문장을 입력하면 정보를 추출해서 카드 UI로 보여드려요!")
print("=" * 50)
print()

# 사용자 입력 또는 기본값
user_input = input("[INPUT] 문장 입력 (Enter = 기본값 사용): ").strip()

if not user_input:
    user_input = "Tom is 23 years old and works as a software engineer at Google."
    print(f"        -> 기본값 사용: {user_input}")

print()
print("[...] LLM에게 요청 중...")

# ============================================
# Step 5: Structured Output API 호출 (확장된 스키마)
# ============================================
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": """Extract person information from the input sentence.
If information is not available, use appropriate default values:
- name: extract the name
- age: extract the age (number)
- job: extract the job/occupation (if not mentioned, use "Not specified")
- company: extract the company name (if not mentioned, use "Not specified")"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person_profile",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "number"},
                    "job": {"type": "string"},
                    "company": {"type": "string"}
                },
                "required": ["name", "age", "job", "company"],
                "additionalProperties": False
            }
        }
    }
)

# ============================================
# Step 6: JSON 응답 파싱
# ============================================
content = response.choices[0].message.content
data = json.loads(content)

print()
print("[OUTPUT] LLM 응답 (JSON):")
print(json.dumps(data, indent=2, ensure_ascii=False))

# ============================================
# Step 7: HTML UI 생성
# ============================================
html_content = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRAI+IT - Person Profile Card</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .header {{
            color: white;
            text-align: center;
            margin-bottom: 30px;
        }}

        .header h1 {{
            font-size: 2rem;
            margin-bottom: 10px;
        }}

        .header p {{
            opacity: 0.9;
            font-size: 1rem;
        }}

        .card {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 400px;
            width: 100%;
            text-align: center;
        }}

        .avatar {{
            width: 100px;
            height: 100px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            margin: 0 auto 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 2.5rem;
            color: white;
        }}

        .name {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }}

        .age {{
            font-size: 1rem;
            color: #888;
            margin-bottom: 20px;
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-top: 20px;
        }}

        .info-item {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
        }}

        .info-label {{
            font-size: 0.75rem;
            color: #888;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 5px;
        }}

        .info-value {{
            font-size: 1rem;
            color: #333;
            font-weight: 600;
        }}

        .footer {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #eee;
        }}

        .badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85rem;
        }}

        .source {{
            margin-top: 30px;
            color: white;
            opacity: 0.8;
            font-size: 0.9rem;
        }}

        .json-box {{
            background: #1e1e1e;
            color: #9cdcfe;
            padding: 15px;
            border-radius: 10px;
            text-align: left;
            font-family: 'Consolas', monospace;
            font-size: 0.85rem;
            margin-top: 20px;
            max-width: 400px;
            width: 100%;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>CRAI+IT API Session</h1>
        <p>LLM Structured Output -> UI Demo</p>
    </div>

    <div class="card">
        <div class="avatar">
            {data['name'][0].upper()}
        </div>

        <div class="name">{data['name']}</div>
        <div class="age">{data['age']} years old</div>

        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Job</div>
                <div class="info-value">{data['job']}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Company</div>
                <div class="info-value">{data['company']}</div>
            </div>
        </div>

        <div class="footer">
            <span class="badge">Generated by AI</span>
        </div>
    </div>

    <div class="json-box">
        <strong style="color: #ce9178;">// LLM JSON Response</strong><br>
        {json.dumps(data, indent=2, ensure_ascii=False).replace(chr(10), '<br>').replace(' ', '&nbsp;')}
    </div>

    <div class="source">
        Input: "{user_input}"
    </div>
</body>
</html>
"""

# ============================================
# Step 8: HTML 파일 저장 및 브라우저에서 열기
# ============================================
output_file = "profile_card.html"

with open(output_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print()
print("=" * 50)
print(f"[OK] HTML 파일 생성 완료: {output_file}")
print("=" * 50)

# 브라우저에서 열기
print()
print("[...] 브라우저에서 결과를 여는 중...")
webbrowser.open(f"file://{os.path.abspath(output_file)}")

print()
print("[DONE] 실습 2 완료!")
print()
print("[TIP] 이것이 바로 AI -> API -> JSON -> UI 흐름입니다!")
print("      실제 서비스에서는 이 JSON 데이터를 React, Vue 등으로 렌더링합니다.")
