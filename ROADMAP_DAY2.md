# Day 2 로드맵 — 도구만들기 2일차

> 📌 **출처**: Notion — 도구만들기 2일차 실습 가이드
> https://byeordinary.notion.site/2-37bf9388619c81f2b8b2f2b0510c5818
>
> 이 문서는 **진행 중인 로드맵 / 작업 트래커**입니다(Day 1 회고 [INSIGHTS.md](INSIGHTS.md)와 짝).
> 단계 번호는 노션 섹션 제목 기준(0~5)입니다. 완료된 단계는 정본 문서를 가리키고,
> 남은 단계는 여기서 추적합니다. 구현되면 [SETUP_GUIDE.md](SETUP_GUIDE.md)·[CLAUDE.md](CLAUDE.md)에 반영하세요.

**필수 계정**: GitHub, Anthropic(API 키), Supabase
**필수 프로그램**: Python 3.11+, Git, VSCode, Claude Code

---

## 전체 흐름도

```
0. 준비 확인 (계정 · 프로그램)
        ↓
1. CSV 대시보드 띄우기
        ↓
2. Claude API 요약 기능 추가
        ↓
3. Supabase 원격 DB 연동 (+ 중복 방지 업로드)
        ↓
4. 스킬로 자동 리포트 생성
        ↓
5. GitHub에 안전하게 업로드
```

---

## 진행 현황 요약

| 단계 | 내용 | 상태 | 정본 / 다음 작업 |
|------|------|------|------------------|
| 0 | 준비 확인 (계정·프로그램) | ✅ 완료 | 아래 §0 |
| 1 | CSV 대시보드 띄우기 | ✅ 완료 | [WORKFLOW_VISUAL_GUIDE.md](WORKFLOW_VISUAL_GUIDE.md), [INSIGHTS.md](INSIGHTS.md) |
| 2 | Claude API 요약 기능 | ✅ 완료 | [SETUP_GUIDE.md](SETUP_GUIDE.md) Phase 4 |
| 3 | Supabase 원격 DB (+ 중복 방지) | 🟡 부분 | [SETUP_GUIDE.md](SETUP_GUIDE.md) Phase 2·6 / 아래 §3 |
| 4 | 스킬 자동 리포트 | ❌ 미착수 | 아래 §4 |
| 5 | GitHub 업로드 | 🟢 푸시 완료 | 아래 §5 |

---

## §0 — 준비 확인 ✅

**목표**: 계정과 프로그램이 갖춰졌는지 점검한다.

- **계정**: GitHub, Anthropic(API 키 발급), Supabase
- **프로그램**: Python 3.11+, Git, VSCode, Claude Code
- **현황**: 프로젝트가 실행되고 git·원격까지 연결되어 있으므로 사전 준비는 충족.

---

## §1 — CSV 대시보드 띄우기 ✅

**목표**: 깃허브 시작용 프로젝트를 받아 CSV 대시보드를 띄운다.

- **현황**: 이 프로젝트가 그 결과물입니다. 매출 카드 3개 + 추이/비중 차트 동작 중.
- **성공 확인**: "브라우저에 매출 카드 3개와 추이·비중 차트가 보이면 성공."
- **함정**: VSCode Pylance가 import를 못 찾으면 인터프리터를 `.venv`로 선택하고 패키지도 같은 위치에 설치. ([TROUBLESHOOTING.md](TROUBLESHOOTING.md))
- **참고**: 환경 구축·문제 해결 기록은 [INSIGHTS.md](INSIGHTS.md)(Day 1).

---

## §2 — Claude API 요약 기능 추가 ✅

**목표**: 버튼을 누르면 Claude가 그날 매출을 한국어 경영진 요약으로 스트리밍.

- **현황**: [app.py](app.py)에 "오늘 매출 AI 요약" 버튼 구현 완료. `claude-opus-4-8` + `messages.stream` + `st.write_stream`.
- **키 처리**: `st.secrets["anthropic"]["api_key"]` → `st.secrets["ANTHROPIC_API_KEY"]` → 환경변수 순. 키 없으면 안내만 표시.
- **성공 확인**: "버튼 클릭 시 요약 글이 실시간으로 흘러나오면 성공."
- **⚠️ API 키 주의**: 코드·깃허브에 절대 올리지 말 것. `.streamlit/secrets.toml`(깃 제외) 또는 환경변수에만 보관. 비밀 파일은 PC마다 새로 생성.
- **정본**: [SETUP_GUIDE.md](SETUP_GUIDE.md) Phase 4.

---

## §3 — Supabase 원격 DB 연동 (+ 중복 방지 업로드) 🟡

**목표**: CSV 대신 원격 DB에서 읽어 어느 컴퓨터에서나 같은 데이터를 본다.

**커리큘럼 프롬프트:**
```
supabase MCP를 전역(user scope)으로 추가해줘. https://mcp.supabase.com/mcp, http 방식.
```
```
지금은 CSV 파일로 데이터를 읽고 있는데, 이걸 Supabase 원격 데이터베이스에서 읽도록 바꿔줘.
1) sales 테이블을 만들고  2) 누구나 읽을 수 있도록 설정한 뒤
3) 지금 CSV에 있는 데이터를 그 테이블에 넣고  4) 대시보드가 그 원격 DB를 조회하도록 연결해줘.
```
```
filesystem MCP를 설치해줘. npx 방식으로, 내 작업 폴더(매출도구 폴더)에 접근할 수 있게.
```

