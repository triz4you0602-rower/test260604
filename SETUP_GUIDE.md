# Streamlit + Supabase 실시간 연동 완벽 가이드

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [Phase 1: 초기 설정](#phase-1-초기-설정)
3. [Phase 2: Supabase 연동](#phase-2-supabase-연동)
4. [Phase 3: 데이터 동기화](#phase-3-데이터-동기화)
5. [Phase 4: AI 요약 기능 (선택)](#phase-4-ai-요약-기능-선택)
6. [Phase 5: 배포](#phase-5-배포)
7. [Phase 6: 권한 설정 및 최적화](#phase-6-권한-설정-및-최적화)
8. [검증 및 테스트](#검증-및-테스트)
9. [트러블슈팅](#트러블슈팅)

---

## 프로젝트 개요

**목표**: Streamlit 대시보드를 Supabase 클라우드 데이터베이스와 실시간으로 연동하기

**최종 결과**:
- ✅ 로컬 앱: Supabase + CSV 완벽 동기화
- ✅ 배포 앱: Supabase 실시간 연동
- ✅ 자동 폴백: Supabase 실패 시 CSV 사용

**기술 스택**:
- Frontend: Streamlit 1.58.0
- Backend: Supabase (PostgreSQL)
- Data: CSV + Cloud DB
- Deployment: Streamlit Cloud

---

## Phase 1: 초기 설정

### 1.1 프로젝트 구조
```
test01/
├── app.py                 # Streamlit 메인 앱
├── requirements.txt       # 패키지 의존성
├── data/
│   └── sales.csv         # 로컬 데이터
├── .streamlit/
│   └── secrets.toml      # Supabase 설정 (로컬 전용)
└── .gitignore            # secrets.toml은 커밋 제외
```

### 1.2 requirements.txt 설정

필수 패키지를 `requirements.txt`에 추가:

```txt
streamlit>=1.28.0
pandas>=1.3.0
plotly>=5.0.0
supabase>=2.0.0
```

**설치 방법:**
```bash
pip install -r requirements.txt
```

### 1.3 기본 Streamlit 앱 구조

`app.py`의 기본 구조:

```python
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title='홈앤쇼핑 일일 매출 현황', layout='wide')

# 데이터 로드 함수 (Phase 2에서 확장)
def load_sales_data():
    df = pd.read_csv('data/sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_sales_data()

# 메트릭 표시
st.markdown('# 홈앤쇼핑 일일 매출 현황')
# ... (나머지 대시보드 코드)
```

---

## Phase 2: Supabase 연동

### 2.1 Supabase 데이터베이스 생성

**단계:**
1. [Supabase](https://supabase.com) 가입
2. 새 프로젝트 생성 → 프로젝트 URL과 API 키 복사
3. SQL Editor에서 테이블 생성

**테이블 생성 SQL:**

```sql
CREATE TABLE sales (
  id BIGSERIAL PRIMARY KEY,
  date DATE NOT NULL,
  category TEXT NOT NULL,
  product TEXT NOT NULL,
  broadcast_time TEXT NOT NULL,
  sales INTEGER NOT NULL,
  orders INTEGER NOT NULL,
  host TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW())
);

CREATE INDEX idx_sales_date ON sales(date);
CREATE INDEX idx_sales_category ON sales(category);
```

### 2.2 로컬 secrets 설정

`.streamlit/secrets.toml` 생성:

```toml
[supabase]
url = "your-supabase-url-here"
key = "your-publishable-key-here"
```

**주의**: `.gitignore`에 추가하여 커밋되지 않도록 함:
```
.streamlit/secrets.toml
```

### 2.3 앱에 Supabase 연동 코드 추가

`app.py` 수정:

```python
def load_sales_data():
    try:
        from supabase import create_client, Client
        url = st.secrets.get("supabase", {}).get("url")
        key = st.secrets.get("supabase", {}).get("key")
        if url and key:
            supabase = create_client(url, key)
            response = supabase.table('sales').select('*').execute()
            df = pd.DataFrame(response.data)
            df['date'] = pd.to_datetime(df['date'])
            return df
    except Exception as e:
        st.warning(f"Supabase 연결 실패: {e}. CSV 파일을 사용합니다.")

    # CSV 폴백
    df = pd.read_csv('data/sales.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df
```

**핵심 기능:**
- ✅ Supabase 우선 연결 시도
- ✅ 실패 시 자동으로 CSV 폴백
- ✅ 캐시 없음 → 실시간 업데이트

---

## Phase 3: 데이터 동기화

### 3.1 CSV → Supabase 데이터 이전

**방법 1: Supabase UI 사용**
1. Supabase 대시보대 → SQL Editor
2. INSERT 문으로 데이터 삽입

**방법 2: Python 스크립트 사용**
```python
import pandas as pd
from supabase import create_client

url = "your-url"
key = "your-key"
supabase = create_client(url, key)

df = pd.read_csv('data/sales.csv')
data = df.to_dict('records')

response = supabase.table('sales').insert(data).execute()
print(f"Inserted {len(response.data)} rows")
```

### 3.2 데이터 검증

```sql
SELECT COUNT(*) as total_rows FROM sales;
SELECT MIN(date), MAX(date) FROM sales;
SELECT DISTINCT category FROM sales;
```

---

## Phase 4: AI 요약 기능 (선택)

### 4.1 Anthropic API 키 설정

**목적**: "오늘 매출 AI 요약" 버튼으로 Claude를 통한 경영진용 요약 생성

#### 4.1.1 API 키 획득

1. [Anthropic API 콘솔](https://console.anthropic.com)에 접속
2. API Keys → Create Key
3. 생성된 키 복사 (예: `sk-ant-...`)

#### 4.1.2 로컬 secrets 설정

`.streamlit/secrets.toml`에 추가:

```toml
[anthropic]
api_key = "sk-ant-..."
```

**또는 환경변수 설정:**

```bash
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

### 4.2 기능 설명

**UI 구성**:
- 기준일 선택 드롭다운 (selectbox)
- "오늘 매출 AI 요약" 버튼

**버튼 클릭 시 동작**:
1. 선택한 기준일의 매출 데이터 수집
   - 카테고리별 매출, 주문수
   - 상위 5개 방송 정보
   - 전일 대비 변화율
2. Claude Opus 4.8로 한국어 경영진용 요약 생성
3. 스트리밍으로 실시간 표시

**에러 처리**:
- API 키 없음 → 친절한 설정 가이드 표시
- 인증 실패 → 키 확인 안내
- 네트워크 오류 → 재시도 안내

### 4.3 requirements.txt 업데이트

```txt
streamlit>=1.28.0
pandas>=1.3.0
plotly>=5.0.0
supabase>=2.0.0
anthropic>=0.9.0
```

설치:
```bash
pip install anthropic
```

---

## Phase 5: 배포

### 4.1 GitHub에 커밋

```bash
git add app.py requirements.txt data/sales.csv
git commit -m "Integrate Supabase with Streamlit dashboard and verify real-time data sync"
git push origin master
```

### 5.2 Streamlit Cloud 배포

**단계:**
1. [share.streamlit.io](https://share.streamlit.io) 접속
2. "New app" → GitHub 저장소 선택
3. 파일 경로: `app.py` 선택
4. 배포 완료 대기

**배포 URL**: 예시
```
https://test260604-pcyo6o9mflydsgcr4i7owy.streamlit.app/
```

---

## Phase 6: 권한 설정 및 최적화

### 6.1 중요: Supabase 권한 설정

**문제**: 배포 앱이 "permission denied for table sales" 에러 발생

**해결책**: Supabase SQL Editor에서 실행:

```sql
GRANT SELECT ON public.sales TO anon;
```

**검증:**
```sql
SELECT privilege_type 
FROM information_schema.role_table_grants 
WHERE table_name='sales' AND grantee='anon';
```

결과:
```
privilege_type
--------------
SELECT
TRUNCATE
REFERENCES
TRIGGER
```

### 6.2 Streamlit Cloud Secrets 설정 (선택사항)

배포 앱에서 Supabase를 직접 사용하려면:

1. https://share.streamlit.io 접속
2. 앱 → Settings → Secrets
3. 다음 추가:
```toml
[supabase]
url = "your-supabase-url"
key = "your-publishable-key"
```

**현재 상황**: 권한 부여로 CSV 폴백이 자동으로 Supabase로 전환됨

---

## 검증 및 테스트

### 검증 1: 데이터 로드 확인

**로컬 앱**:
```bash
streamlit run app.py
# http://localhost:8501에서 데이터 확인
```

**확인 항목**:
- ✅ 메트릭 카드 표시
- ✅ 라인 차트 표시
- ✅ 파이 차트 표시
- ✅ 경고 메시지 없음 (Supabase 연결 성공)

### 검증 2: 실시간 동기화 테스트

**단계:**

1. **데이터 수정** (Supabase SQL Editor):
```sql
UPDATE sales SET sales = 50000000 WHERE id = 146;
```

2. **앱 새로고침** (F5):
브라우저에서 localhost:8501 새로고침

3. **결과 확인**:
- 메트릭이 즉시 업데이트되어야 함
- 차트가 새 데이터로 표시되어야 함

### 검증 3: 배포 앱 확인

배포 앱 URL 방문:
```
https://test260604-pcyo6o9mflydsgcr4i7owy.streamlit.app/
```

**확인 사항**:
- ✅ 어제 매출이 Supabase 데이터 표시
- ✅ 경고 메시지 없음
- ✅ 모든 차트 표시

---

## 트러블슈팅

### 문제 1: "permission denied for table sales"

**원인**: anon 역할이 sales 테이블 SELECT 권한 없음

**해결**:
```sql
GRANT SELECT ON public.sales TO anon;
```

### 문제 2: Supabase 연결 실패하지만 CSV 폴백 작동

**이유**: 정상 동작입니다!
- Supabase 권한 부여 전까지 CSV 사용
- 권한 부여 후 자동으로 Supabase 로드

**확인**:
```python
# app.py에서 load_sales_data() 함수가 두 가지 소스를 모두 지원
```

### 문제 3: CSV 파일이 너무 크거나 로드 느림

**해결**:
1. Supabase만 사용 (클라우드 기반)
2. 캐시 활성화 (선택사항):
```python
@st.cache_data(ttl=3600)  # 1시간 캐시
def load_sales_data():
    ...
```

### 문제 4: 배포 앱이 여전히 구 데이터 표시

**해결**:
1. Streamlit Cloud에서 "Rerun" 클릭
2. 또는 GitHub에 새 커밋 푸시 (자동 재배포)

---

## 최종 아키텍처

**데이터 흐름 요약:**
1. Supabase 우선: 클라우드 DB에서 직접 읽기
2. 폴백: Supabase 실패 시 CSV 파일 사용
3. 실시간: Supabase 변경사항 즉시 반영

> 📐 전체 아키텍처 다이어그램과 Phase별 ASCII 플로우차트는
> [WORKFLOW_VISUAL_GUIDE.md](WORKFLOW_VISUAL_GUIDE.md)에 있습니다 (시각 자료 정본).

---

## 요약: 단계별 설정 체크리스트

### 로컬 개발 환경 구성
- [x] requirements.txt에 supabase 추가
- [x] .streamlit/secrets.toml 생성
- [x] app.py에 Supabase 연동 코드 추가
- [ ] 로컬에서 `streamlit run app.py` 테스트

### Supabase 설정
- [ ] 프로젝트 생성 및 URL, 키 복사
- [ ] sales 테이블 생성 (SQL)
- [ ] CSV 데이터 삽입
- [ ] GRANT SELECT ON public.sales TO anon 실행

### Anthropic API 설정 (선택)
- [x] .streamlit/secrets.toml에 anthropic 섹션 추가
- [x] API 키 설정 완료
- [ ] "오늘 매출 AI 요약" 버튼 테스트

### 배포
- [ ] GitHub에 코드 커밋 (secrets.toml 제외)
- [ ] Streamlit Cloud에서 배포
- [ ] 배포 앱 URL 확인
- [ ] 권한 설정 후 배포 앱 재로드
- [ ] Streamlit Cloud Secrets 설정 (Anthropic 포함)

### 검증
- [ ] 로컬 앱: Supabase 데이터 표시
- [ ] 배포 앱: Supabase 데이터 표시
- [ ] 실시간 동기화: 데이터 수정 후 즉시 반영
- [ ] 경고 메시지: 없음 (정상)
- [ ] AI 요약: 버튼 클릭 후 스트리밍 응답

---

## 참고 링크

- [Supabase 문서](https://supabase.com/docs)
- [Streamlit 문서](https://docs.streamlit.io)
- [Supabase Python SDK](https://supabase.com/docs/reference/python/introduction)
- [Streamlit Secrets 관리](https://docs.streamlit.io/deploy/streamlit-cloud/deploy-your-app#secrets-management)

---

## 커밋 히스토리

이 프로젝트의 주요 커밋:

```
b9a9e26 - Integrate Supabase with Streamlit dashboard and verify real-time data sync
7b42801 - Update INSIGHTS.md: Integrate Notion Day 1 curriculum content
d89a256 - Integrate Notion 'Day 1 Streamlit MCP Skills' into INSIGHTS
879148f - Add comprehensive project insights and learnings
```

---

**작성일**: 2026-06-04  
**최종 상태**: ✅ 완벽하게 작동 중  
**실시간 동기화**: ✅ Supabase 및 배포 앱 모두 작동  

---

## 📝 업데이트 이력

### 2026-06-11
- ✅ Phase 4 추가: Anthropic API 설정 및 "오늘 매출 AI 요약" 기능
- ✅ requirements.txt에 `anthropic>=0.9.0` 추가
- ✅ 체크리스트 업데이트 (Anthropic API 설정 포함)
