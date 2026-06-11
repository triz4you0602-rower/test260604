# Streamlit 대시보드 문제 해결 가이드

## 📋 작업 개요
- **프로젝트**: 홈앤쇼핑 일일 매출 현황 Streamlit 대시보드
- **파일**: `app.py`
- **데이터**: `data/sales.csv`
- **작성 날짜**: 2026-06-04

---

## ❌ 발생했던 문제들

### 문제 1: `test_app.py` 파일을 찾을 수 없음
**에러 메시지:**
```
[Errno 2] No such file or directory: 'C:\\test01\\test_app.py'
```

**원인:**
- `test_app.py` 파일이 존재하지 않음
- IDE 또는 실행 도구의 설정에서 잘못된 파일명 참조
- 실제 파일명: `app.py`

**해결 방법:**
```bash
# 올바른 파일명으로 실행
python -m streamlit run app.py
```

---

### 문제 2: Streamlit이 PowerShell PATH에 등록되지 않음
**에러 메시지:**
```
streamlit : 'streamlit' 용어가 cmdlet, 함수, 스크립트 파일 또는 실행할 수 있는 프
로그램 이름으로 인식되지 않습니다.
```

**원인:**
- Streamlit이 설치되어 있으나 (버전: 1.58.0)
- Windows PowerShell의 환경 변수(PATH)에 등록되지 않음
- 직접 `streamlit` 명령어로는 실행 불가

**해결 방법:**
```powershell
# Python 모듈로 실행 (권장)
python -m streamlit run app.py
```

---

### 문제 3: 포트 충돌 (Port 8501 이미 사용 중)
**에러 메시지:**
```
Exit code 1
```

**원인:**
- 이전에 실행한 Streamlit 프로세스가 여전히 포트 8501을 점유
- 종료되지 않은 Python 프로세스가 메모리에 남아있음

**확인 방법:**
```powershell
netstat -ano | findstr "8501"
```

**해결 방법:**
```powershell
# 1. 모든 Python 프로세스 강제 종료
taskkill /F /IM python.exe

# 2. 잠시 대기 후 다시 실행
Start-Sleep -Seconds 2
python -m streamlit run app.py
```

---

### 문제 5: ModuleNotFoundError (Plotly 등 라이브러리 미설치)

**에러 메시지:**
```
ModuleNotFoundError: This app has encountered an error.
File "app.py", line 3, in <module>
    import plotly.express as px
```

**원인:**
- `requirements.txt`에 명시된 패키지가 로컬/배포 환경에 설치되지 않음
- 대표 사례: `plotly` 미설치 (차트 렌더링 불가)

**해결 방법:**
```powershell
# 방법 1: 개별 설치 (빠른 해결)
pip install plotly

# 방법 2: 일괄 설치 (권장 — 버전 관리·재현성)
pip install -r requirements.txt

python -m streamlit run app.py
```

**여전히 발생하는 경우:**
```powershell
# 설치 확인
pip show plotly

# 강제 재설치
pip install --upgrade --force-reinstall plotly

# 가상환경/Python 경로 확인
python -c "import sys; print(sys.prefix)"
```

> 💡 **학습 포인트**: 프로젝트 시작 시 `requirements.txt`를 먼저 만들고 유지하면
> 팀원·CI·배포 환경에서 이런 누락이 재발하지 않습니다.

---

## ✅ 최종 해결책

### 올바른 실행 방법
```powershell
cd c:\test01
python -m streamlit run app.py
```

### 실행 결과
```
Uvicorn server started on 0.0.0.0:8501

You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.45.204:8501
```

### 브라우저 접속
```
http://localhost:8501
```

---

### 문제 4: "오늘 매출 AI 요약" 버튼이 작동하지 않음

#### 4-1. Anthropic API 키가 설정되지 않음
**증상**: 버튼 클릭 시 "AI 요약을 사용하려면 Anthropic API 키가 필요합니다" 메시지 표시

**원인**:
- `.streamlit/secrets.toml`에 `[anthropic]` 섹션이 없음
- 환경변수 `ANTHROPIC_API_KEY`가 설정되지 않음

**해결 방법**:

1. **secrets.toml에 추가** (권장)
   ```toml
   [anthropic]
   api_key = "sk-ant-..."
   ```

2. **또는 환경변수 설정**
   ```powershell
   $env:ANTHROPIC_API_KEY = "sk-ant-..."
   ```

3. **Streamlit 재시작**
   ```powershell
   python -m streamlit run app.py
   ```

#### 4-2. API 키가 유효하지 않음
**에러 메시지**: "API 키가 유효하지 않습니다. 키를 확인해 주세요."

**원인**:
- 잘못된 API 키 입력
- API 키 만료 또는 비활성화
- 복사/붙여넣기 실수 (공백 포함)

