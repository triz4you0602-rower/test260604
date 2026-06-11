# CLAUDE.md

이 파일은 이 저장소에서 작업할 때 Claude Code(claude.ai/code)에 가이드를 제공합니다.

## 프로젝트 개요

홈앤쇼핑 일일 매출 현황 — 일일 매출 지표와 차트(Plotly 라인/파이)를 보여주는 단일 파일 Streamlit 대시보드([app.py](app.py))입니다. 모든 UI 텍스트, 데이터, 대부분의 문서가 한국어로 작성되어 있습니다. Streamlit Cloud `https://test260604-pcyo6o9mflydsgcr4i7owy.streamlit.app/`에 배포되어 있습니다.

## 명령어

```powershell
# 설정 (Windows)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 대시보드 실행 (`python -m` 사용 — 맨 `streamlit`은 PATH에 없는 경우가 많음)
python -m streamlit run app.py
# → http://localhost:8501

# 이전 실행으로 포트 8501이 막혀 있을 때
netstat -ano | findstr "8501"
taskkill /F /IM python.exe
```

테스트나 린터는 구성되어 있지 않습니다.

`generate_diagrams.py`(문서용 다이어그램 생성기)는 `matplotlib`이 필요하지만, 이는 의도적으로 requirements.txt에 **포함하지 않았습니다** — 이 스크립트를 실행할 때 별도로 설치하세요.

## 아키텍처

**데이터 로딩은 자동 폴백을 갖춘 이중 소스 방식입니다** ([app.py](app.py)의 `load_sales_data()`):
1. 먼저 Supabase를 시도하며, `st.secrets["supabase"]`(`url`, `key`)의 자격증명을 사용합니다
2. 어떤 실패든(비밀 누락, 권한 오류, 네트워크) 발생하면 `data/sales.csv`로 폴백하고 `st.warning`을 표시합니다

즉, Supabase가 설정되지 않아도 앱은 항상 실행됩니다 — 경고 배너는 버그가 아니라 예상된 동작입니다.

**AI 요약 (Claude API):** "오늘 매출 AI 요약" 버튼은 선택한 날짜의 매출에 대한 한국어 경영진용 요약을 Anthropic Python SDK(`claude-opus-4-8`, `client.messages.stream` + `st.write_stream`)를 통해 스트리밍합니다. API 키는 `st.secrets["anthropic"]["api_key"]`, 그다음 `st.secrets["ANTHROPIC_API_KEY"]`, 그다음 `ANTHROPIC_API_KEY` 환경변수 순으로 해석됩니다 — 절대 하드코딩하지 마세요. 키가 없으면 크래시 대신 `st.info` 설정 안내를 표시합니다.

**Supabase 설정:**
- 로컬 비밀은 `.streamlit/secrets.toml`(gitignore 처리됨)에 들어가며, Streamlit Cloud 비밀은 앱의 Settings → Secrets에서 설정합니다
- 테이블: `sales`, 컬럼은 `id, date, category, product, broadcast_time, sales, orders, host, created_at`
- 배포된 앱은 `anon` 역할로 읽으므로 `GRANT SELECT ON public.sales TO anon;`이 필요합니다 — "permission denied for table sales"는 이 권한이 누락되었다는 의미입니다
- `.mcp.json`은 Claude Code에서 DB에 직접 접근하기 위한 Supabase MCP 서버(프로젝트 ref `nqktdzbebjjwhmwnspha`)를 구성합니다

**데이터 규칙:**
- `data/sales.csv`는 한국어 텍스트가 포함된 UTF-8입니다 — PowerShell 콘솔 출력에서 깨져 보일 수 있으나 파일 자체는 정상입니다
- 차트는 한국어 폰트 스택(`Malgun Gothic, AppleGothic, NanumGothic`)과 `₩` + 천 단위 콤마 형식을 사용합니다. 차트를 수정할 때 둘 다 유지하세요
- "오늘"은 실제 현재 날짜가 아니라 `df['date'].max()`로 도출합니다

**문서 파일**은 각각 단일 역할을 가집니다(2026-06-11 통합):
- **SETUP_GUIDE.md** — 활성 실행 가이드: Supabase + AI 요약 + 배포 전체 흐름. 가장 유용한 살아있는 가이드.
- **TROUBLESHOOTING.md** — 단일 문제 해결 레퍼런스(구 DEPENDENCY_ISSUE.md / Plotly 가이드를 흡수, Day 2 함정 표 포함).
- **ROADMAP_DAY2.md** — 진행 중인 Day 2 로드맵/트래커(Notion 2일차 커리큘럼 기반). 단계 0·1 완료, 2 부분, 3(중복 방지)·4(주간 리포트 스킬)·5(깃허브)는 미착수.
- **WORKFLOW_VISUAL_GUIDE.md** — 동결된 Day-1 스냅샷; 아키텍처 다이어그램 / ASCII 플로우차트의 정본.
- **INSIGHTS.md** — 동결된 Day-1 학습 회고(코드 통계와 수치는 2026-06-04 기준이며 의도적으로 갱신하지 않음).

동결된 두 문서는 살아있는 스펙이 아니라 저널입니다 — 통계를 갱신하지 마세요. `.txt` 쌍둥이 파일과 DEPENDENCY_ISSUE.md는 중복이라 제거되었습니다.