- **현황(부분 완료)**:
  - ✅ `load_sales_data()`가 Supabase 우선 → CSV 폴백 구조로 구현됨
  - ✅ [.mcp.json](.mcp.json)에 Supabase MCP(project ref `nqktdzbebjjwhmwnspha`) 구성됨
  - ✅ `GRANT SELECT ON public.sales TO anon;` 권한 절차 문서화됨 ([SETUP_GUIDE.md](SETUP_GUIDE.md) Phase 6)
- **남은 작업**:
  - [ ] 로컬 `.streamlit/secrets.toml`에 실제 Supabase `url`/`key` 입력 (현재 placeholder)
  - [ ] filesystem MCP 추가 (선택)
  - [ ] **중복 방지 업로드**: 유일키(예: `date`+`product`+`broadcast_time`) + 업서트(덮어쓰기)로 적재해 재실행 시 중복 방지
- **성공 확인**: "CSV 파일을 지워도 대시보드가 똑같이 뜨면 성공(원격에서 읽는 중)." / 같은 적재를 두 번 돌려도 행 수가 늘지 않으면 중복 방지 성공.
- **주의**: publishable=읽기(공개 OK) vs service_role=쓰기(비밀, 공개 금지). 새 Supabase 프로젝트는 요금 발생 가능 → 기존 프로젝트 재사용 권장.

---

## §4 — 스킬로 자동 리포트 생성 ❌

**목표**: 반복 작업을 스킬로 만들어 한마디로 주간 리포트가 자동 생성되게 한다.

**커리큘럼 프롬프트:**
```
"주간 매출 리포트" 스킬을 만들어줘. claude/commands/weekly-sales-report.md에 저장하고,
data/template.docx 구조를 반영해서 Supabase 조회 → 보고서 작성 → Word 파일 저장까지
절차를 기술해줘. frontmatter의 name/description + 마크다운 본문 섹션들을 따라줘.
```

- **현황**: 미착수. `weekly-sales-report.md` 스킬 파일 없음, `data/template.docx` 없음.
- **남은 작업**:
  - [ ] `data/template.docx` 서식 준비
  - [ ] `.claude/commands/weekly-sales-report.md` 스킬 작성 (frontmatter `name`/`description` + 본문)
  - [ ] 절차: Supabase 조회 → 보고서 작성 → `.docx` 저장
- **실행 방법**: Claude Code에서 `/reload-skills` 후 → `4월 2주차 주간 매출 리포트를 작성해줘`
- **성공 확인**: 제목 + 카테고리 표 + 요약이 자동 생성되면 성공.
- **함정**: 스킬에 워드 저장 기능이 없으면 데이터만 추출됨(별도 요청 필요). 리포트 숫자는 암산 금지(스크립트 계산). `.docx`가 Word에서 열려 있으면 저장 잠김 → 닫고 재시도. "최근 7일"이 0건이면 기준일을 데이터 최신일로. 스킬은 계속 업데이트.

---

## §5 — GitHub에 안전하게 업로드 🟢

**목표**: 작업물을 깃허브에 올려 다른 PC에서 이어서 작업하고, 비밀이 새지 않게 한다.

**커리큘럼 프롬프트:**
```
지금까지 작업한 프로젝트를 깃허브에 올려줘. 다른 PC에서도 이어서 개발할 수 있게.
올리기 전에 API 키 같은 비밀정보가 포함되지 않았는지 점검하고, 저장소는 비공개(Private)로 만들어줘.
```
```
방금 깃허브에 올린 내용에 API 키나 비밀정보가 들어갔는지 다시 점검해줘.
```
```
이 깃허브 저장소를 새 컴퓨터에서 받아 이어서 개발할 수 있게 설정해줘.
필요한 가상환경과 패키지 설치, 비밀 키(secrets) 재설정 방법까지 안내해줘.
```

- **현황**:
  - ✅ 원격 연결됨: `github.com/triz4you0602-rower/test260604`
  - ✅ 비밀 점검 통과(추적 파일에 키 없음) 후 커밋·푸시 완료 (`origin/master` 동기화)
- **남은 작업(선택)**:
  - [ ] 저장소 **Private** 전환 여부 검토 (현재 `data/sales.csv` 매출 데이터 공개 여부 확인)
  - [ ] 새 PC 이어받기 절차 문서화(가상환경·패키지·secrets 재설정)
- **성공 확인**: "깃허브에 올라가고, 비밀정보 점검에서 '없음'이 나오면 성공." → 달성.
- **주의**: `.venv`·`secrets.toml`은 올리지 않음(새 PC에서 재생성). 결과물(.docx/.pptx)도 코드가 아니므로 제외. 공개/비공개는 저장소 Settings → Danger Zone → Change visibility.

---

## 핵심 팁

> 각 단계는 독립적입니다. 막히면 그 단계의 프롬프트만 다시 붙여넣고, 에러 메시지를
> Claude에게 그대로 보여주면 됩니다. **"이 에러 왜 났어? 고쳐줘"가 가장 강력한 프롬프트입니다.**

추가 함정·해결책은 [TROUBLESHOOTING.md](TROUBLESHOOTING.md)의 "Day 2 함정 빠른 참조"를 보세요.

---

**작성일**: 2026-06-11 (단계 번호를 노션 섹션 제목 기준으로 재정렬)
**상태**: 🟡 진행 중 (단계 0·1·2 완료, 3 부분, 5 푸시 완료, 4 남음)