**해결 방법**:
1. [api.anthropic.com](https://api.anthropic.com) 접속
2. API Keys에서 키 확인
3. 키가 "Active" 상태인지 확인
4. secrets.toml에 다시 입력 (공백 제거)

#### 4-3. 네트워크 오류
**에러 메시지**: "네트워크 연결에 실패했습니다."

**원인**:
- 인터넷 연결 끊김
- Anthropic API 서버 다운
- 방화벽 차단

**해결 방법**:
1. 인터넷 연결 확인
2. 몇 초 대기 후 다시 시도
3. Anthropic 상태 페이지 확인

#### 4-4. 요청 한도 초과
**에러 메시지**: "요청 한도를 초과했습니다. 잠시 후 다시 시도해 주세요."

**원인**:
- Rate limit 도달
- API 쿼타 초과

**해결 방법**:
1. 몇 분 후 재시도
2. 계정의 쿠터 설정 확인
3. Anthropic 콘솔에서 usage 모니터링

---

## 📊 대시보드 구성

### 표시되는 항목
1. **페이지 제목**: 홈앤쇼핑 일일 매출 현황
2. **지표 카드 3개**
   - 오늘 매출: ₩111,108,431
   - 어제 매출: ₩71,026,016
   - 어제 대비 증감률: +56.4%

3. **차트 2개**
   - 좌: 일별 매출 추이 (선 차트)
   - 우: 카테고리별 매출 비중 (원 차트)

### 스타일
- ✅ 금액 형식: `₩` 기호 + 천 단위 콤마
- ✅ 한글 폰트: Malgun Gothic / AppleGothic / NanumGothic
- ✅ 색상: 차분한 톤 (블루 메인)

---

## 🔧 설치된 라이브러리

| 라이브러리 | 버전 | 역할 | 필수 |
|-----------|------|------|------|
| streamlit | 1.58.0 | 대시보드 프레임워크 | ✅ |
| pandas | - | 데이터 처리 | ✅ |
| plotly | - | 차트 시각화 | ✅ |
| anthropic | 0.9.0+ | Claude API 클라이언트 | ❌ (선택) |
| supabase | 2.0.0+ | Supabase 연동 | ❌ (선택) |

---

## 🧭 Day 2 함정 빠른 참조

> 출처: Notion 도구만들기 2일차 종합 문제 해결 표. 단계별 로드맵은 [ROADMAP_DAY2.md](ROADMAP_DAY2.md) 참조.

| 상황 / 함정 | 이렇게 하세요 |
|---|---|
| VSCode가 import를 못 찾음 (Pylance) | 인터프리터를 `.venv`로 선택 + 패키지도 `.venv`에 설치 |
| API 키 노출 걱정 | `secrets.toml`/환경변수에만, 코드·깃에 절대 금지 |
| 비밀 파일이 새 PC에 없음 | `secrets.toml`은 PC마다 새로 생성 (깃 제외됨) |
| Supabase 새 프로젝트 요금 | 기존 활성 프로젝트 재사용 |
| 공개 키 vs 비밀 키 헷갈림 | `publishable`=읽기(공개 OK), `service_role`=쓰기(비밀, 공개 금지) |
| "최근 7일"이 0건 | 기준일을 데이터 최신일로 설정 (`df['date'].max()`) |
| 데이터 중복 | 중복 방지(유일키 + 덮어쓰기/업서트) 요청 |
| 리포트 숫자가 틀림 | 계산은 스크립트로(암산 금지) 요청 |
| `.docx` 저장이 안 됨 | Word에서 파일 닫고 다시 시도 (파일 잠금) |
| 깃에 비밀 올라갈까 걱정 | 올리기 전 "비밀정보 점검해줘" 요청 |

---

## 💡 주요 학습 포인트

1. **Python 모듈 실행**: PATH 문제 해결 위해 `python -m` 사용
2. **포트 충돌 관리**: `netstat` 로 포트 상태 확인 및 프로세스 종료
3. **Streamlit 특성**: 브라우저 기반 앱, 자동 핫 리로드 지원
4. **에러 그대로 보여주기**: 막히면 에러 메시지를 Claude에게 그대로 붙여넣고 "왜 났어? 고쳐줘"

---

## 🚀 향후 개선 사항

- Streamlit을 시스템 PATH에 등록하기 (선택사항)
- 다른 포트(예: 8502)에서 다중 인스턴스 실행
- 데이터 자동 새로고침 설정
- 필터 기능 추가

---

## 📝 업데이트 이력

### 2026-06-11
- ✅ 문제 4 추가: Anthropic API 설정 및 사용 시 문제 해결
- ✅ 라이브러리 테이블에 anthropic 및 supabase 추가
- ✅ 4개의 세부 문제 시나리오 추가 (키 미설정, 유효하지 않은 키, 네트워크 오류, 한도 초과)
- ✅ **문제 5 추가**: Plotly 등 라이브러리 미설치 (구 `DEPENDENCY_ISSUE.md` 흡수 — 이 문서가 트러블슈팅 정본)
- ✅ **"Day 2 함정 빠른 참조" 표 추가**: Notion 2일차 종합 문제 해결 표 반영 (Pylance, 키 구분, 중복, .docx 잠금 등 10항목)

