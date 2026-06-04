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

| 라이브러리 | 버전 | 역할 |
|-----------|------|------|
| streamlit | 1.58.0 | 대시보드 프레임워크 |
| pandas | - | 데이터 처리 |
| plotly | - | 차트 시각화 |

---

## 💡 주요 학습 포인트

1. **Python 모듈 실행**: PATH 문제 해결 위해 `python -m` 사용
2. **포트 충돌 관리**: `netstat` 로 포트 상태 확인 및 프로세스 종료
3. **Streamlit 특성**: 브라우저 기반 앱, 자동 핫 리로드 지원

---

## 🚀 향후 개선 사항

- Streamlit을 시스템 PATH에 등록하기 (선택사항)
- 다른 포트(예: 8502)에서 다중 인스턴스 실행
- 데이터 자동 새로고침 설정
- 필터 기능 추가

