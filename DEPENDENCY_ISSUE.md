# ModuleNotFoundError: Plotly 라이브러리 해결 가이드

## 🐛 에러 상황

### 에러 메시지
```
ModuleNotFoundError: This app has encountered an error.

Traceback:
File "/mount/src/test260604/app.py", line 3, in <module>
    import plotly.express as px
```

### 원인 분석

| 항목 | 상태 |
|------|------|
| streamlit | ✅ 설치됨 (1.58.0) |
| pandas | ✅ 설치됨 (3.0.3) |
| plotly | ❌ **설치 안 됨** |

**문제점**: `app.py`의 3번 줄에서 `plotly` 라이브러리를 import하려고 했지만, 설치되지 않음.

---

## 📦 필요한 라이브러리

### app.py 의존성
```python
import streamlit as st              # Streamlit 프레임워크
import pandas as pd                 # 데이터 처리
import plotly.express as px         # 차트 시각화 (고수준 API)
import plotly.graph_objects as go   # 차트 커스터마이징 (저수준 API)
```

### 설치 상태 확인
```powershell
pip list | findstr plotly
```

---

## ✅ 해결 방법

### **방법 1: Plotly만 설치 (빠른 해결)**

```powershell
pip install plotly
python -m streamlit run app.py
```

**소요 시간**: ~30초
**크기**: ~10MB

### **방법 2: 모든 패키지 일괄 설치 (권장)**

#### 2-1. requirements.txt 파일 생성
```powershell
cd c:\test01
echo streamlit==1.58.0 > requirements.txt
echo pandas>=1.3.0 >> requirements.txt
echo plotly>=5.0.0 >> requirements.txt
```

또는 제공된 [requirements.txt](requirements.txt) 파일 사용

#### 2-2. 설치
```powershell
pip install -r requirements.txt
python -m streamlit run app.py
```

**장점**:
- 버전 관리 용이
- 팀원과 동일한 환경 공유 가능
- 재현 가능성 높음
- 배포 시 필수

---

## 🔍 라이브러리 상세 정보

### Streamlit (1.58.0)
- **역할**: 웹 대시보드 프레임워크
- **용도**: UI 구성, 메트릭 카드, 레이아웃
- **설치**: ✅ 완료

### Pandas (3.0.3)
- **역할**: 데이터 처리 라이브러리
- **용도**: CSV 읽기, 데이터 집계, 그룹화
- **설치**: ✅ 완료

### Plotly (6.8.0) ⭐
- **역할**: 대화형 차트 라이브러리
- **용도**: 
  - `px.line()`: 일별 매출 추이 차트
  - `px.pie()`: 카테고리별 매출 비중 차트
- **설치**: ✅ 완료

---

## 🚀 최종 실행 명령

```powershell
cd c:\test01
python -m streamlit run app.py
```

### 예상 결과
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

## 📊 대시보드 확인 체크리스트

대시보드 로드 후 다음을 확인하세요:

- [ ] 제목: "홈앤쇼핑 일일 매출 현황" 표시
- [ ] 지표 카드 3개 표시
  - [ ] 오늘 매출: ₩111,108,431
  - [ ] 어제 매출: ₩71,026,016
  - [ ] 어제 대비 증감률: +56.4%
- [ ] 좌측 차트: 일별 매출 추이 (선 그래프)
- [ ] 우측 차트: 카테고리별 매출 비중 (원 그래프)
- [ ] 한글 텍스트가 깨지지 않음
- [ ] 금액이 ₩ 기호와 천 단위 콤마로 표시

---

## 🛠️ 트러블슈팅

### 여전히 ModuleNotFoundError 발생하는 경우

#### 1️⃣ 설치 확인
```powershell
pip list | findstr "streamlit pandas plotly"
```

#### 2️⃣ 강제 재설치
```powershell
pip install --upgrade --force-reinstall plotly
python -m streamlit run app.py
```

#### 3️⃣ 가상 환경 확인
```powershell
# 현재 Python 경로 확인
python -c "import sys; print(sys.prefix)"

# 설치 경로 확인
pip show plotly
```

#### 4️⃣ pip 업그레이드
```powershell
python -m pip install --upgrade pip
pip install plotly
```

---

## 📝 참고: app.py 구조

```
app.py
├── import 섹션 (라이브러리 로드)
├── 데이터 로드
│   └── CSV 읽기 및 전처리
├── 계산 섹션
│   ├── 오늘 매출 계산
│   ├── 어제 매출 계산
│   └── 증감률 계산
├── UI 구성
│   ├── 제목
│   ├── 지표 카드 3개
│   └── 차트 2개
│       ├── 선 차트 (Plotly)
│       └── 원 차트 (Plotly)
└── 스타일링
    └── 한글 폰트 설정
```

---

## 🌐 배포 시 고려사항

### Streamlit Cloud 배포 시
- `requirements.txt` 파일 필수 제출
- 파일 경로가 상대경로로 설정되어야 함
- `data/sales.csv` 파일도 함께 업로드

### 로컬 개발 시
- `requirements.txt`로 환경 재현 가능
- `python -m streamlit run app.py` 명령어 사용

---

## ✅ 체크리스트: 완전 해결 확인

- [x] requirements.txt 생성
- [x] plotly 설치 확인
- [x] streamlit 실행 성공
- [x] 대시보드 로드 확인
- [x] 모든 차트가 정상 표시됨
- [x] 한글이 깨지지 않음
- [x] 금액 형식이 올바름 (₩ + 콤마)

