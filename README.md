# CREAI+IT API & Structured Output Session

> **오늘의 핵심 메시지:** "AI는 챗봇이 아니라 API로 호출되는 컴퓨팅 서비스다."

---

## 1. 세션 소개

이 세션에서는 **API**, **OpenRouter**, 그리고 **Structured Output**에 대해 배웁니다.

ChatGPT 같은 챗봇 인터페이스가 아닌, **코드로 직접 AI를 호출하는 방법**을 실습합니다.

- `exercise1.py` — 세션 중 라이브로 작성합니다
- `exercise2.py` — 세션 중 라이브로 작성합니다

---

## 2. 사전 준비

시작하기 전에 다음이 필요합니다:

| 항목 | 설명 |
|------|------|
| **VS Code 또는 Cursor** | 이미 설치되어 있다고 가정합니다 |
| **Python** | 버전 3.9 이상 권장 (아래에서 설치 방법 안내) |
| **OpenRouter API Key** | 세션 중 안내 예정 |

---

## 3. Python 설치 확인 및 설치 방법

### 3.1 Python이 설치되어 있는지 확인하기

터미널(또는 명령 프롬프트)을 열고 다음 명령어를 입력하세요:

**Windows:**
```powershell
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

결과 예시:
```
Python 3.11.5
```

버전 번호가 출력되면 Python이 설치된 것입니다. **3.9 이상**이면 괜찮습니다.

### 3.2 Python이 설치되어 있지 않은 경우

**Windows:**
1. https://www.python.org/downloads/ 에 접속
2. "Download Python 3.x.x" 버튼 클릭
3. 설치 시 **반드시 "Add Python to PATH" 체크박스를 선택**
4. 설치 완료 후 터미널을 **새로 열어서** 다시 확인

**macOS:**
1. https://www.python.org/downloads/ 에 접속
2. macOS용 설치 파일 다운로드 후 설치

또는 Homebrew 사용:
```bash
brew install python
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-venv python3-pip
```

---

## 4. GitHub에서 프로젝트 받는 방법

### 방법 A: Download ZIP (Git 없이)

1. GitHub 저장소 페이지로 이동
2. 초록색 **"Code"** 버튼 클릭
3. **"Download ZIP"** 클릭
4. 다운로드된 ZIP 파일 압축 해제
5. 압축 해제된 폴더 이름을 `creaiit-api-session`으로 변경 (폴더명에 `-main` 등이 붙어있을 수 있음)

### 방법 B: git clone (Git 설치됨)

터미널에서 원하는 위치로 이동 후:

```bash
git clone https://github.com/YOUR_USERNAME/creaiit-api-session.git
```

> `YOUR_USERNAME` 부분은 실제 저장소 주소로 바꿔주세요. 세션 중 안내됩니다.

---

## 5. 프로젝트 폴더 열기

### 5.1 터미널에서 폴더로 이동

다운로드한 폴더가 있는 위치에서:

```bash
cd creaiit-api-session
```

### 5.2 VS Code / Cursor에서 폴더 열기

**방법 1: 터미널에서 열기**
```bash
code .
```
또는 (Cursor 사용 시)
```bash
cursor .
```

**방법 2: GUI에서 열기**
1. VS Code 또는 Cursor 실행
2. `파일(File)` → `폴더 열기(Open Folder)` 클릭
3. `creaiit-api-session` 폴더 선택

---

## 6. 가상환경 생성

### 가상환경이란?

`python -m venv .venv` 명령어는 **이 프로젝트 전용 Python 환경**을 만듭니다.

쉽게 설명하면:
- 컴퓨터에 설치된 Python과 **분리된 독립 공간**을 만드는 것
- 이 프로젝트에서 설치하는 패키지가 **다른 프로젝트에 영향을 주지 않음**
- 프로젝트마다 **다른 버전의 패키지**를 사용할 수 있음

### 가상환경 생성 명령어

프로젝트 폴더 안에서 실행하세요:

**Windows:**
```powershell
python -m venv .venv
```

**macOS/Linux:**
```bash
python3 -m venv .venv
```

실행 후 `.venv` 폴더가 생성됩니다.

### 왜 `.venv/` 폴더가 GitHub에 없나요?

`.venv/` 폴더는 **용량이 크고** (수백 MB), **각 컴퓨터의 환경에 맞게 생성되어야** 합니다.

그래서:
- `.gitignore` 파일에 `.venv/`를 추가하여 **Git에 업로드되지 않도록** 설정
- 각자 자신의 컴퓨터에서 **직접 생성**해야 함

---

## 7. 가상환경 활성화

가상환경을 **활성화**해야 그 안에 패키지를 설치할 수 있습니다.

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

### Windows CMD (명령 프롬프트)

```cmd
.\.venv\Scripts\activate.bat
```

### macOS / Linux

```bash
source .venv/bin/activate
```

### 활성화 확인

활성화되면 터미널 프롬프트 앞에 `(.venv)`가 표시됩니다:

```
(.venv) C:\Users\...\creaiit-api-session>
```

또는

```
(.venv) ~/creaiit-api-session$
```

---

## 8. requirements.txt 설치

가상환경이 활성화된 상태에서:

```bash
pip install -r requirements.txt
```

이 명령어는 `requirements.txt`에 명시된 패키지들을 설치합니다:
- `openai` — OpenAI/OpenRouter API 호출용
- `python-dotenv` — `.env` 파일에서 환경변수 로드용

---

## 9. `.env.example`을 `.env`로 복사하기

### 왜 `.env` 파일이 GitHub에 없나요?

`.env` 파일에는 **API 키 같은 민감한 정보**가 들어갑니다.

이런 정보를 GitHub에 올리면:
- 누구나 볼 수 있음
- API 키가 도용될 수 있음
- **비용이 청구될 수 있음!**

그래서:
- `.env`는 `.gitignore`에 추가하여 **절대 업로드되지 않음**
- 대신 `.env.example` 파일을 제공하여 **어떤 값이 필요한지** 알려줌
- 각자 `.env.example`을 복사해서 `.env`를 만들고, **실제 키 값을 입력**

### 복사 명령어

**Windows CMD:**
```cmd
copy .env.example .env
```

**Windows PowerShell:**
```powershell
Copy-Item .env.example .env
```

**macOS / Linux:**
```bash
cp .env.example .env
```

### `.env` 파일 편집

복사 후 `.env` 파일을 열어서 실제 API 키를 입력하세요:

```
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxx
```

> API 키는 세션 중 안내됩니다.

---

## 10. exercise1.py / exercise2.py 실행 방법

가상환경이 활성화된 상태에서:

```bash
python exercise1.py
```

```bash
python exercise2.py
```

> **참고:** `exercise1.py`와 `exercise2.py`는 현재 비어있습니다. 세션 중 라이브로 코드를 작성합니다.

---

## 11. 자주 발생하는 오류와 해결법

### 오류 1: `python` 명령어를 찾을 수 없음

**증상:**
```
'python'은(는) 내부 또는 외부 명령, 실행할 수 있는 프로그램, 또는
배치 파일이 아닙니다.
```
또는
```
python: command not found
```

**해결법:**
1. Python이 설치되어 있는지 확인 (섹션 3 참고)
2. 설치 시 "Add Python to PATH" 옵션을 선택했는지 확인
3. 터미널을 **새로 열어서** 다시 시도
4. Windows에서 `py` 명령어로 시도:
   ```powershell
   py --version
   py -m venv .venv
   ```

---

### 오류 2: `python3`를 사용해야 하는 경우

**증상 (macOS/Linux):**
```
python: command not found
```

**해결법:**
macOS/Linux에서는 `python` 대신 `python3`를 사용하세요:

```bash
python3 --version
python3 -m venv .venv
python3 exercise1.py
```

---

### 오류 3: PowerShell 실행 정책 오류

**증상:**
```
.\.venv\Scripts\Activate.ps1 : 이 시스템에서 스크립트를 실행할 수 없으므로...
```

**해결법:**

**방법 A: 현재 세션에서만 허용**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
그 다음 다시 활성화:
```powershell
.\.venv\Scripts\Activate.ps1
```

**방법 B: CMD 사용**
PowerShell 대신 CMD(명령 프롬프트)를 사용:
```cmd
.\.venv\Scripts\activate.bat
```

---

### 오류 4: 가상환경 활성화를 잊은 경우

**증상:**
```
ModuleNotFoundError: No module named 'openai'
```

**원인:**
패키지를 설치했지만 **가상환경이 활성화되지 않은 상태**에서 실행

**해결법:**
1. 가상환경 활성화 (섹션 7 참고)
2. 터미널 프롬프트에 `(.venv)`가 표시되는지 확인
3. 다시 실행

---

### 오류 5: `.env` 파일이 없는 경우

**증상:**
```
OPENROUTER_API_KEY가 설정되지 않았습니다
```
또는 API 호출 시 인증 오류

**해결법:**
1. `.env.example`을 `.env`로 복사했는지 확인 (섹션 9 참고)
2. `.env` 파일 안에 실제 API 키가 입력되어 있는지 확인
3. 파일 이름이 정확히 `.env`인지 확인 (`.env.txt` 아님!)

---

## 12. 오늘의 핵심 개념 정리

### AI는 챗봇이 아니라 API로 호출되는 컴퓨팅 서비스다

| 챗봇 (ChatGPT 웹) | API (오늘 배우는 것) |
|------------------|---------------------|
| 브라우저에서 대화 | 코드로 요청 |
| 사람이 직접 사용 | 프로그램이 자동 호출 |
| 정해진 인터페이스 | 자유로운 커스터마이징 |
| 실시간 대화 전용 | 앱/서비스에 통합 가능 |

### 핵심 용어

- **API (Application Programming Interface):** 프로그램이 다른 프로그램과 소통하는 방법
- **OpenRouter:** 다양한 AI 모델을 하나의 API로 사용할 수 있게 해주는 서비스
- **Structured Output:** AI 응답을 JSON 등 정해진 형식으로 받는 것

---

## 폴더 구조

```
creaiit-api-session/
├── README.md           ← 지금 보고 있는 파일
├── requirements.txt    ← 필요한 패키지 목록
├── .gitignore          ← Git에서 제외할 파일 목록
├── .env.example        ← 환경변수 예시 파일
├── .env                ← (직접 생성) 실제 API 키 입력
├── .venv/              ← (직접 생성) 가상환경 폴더
├── exercise1.py        ← 실습 파일 1
└── exercise2.py        ← 실습 파일 2
```

---

## 도움이 필요하면?

세션 중 손을 들어 질문해 주세요!
