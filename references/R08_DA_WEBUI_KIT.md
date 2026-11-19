# DrimAES Light Web UI Kit · v1.0

> Next.js 14 + TypeScript + Tailwind CSS 3 기반의 **라이트 모드** 슬라이드/도큐멘트 UI 디자인 시스템.
> `DA_WEB_darkUI_KIT.md`(v1.3)의 **레이아웃·컴포넌트·인터랙션 체계를 그대로 유지**하면서,
> 컬러 테마만 `DA_ppt_design_guide.md`(v2.1)의 **PPT 라이트 캔버스 시스템**(흰 바탕 · 회사 8색 · 네이비 프라이머리)을 이식했습니다.
>
> 제작: 2026-07-10 · **Claude Fable 5와 공동 제작** · 다크 키트 v1.3의 잔존 바이올렛 값(§5 gradient-text 예시, 사이드바 글로우 rgba(139,169,255))은 본 킷에서 회사 토큰으로 정정됨.

---

## ⚠ 적용 범위 (Scope)

본 키트는 **웹페이지(HTML/CSS/JavaScript) 기반 문서 전용**입니다. PPT·Word·PDF·Figma에는 적용하지 마세요 — 인쇄·문서용은 `DA_ppt_design_guide.md`를 사용합니다. 다크 모드가 필요하면 `DA_WEB_darkUI_KIT.md`를 사용하세요. 두 웹 키트는 **같은 레이아웃 체계**를 공유하므로 토큰 매핑(§4.8)만으로 상호 전환이 가능합니다.

| 매체 | 적용 가능? |
|---|---|
| **웹페이지 (Next.js / React / 정적 HTML) · 라이트 테마** | ✅ 정식 대상 |
| 웹페이지 · 다크 테마 | ❌ → `DA_WEB_darkUI_KIT.md` |
| PowerPoint / Word / PDF / Figma | ❌ → `DA_ppt_design_guide.md` (PPT) 또는 별도 가이드 |

---

## 0. 다른 AI 세션에서 사용하는 법

이 파일을 새 채팅에 그대로 첨부한 뒤 다음 형식으로 요청하세요:

> 첨부한 `DA_WEBUI_KIT.md` v1.0 디자인 시스템을 그대로 사용해서, **[프로젝트 설명]** 을 Next.js 14 App Router 프로젝트로 만들어줘.
> 좌측 사이드바 SPA, **라이트 테마(흰 캔버스)**, 챕터 번호 prefix, 슬라이드 진입 애니메이션, BlockFlow/FlowDiagram, Card/Callout/DataTable+SoWhat 그대로 사용. 본문 컨테이너 `max-w-[82rem]`, 텍스트는 §5 표 기준. Vercel 배포 가능 구조.

---

## 1. 디자인 철학

| 원칙 | 의미 |
|---|---|
| **라이트 우선** | 연회색 캔버스(`#F4F5F7`) 위 흰색 페이퍼 카드. PPT 문서와 같은 톤·같은 위계. |
| **페이퍼 + 네이비** | 카드는 흰 배경 + `#DEDEDE` 보더 + 옅은 그림자. 강조는 **네이비 솔리드 + 흰 텍스트**. |
| **회사 8색 전용** | 모든 액센트는 회사 8색 + 구조 중립색만. 빨강·노랑·주황·보라 등 의미색 도입 금지 (PPT §1.3과 동일). |
| **슬라이드 SPA** | 긴 스크롤 대신 사이드바 → 슬라이드 한 페이지 교체. 키보드 ←/→ 지원. |
| **번호 + 모노 prefix** | 사이드바·슬라이드 헤더에 `01`/`02`/`A` 모노스페이스 prefix로 지도감 강화. |
| **부드러운 인터랙션** | hover에 -1~2px 리프트, 보더 색 변경, 네이비 헤일로. cubic-bezier `(0.22, 1, 0.36, 1)`. |
| **flow 애니메이션** | 절차/플로우는 dash가 흐르는 SVG 화살표. `stroke-dashoffset` 키프레임 (다크 키트와 동일). |

---

## 2. 비주얼 시그니처

- 본문 배경: 옅은 회색 캔버스 `#F4F5F7` (PPT 배경 텍스처 평균톤의 웹 근사) — 글로우·메쉬 없음, 플랫
- 콘텐츠는 **흰색 페이퍼 카드**(`#FFFFFF` + 1px `#DEDEDE` 보더 + Standard 그림자) 위에만
- 큰 KPI 숫자는 **`co-navy` 솔리드 700** (다크 키트의 그라디언트 텍스트 대신 — PPT §2와 동일)
- 그라디언트 텍스트/패널은 **Hero Gradient**(navy→blue→cyan) 한 종만, 페이지당 1개·문서 전체 3개 이내
- 활성 사이드바 항목: 좌측 3px **네이비 막대** + cyan 글로우 + 우측 cyan 점등 도트
- 표: `#DEDEDE` 헤더 밴드 + zebra(`#FFFFFF`/`#FAFAFA`) + 하단 **So-What 네이비 바** (PPT §4.5 이식)
- BlockFlow / FlowDiagram의 dash 화살표 애니메이션은 다크 키트와 동일 (`stroke-dashoffset` 0.9s 무한)

---

## 3. 테크 스택

```
- Next.js 14 (App Router, RSC + Client Component 혼합)
- TypeScript 5 · React 18 · Tailwind CSS 3.4
- Pretendard 우선 폰트 스택
- Vercel zero-config 배포 · 순수 CSS 애니메이션 (framer-motion 불사용)
```

---

## 4. 컬러 토큰

### 4.1 회사 8색 (1차 컬러 소스 — PPT §1.1과 동일)

| Token | HEX | 라이트 테마에서의 역할 |
|---|---|---|
| `co-black` | `#000000` | 제목·강조 텍스트 (1차) |
| `co-dark-gray` | `#555555` | 본문·설명 텍스트 (2차) |
| `co-mid-gray` | `#A0A0A0` | eyebrow·캡션·메타·페이지번호 (3차/뮤트) — **본문에 사용 금지** |
| `co-light-gray` | `#DEDEDE` | 보더·디바이더·표 헤더 BG·게이지 트랙 |
| `co-mint` | `#7DEAD5` | 데코·성공 계열 원천 (텍스트는 §4.4 진한 단계 사용) |
| `co-cyan` | `#1BBBCC` | 활성 도트·글로우·밝은 액센트 |
| `co-blue` | `#4383AF` | 세컨더리 브랜드 |
| `co-navy` | `#06438C` | **Primary 브랜드** · KPI 숫자 · 강조 패널 BG · So-What 바 |

### 4.2 구조용 중립색 (표면 전용)

| 역할 | 값 | 용도 |
|---|---|---|
| 본문 캔버스 | `#F4F5F7` | body 배경 (플랫, 텍스처·메쉬 없음) |
| 콘텐츠 표면 | `#FFFFFF` | 카드·표 기본 행·사이드바 |
| 보조 표면 | `#FAFAFA` | 표 zebra 행·코드 블록·muted 카드 |
| hover 표면 | `#EEF0F3` | 사이드바·리스트 hover |
| 다크 표면(한정) | `co-navy → co-black` 그라디언트 | 표지/클로징성 히어로에만 선택적 (페이지당 0~1) |

### 4.3 Brand 시리즈 (다크 키트와 동일 HEX — 사용처만 반전)

`brand-400 = co-cyan`, `brand-500 = co-blue`, `brand-600 = co-navy` anchor는 동일. **흰 바탕에서는 텍스트 액센트로 600·700을, 배경 틴트로 50·100을 쓴다** (다크 키트의 200·300 텍스트 액센트는 흰 바탕에서 대비 부족 — §4.8 매핑 참조).

| Token | HEX | 라이트에서의 용도 |
|---|---|---|
| `brand-50` | `#E5F0F5` | 활성 항목·Callout·pill의 틴트 BG |
| `brand-100` | `#C7DCE7` | 옅은 보더·hover 틴트 |
| `brand-200` | `#BCE3EA` | 장식 한정 |
| `brand-300` | `#7CC9D5` | 장식·아이콘 한정 (텍스트 금지) |
| `brand-400` | `#1BBBCC` | **회사 cyan** — 활성 도트·글로우·데코 |
| `brand-500` | `#4383AF` | **회사 blue** — 보조 텍스트 액센트·보더 |
| `brand-600` | `#06438C` | **회사 navy** — 주 텍스트 액센트·KPI·강조 패널 |
| `brand-700` | `#052E62` | hover 진한 액센트 |
| `brand-800` | `#031F44` | active·최고 대비 텍스트 |
| `brand-900` | `#021530` | 다크 표면 anchor |

### 4.4 Mint(success) 단계 (emerald override — 다크 키트와 동일 HEX)

흰 바탕에서 성공/완료 텍스트는 **600·700**, 틴트 BG는 **100**을 쓴다.

| Token | HEX | 라이트 용도 |
|---|---|---|
| `emerald-100` | `#E5F8F2` | success Callout·배지 틴트 BG |
| `emerald-300` | `#7DEAD5` | 회사 mint — 데코·게이지 채움 |
| `emerald-500` | `#3DC4A7` | 보더·아이콘 |
| `emerald-600` | `#2BAA8D` | **success 텍스트 표준** |
| `emerald-700` | `#1F8F76` | success 텍스트 강조 |

### 4.5 색 사용 하드 룰 (PPT §1.3 이식)

- 위 토큰 외 색상 **금지**. 의미색(경고 amber·위험 rose) 토큰을 두지 않는다 — 다크 키트의 warn/danger variant는 본 킷에 **없다**. 경고·금지 뉘앙스는 **navy 솔리드 패널(emphasis) + Bold**로 처리한다.
- `co-mid-gray(#A0A0A0)`는 메타·캡션 전용. 문장 단위 본문에 쓰지 않는다(대비 부족).
- `co-mint`·`brand-300` 이하 밝은 단계는 흰 바탕에서 **텍스트 금지**(장식·차트·게이지 한정).

### 4.6 Elevation (그림자 — PPT §1.5 이식)

| 레벨 | Tailwind 토큰 | 값 | 사용처 |
|---|---|---|---|
| 0 — Flat | — | 없음 | 캔버스 위 일반 텍스트 |
| 1 — Standard | `shadow-card` | `0 4px 6px rgba(0,0,0,0.08)` | 표준 페이퍼 카드 |
| 2 — Ambient | `shadow-ambient` | `0 0 22.6px rgba(0,0,0,0.08)` | 부드러운 주변 확산 |
| 3 — Brand Glow | `shadow-glow` | `0 0 15px rgba(6,67,140,0.16)` | Featured 카드 (페이지당 1개) |
| 4 — Elevated | `shadow-elevated` | `0 12px 16px -4px rgba(6,67,140,0.10)` | 히어로 카드 |

> 그림자 알파는 흑색 0.08 또는 네이비 0.16을 넘기지 않는다.

### 4.7 Hero Gradient (PPT §1.4 이식)

```
linear-gradient(135deg, #06438C 0%, #4383AF 50%, #1BBBCC 100%)
```

- `.gradient-text` 및 그라디언트 패널의 유일한 정의. 각도·스톱 변형 금지.
- 허용 한도: **페이지당 1개 · 문서 전체 3개 이내.** 패널로 쓸 때 그 위 텍스트는 흰색만.
- 대부분의 강조는 그라디언트가 아니라 **`co-navy` 솔리드**로 처리한다.

### 4.8 다크 → 라이트 토큰 매핑 (기존 다크 덱 전환용)

| 다크 키트 (v1.3) | 라이트 키트 (본 문서) |
|---|---|
| body `#04060f` + 메쉬 그라디언트 | body `#F4F5F7` 플랫 |
| `.glass` (반투명+blur) | `.paper` (흰 BG + `#DEDEDE` 보더 + shadow-card) |
| `text-slate-50/100` (제목) | `text-black` (`co-black`) |
| `text-slate-200/300` (본문) | `text-[#555555]` (`co-dark-gray`) |
| `text-slate-400/500` (보조·메타) | `text-[#A0A0A0]` (`co-mid-gray`) |
| `text-brand-200/300` (액센트 텍스트) | `text-brand-600` / `text-brand-700` |
| `text-emerald-200/300` (성공 텍스트) | `text-emerald-600` / `text-emerald-700` |
| `bg-brand-500/15` 류 틴트 | `bg-brand-50` |
| KPI `.gradient-text` | KPI `text-brand-600 font-extrabold` (그라디언트는 Hero 한도 내) |
| Callout `warn(amber)`·`danger(rose)` | `emphasis`(navy 솔리드) 또는 `muted` 로 통합 |
| 사이드바 `bg-ink-900/80` | `bg-white/85` + `border-r #DEDEDE` |
| 활성 막대 `bg-brand-300` + 바이올렛 glow(잔재) | `bg-brand-600` + cyan glow `rgba(27,187,204,0.55)` |

---

## 5. 타이포그래피

폰트 스택·크기 스케일은 다크 키트 v1.3과 **동일**(본문 1.15× 확대 + 1pt 보정 반영). 색만 라이트 매핑.

```css
font-family: Pretendard, -apple-system, BlinkMacSystemFont, system-ui,
             "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
font-feature-settings: "tnum" 1, "ss01" 1;
```

| 위치 | 크기/굵기 | 색 |
|---|---|---|
| Hero 타이틀 | `text-4xl sm:text-6xl` / `font-extrabold` / `tracking-tight` / `leading-[1.05]` | `co-black` |
| Hero 인트로 한 줄 | `text-base sm:text-lg` / `leading-relaxed` | `#555555` |
| 슬라이드 H2 | `text-2xl sm:text-4xl` / `font-bold` / `tracking-tight` | `co-black` |
| 슬라이드 한 줄 설명 | `text-sm sm:text-[15px]` / `leading-relaxed` | `#555555` |
| 카드 제목 | `text-[15px]` / `font-semibold` | `co-black` |
| 카드 본문 | `text-[13.5px]` / `leading-relaxed` | `#555555` |
| 본문 단락(일반) | `text-[13px–15px]` / `leading-relaxed` | `#555555` |
| Section 라벨(eyebrow) | `text-[12px]` / `uppercase` / `tracking-[0.18em]` / `font-semibold` | `brand-600` |
| 사이드바 그룹 라벨 | `text-[11px]` / `uppercase` / `tracking-[0.18em]` / `font-semibold` | `#A0A0A0` |
| 사이드바 라벨 | `text-[15px] sm:text-base` / `font-medium`, 활성 시 `font-semibold` | `#555555` → 활성 `brand-800` |
| 사이드바 번호 prefix | `text-[12px]` / `font-mono` / `font-semibold` / `tabular-nums` | `#A0A0A0` → 활성 `brand-600` |
| KPI 숫자 | `text-3xl~4xl` / `font-extrabold` | `brand-600` |
| 모노 / 코드 인라인 | `font-mono` / `text-[12–13.5px]` | `brand-700` |
| 모노 / 코드 블록(pre) | `text-[11.5–12.5px]` / `leading-relaxed` | `#333333` on `#FAFAFA` |
| 표 본문 | `text-[14px]` / padding `py-2.5 px-3.5` | `#555555` (1열은 `co-black` medium) |
| 표 thead | `text-[12px]` / `uppercase` / `tracking-wider` / `font-bold` | `co-black` on `#DEDEDE` |
| So-What 바 | `text-[13px]` / `font-bold` | `#FFFFFF` on `brand-600` |
| FlowDiagram 제목/본문 | `1.04rem` / `0.94rem` | `co-black` / `#555555` |
| BlockFlow 제목/보조/번호 | `0.92rem` / `0.76rem` / `0.66rem` | `co-black` / `#A0A0A0` / `brand-500` |
| Tag pill | `0.78rem` | variant별 (§7.3) |

헤더 식별 영역(슬라이드 번호 배지·eyebrow·H2·한 줄 설명·Hero 상단)은 다크 키트 §5.1과 동일하게 +1pt 보정 제외.

그라디언트 텍스트 (단일 정의 — §4.7):
```css
.gradient-text {
  background: linear-gradient(135deg, #06438C 0%, #4383AF 50%, #1BBBCC 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

---

## 6. 컴포넌트 카탈로그

| # | 이름 | 역할 |
|---|---|---|
| C1 | `HomeShell` | 사이드바 + 본문 SPA 컨테이너, activeId 상태, URL 해시·키보드 네비 (다크 키트와 로직 동일) |
| C2 | `Sidebar` | 좌측 고정 메뉴 — 정확 명세 §6.2 |
| C3 | `SlideShell` | 슬라이드 헤더(번호 배지·eyebrow·타이틀·설명) + 본문 + 진입 애니메이션 |
| C4 | `Card` / `CardGrid` | 페이퍼 카드 + 액센트 틴트 + 호버 리프트 |
| C5 | `Callout` | 4 variants (**info / success / muted / emphasis**) — warn·danger 없음(§4.5) |
| C6 | `BlockFlow` | 가로 블록 + 화살표 플로우 (모바일 세로 자동 전환) |
| C7 | `FlowDiagram` | 번호 카드 + 세로 화살표 (dash flow) |
| C8 | `DataTable` + `SoWhat` | `#DEDEDE` thead + zebra + **네이비 So-What 결론 바** (PPT §4.5 이식) |
| C9 | `Kpi` / `KpiGrid` | 네이비 큰 숫자 + 페이퍼 카드 |
| C10 | `Roadmap`/`Phase` | 활성 단계 네이비 틴트 강조 |
| C11 | `Tag`/`Pill` | 컬러 variants 작은 라운드 |
| C12 | `Faq` (Accordion) | Q번호 prefix + `+` 45° 회전 |

### 6.2 Sidebar 정확 명세 (라이트 표준 v1.0)

다크 키트 §6.2의 좌표·간격·크기는 **전부 동일**. 색만 아래로 교체.

| 영역 | 속성 | 값 |
|---|---|---|
| 컨테이너 | 너비/패딩 | `w-[280px]` · `px-4 py-6` (동일) |
| | 배경 | `bg-white/85 backdrop-blur-xl` |
| | 우측 보더 | `1px #DEDEDE` |
| 로고 | 마크 | 36×36, 라운드 12px, **navy→cyan 그라디언트** (동일) |
| | 텍스트 / 서브 | `co-black` 700 / `brand-600` |
| 그룹 라벨 | 폰트 | 11px uppercase `tracking-[0.18em]` 600 `#A0A0A0` |
| 항목 | 라벨 / 번호 | 15–16px `#555555` / 12px mono `#A0A0A0` |
| | hover | `bg-[#EEF0F3] text-black` |
| 활성 | 배경 | `bg-gradient-to-r from-brand-50 via-brand-50/50 to-transparent` |
| | ring | `ring-1 ring-brand-500/25` |
| | 라벨/번호 | `text-brand-800 font-semibold` / `text-brand-600` |
| | 좌측 막대 | 24×3px `bg-brand-600` + glow `0 0 10px 2px rgba(27,187,204,0.55)` |
| | 우측 도트 | 6×6px `bg-brand-400` + glow `0 0 8px 2px rgba(27,187,204,0.55)` |
| 부록 활성 | 배경 | `bg-[#EFF0F2] ring-1 ring-[#D5D7DA]` (브랜드 톤 X, 막대 X) |
| 모바일 토글 | 버튼 | `bg-brand-600 text-white shadow-glow` (우하단 고정) |

모바일 동작(lg 미만 숨김·백드롭·sticky)은 다크 키트와 동일. 백드롭만 `bg-black/30 backdrop-blur-sm`.

---

## 7. 전체 코드 (복붙 가능)

### 7.1 `tailwind.config.ts`

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{js,ts,jsx,tsx,mdx}", "./components/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      fontFamily: {
        sans: [
          "Pretendard", "-apple-system", "BlinkMacSystemFont", "system-ui",
          "Segoe UI", "Apple SD Gothic Neo", "Noto Sans KR", "sans-serif",
        ],
      },
      colors: {
        brand: {
          50:"#E5F0F5",100:"#C7DCE7",200:"#BCE3EA",300:"#7CC9D5",
          400:"#1BBBCC",500:"#4383AF",600:"#06438C",700:"#052E62",
          800:"#031F44",900:"#021530",
        },
        emerald: {
          100:"#E5F8F2",200:"#C9F1E5",300:"#7DEAD5",400:"#5DD7BE",
          500:"#3DC4A7",600:"#2BAA8D",700:"#1F8F76",800:"#16735F",900:"#0E5847",
        },
        surface: { 0:"#FFFFFF", 50:"#FAFAFA", 100:"#F4F5F7", 200:"#EEF0F3" },
        co: {
          black:"#000000", dark:"#555555", mid:"#A0A0A0", light:"#DEDEDE",
          mint:"#7DEAD5", cyan:"#1BBBCC", blue:"#4383AF", navy:"#06438C",
        },
      },
      boxShadow: {
        card: "0 4px 6px rgba(0,0,0,0.08)",
        ambient: "0 0 22.6px rgba(0,0,0,0.08)",
        glow: "0 0 15px rgba(6,67,140,0.16)",
        elevated: "0 12px 16px -4px rgba(6,67,140,0.10)",
        "glow-cyan": "0 0 12px rgba(27,187,204,0.4)",
      },
      animation: {
        slideIn: "slideIn 0.45s cubic-bezier(0.22,1,0.36,1)",
        fadeIn: "fadeIn 0.35s ease-out",
      },
      keyframes: {
        slideIn: {
          "0%": { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        fadeIn: { "0%": { opacity: "0" }, "100%": { opacity: "1" } },
      },
    },
  },
  plugins: [],
};
export default config;
```

### 7.2 `app/layout.tsx`

```tsx
import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Your App",
  description: "Modern light slide-style document UI.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  themeColor: "#F4F5F7",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body className="bg-surface-100 text-black antialiased">{children}</body>
    </html>
  );
}
```

### 7.3 `app/globals.css` (디자인의 핵심)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

:root { color-scheme: light; }
html { scroll-behavior: smooth; }

body {
  font-feature-settings: "tnum" 1, "ss01" 1;
  background-color: #F4F5F7;   /* 플랫 캔버스 — 메쉬/글로우 없음 */
  min-height: 100vh;
  color: #111111;
}

.gradient-text {
  background: linear-gradient(135deg, #06438C 0%, #4383AF 50%, #1BBBCC 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* 다크 키트의 .glass 대응 — 라이트 페이퍼 카드 */
.paper {
  background: #FFFFFF;
  border: 1px solid #DEDEDE;
  box-shadow: 0 4px 6px rgba(0,0,0,0.08);
}

.dot-bg {
  background-image: radial-gradient(rgba(85,85,85,0.07) 1px, transparent 1px);
  background-size: 18px 18px;
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(85,85,85,0.22); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: rgba(85,85,85,0.34); }

/* === FlowDiagram (vertical) === */
.flow-card {
  display:flex; gap:1rem; padding:1rem 1.15rem; border-radius:1rem;
  background: #FFFFFF;
  border: 1px solid #DEDEDE;
  box-shadow: 0 4px 6px rgba(0,0,0,0.06);
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.flow-card:hover {
  transform: translateY(-1px);
  border-color: rgba(67,131,175,0.55);
  box-shadow: 0 6px 22px rgba(6,67,140,0.12);
}
.flow-number {
  flex:0 0 auto; width:2.4rem; height:2.4rem; border-radius:9999px;
  background: linear-gradient(135deg,#06438C,#1BBBCC);
  color:white; display:grid; place-items:center;
  font-weight:700; font-size:0.92rem;
  box-shadow: 0 4px 14px rgba(6,67,140,0.30);
}
.flow-content { flex:1 1 auto; min-width:0; }
.flow-title { font-weight:600; color:#000000; font-size:1.04rem; }
.flow-body  { margin-top:0.45rem; font-size:0.94rem; line-height:1.65; color:#555555; }
.flow-arrow { display:grid; place-items:center; color:#A0A0A0; }
.flow-line-anim { stroke-dasharray:4 4; animation: dashFlow 0.9s linear infinite; }
@keyframes dashFlow { to { stroke-dashoffset:-8; } }

/* === BlockFlow (horizontal on sm+, vertical on mobile) === */
.block-flow-card {
  position:relative; padding:0.75rem 0.95rem; border-radius:0.85rem;
  background: #FFFFFF;
  border: 1px solid rgba(6,67,140,0.25);
  box-shadow: 0 2px 5px rgba(0,0,0,0.05);
  display:flex; flex-direction:column; gap:0.1rem;
  transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
}
.block-flow-card:hover {
  transform: translateY(-2px);
  border-color: rgba(27,187,204,0.6);
  box-shadow: 0 10px 24px rgba(27,187,204,0.16);
}
.block-flow-card .num   { font-size:0.66rem; font-family: ui-monospace,monospace; color:#4383AF; letter-spacing:0.04em; line-height:1.1; }
.block-flow-card .title { font-weight:600; font-size:0.92rem; color:#000000; line-height:1.25; word-break:keep-all; }
.block-flow-card .sub   { font-size:0.76rem; color:#A0A0A0; margin-top:0.1rem; line-height:1.3; word-break:keep-all; }
.flow-line-anim-h { stroke-dasharray:4 4; animation: dashFlowH 0.9s linear infinite; }
@keyframes dashFlowH { to { stroke-dashoffset:-8; } }

/* === 슬라이드 진입 === */
.slide-enter { animation: slideEnter 0.4s cubic-bezier(0.22,1,0.36,1); }
@keyframes slideEnter {
  from { opacity:0; transform: translateY(14px); }
  to   { opacity:1; transform: translateY(0); }
}

/* === 부록 / 섹션 디바이더 === */
.appendix-bg { background: linear-gradient(180deg, rgba(85,85,85,0.05), transparent 30%); }
.appendix-divider {
  position:relative; margin:0 0 1rem; text-align:center;
  font-size:0.65rem; letter-spacing:0.22em; text-transform:uppercase; color:#A0A0A0;
}
.appendix-divider::before, .appendix-divider::after {
  content:""; position:absolute; top:50%; width:38%; height:1px;
  background: linear-gradient(to right, transparent, #DEDEDE, transparent);
}
.appendix-divider::before { left:0; } .appendix-divider::after { right:0; }

/* === 코드블록 === */
.code-block {
  background: #FAFAFA;
  border: 1px solid #DEDEDE;
  color: #333333;
  border-radius: 0.75rem;
  padding: 1rem 1.1rem;
  font-size: 0.84rem; line-height: 1.7;
  overflow-x: auto;
}

/* === So-What 바 (PPT §4.5 이식) === */
.sowhat {
  border-radius: 0.6rem;
  background: #06438C;
  color: #FFFFFF;
  font-weight: 700; font-size: 0.82rem;
  padding: 0.65rem 1rem;
}

/* === Tag / Pill === */
.tag {
  display:inline-flex; align-items:center; gap:0.35rem;
  padding:0.2rem 0.6rem; border-radius:999px; font-size:0.78rem; font-weight:500;
  background: rgba(27,187,204,0.10); color:#052E62; border:1px solid rgba(27,187,204,0.35);
}
.tag-muted { background:#FAFAFA; color:#555555; border-color:#DEDEDE; }
.tag-navy  { background: rgba(6,67,140,0.08); color:#06438C; border-color: rgba(6,67,140,0.25); }

@media print {
  .no-print { display:none !important; }
  .flow-line-anim, .flow-line-anim-h { animation:none; }
}
```

### 7.4 `app/HomeShell.tsx` — SPA 본체 (다크 키트와 로직 동일, 페이지네이션만 라이트)

```tsx
"use client";

import { useEffect, useRef, useState } from "react";
import Sidebar from "@/app/components/Sidebar";
import { slides, defaultSlideId, slideIds } from "@/app/slides";

export default function HomeShell() {
  const [activeId, setActiveId] = useState<string>(defaultSlideId);
  const mainRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const sync = () => {
      const h = window.location.hash.replace("#", "");
      if (h && slideIds.includes(h)) setActiveId(h);
    };
    sync();
    window.addEventListener("hashchange", sync);
    window.addEventListener("popstate", sync);
    return () => {
      window.removeEventListener("hashchange", sync);
      window.removeEventListener("popstate", sync);
    };
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") return;
    if (window.location.hash !== `#${activeId}`) {
      try { history.replaceState(null, "", `#${activeId}`); } catch {}
    }
    requestAnimationFrame(() => {
      window.scrollTo({ top: 0 });
      mainRef.current?.scrollTo?.({ top: 0 });
    });
  }, [activeId]);

  useEffect(() => {
    if (typeof window === "undefined") return;
    const onKey = (e: KeyboardEvent) => {
      const t = e.target as HTMLElement | null;
      if (t && (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable)) return;
      const idx = slideIds.indexOf(activeId);
      if (idx === -1) return;
      if (e.key === "ArrowRight" || e.key === "PageDown") {
        const next = slideIds[Math.min(idx + 1, slideIds.length - 1)];
        if (next !== activeId) setActiveId(next);
      } else if (e.key === "ArrowLeft" || e.key === "PageUp") {
        const prev = slideIds[Math.max(idx - 1, 0)];
        if (prev !== activeId) setActiveId(prev);
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [activeId]);

  const Slide = slides[activeId] ?? slides[defaultSlideId];
  const idx = slideIds.indexOf(activeId);
  const total = slideIds.length;

  return (
    <div className="min-h-screen flex">
      <Sidebar activeId={activeId} onSelect={setActiveId} />
      <main ref={mainRef} className="flex-1 min-w-0 relative">
        <div key={activeId} className="max-w-[82rem] mx-auto"><Slide /></div>

        <div className="no-print fixed bottom-5 left-1/2 -translate-x-1/2 lg:left-auto lg:right-6 lg:translate-x-0 z-30 flex items-center gap-2 rounded-full bg-white/90 backdrop-blur ring-1 ring-[#DEDEDE] shadow-card px-3 py-1.5 text-[11px] text-[#555555]">
          <button disabled={idx<=0} onClick={()=>setActiveId(slideIds[Math.max(idx-1,0)])}
            className="px-1.5 py-0.5 rounded hover:bg-surface-200 disabled:opacity-30 disabled:cursor-not-allowed">←</button>
          <span className="font-mono tabular-nums">
            {String(idx + 1).padStart(2, "0")} / {String(total).padStart(2, "0")}
          </span>
          <button disabled={idx>=total-1} onClick={()=>setActiveId(slideIds[Math.min(idx+1,total-1)])}
            className="px-1.5 py-0.5 rounded hover:bg-surface-200 disabled:opacity-30 disabled:cursor-not-allowed">→</button>
        </div>
      </main>
    </div>
  );
}
```

### 7.5 `app/data/nav.ts` (다크 키트와 동일)

```ts
export type NavItem = {
  id: string;
  label: string;
  number?: string;
  group?: string;
  appendix?: boolean;
};

export const navItems: NavItem[] = [
  { id: "overview", label: "개요", number: "01" },
  // ... group으로 묶음 가능, appendix:true는 부록 톤.
];
```

### 7.6 `app/components/Sidebar.tsx`

```tsx
"use client";
import { useEffect, useState } from "react";
import { navItems } from "@/app/data/nav";

type Props = { activeId: string; onSelect: (id: string) => void; };

export default function Sidebar({ activeId, onSelect }: Props) {
  const [mobileOpen, setMobileOpen] = useState(false);
  useEffect(() => { setMobileOpen(false); }, [activeId]);

  const groups: { name?: string; items: typeof navItems }[] = [];
  navItems.forEach((it) => {
    const last = groups[groups.length - 1];
    if (last && last.name === it.group) last.items.push(it);
    else groups.push({ name: it.group, items: [it] });
  });

  return (
    <>
      <button type="button" onClick={() => setMobileOpen(v => !v)}
        className="no-print fixed bottom-5 right-5 z-50 lg:hidden rounded-full bg-brand-600 hover:bg-brand-700 text-white shadow-glow px-5 py-3 text-sm font-semibold active:scale-95 transition"
        aria-label="목차 열기">
        {mobileOpen ? "닫기 ✕" : "목차 ☰"}
      </button>
      {mobileOpen && (
        <div className="no-print fixed inset-0 z-30 bg-black/30 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileOpen(false)} />
      )}
      <aside className={`no-print fixed lg:sticky top-0 left-0 z-40 h-screen w-[280px] shrink-0 border-r border-[#DEDEDE] bg-white/85 backdrop-blur-xl transition-transform duration-200 ${mobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}`}>
        <div className="h-full overflow-y-auto px-4 py-6">
          <button type="button" onClick={() => onSelect("overview")}
            className="w-full flex items-center gap-2.5 mb-7 px-2">
            <span className="relative inline-block">
              <span className="absolute inset-0 rounded-xl bg-brand-500 blur-md opacity-30" />
              <span className="relative inline-block h-9 w-9 rounded-xl bg-gradient-to-br from-brand-400 to-brand-700 ring-1 ring-black/10" />
            </span>
            <span className="text-left">
              <span className="block font-bold tracking-tight text-black text-[15px]">YourApp</span>
              <span className="block text-xs text-brand-600 font-medium tracking-wide">Subtitle · v1.0</span>
            </span>
          </button>
          <nav className="space-y-5">
            {groups.map((g, gi) => (
              <div key={gi}>
                {g.name && (
                  <p className="px-2 mb-1.5 text-[11px] uppercase tracking-[0.18em] font-semibold text-[#A0A0A0]">{g.name}</p>
                )}
                <ul className="space-y-1">
                  {g.items.map((n) => {
                    const isActive = activeId === n.id;
                    const isAppendix = n.appendix;
                    return (
                      <li key={n.id}>
                        <button type="button" onClick={() => onSelect(n.id)}
                          className={`group w-full flex items-center gap-3 rounded-lg px-2.5 py-2.5 text-base transition relative ${
                            isActive
                              ? isAppendix
                                ? "bg-[#EFF0F2] text-black font-semibold ring-1 ring-[#D5D7DA]"
                                : "bg-gradient-to-r from-brand-50 via-brand-50/50 to-transparent text-brand-800 font-semibold ring-1 ring-brand-500/25"
                              : "text-[#555555] hover:bg-surface-200 hover:text-black"
                          }`}>
                          {isActive && !isAppendix && (
                            <span className="absolute left-0 top-1/2 -translate-y-1/2 h-6 w-[3px] rounded-r-full bg-brand-600 shadow-[0_0_10px_2px_rgba(27,187,204,0.55)]" />
                          )}
                          <span className={`text-[12px] font-mono font-semibold tabular-nums ${
                            isActive ? (isAppendix ? "text-[#555555]" : "text-brand-600")
                                     : "text-[#A0A0A0] group-hover:text-[#555555]"
                          }`}>{n.number}</span>
                          <span className="flex-1 text-left text-[15px] sm:text-base leading-tight">{n.label}</span>
                          {isActive && !isAppendix && (
                            <span className="h-1.5 w-1.5 rounded-full bg-brand-400 shadow-[0_0_8px_2px_rgba(27,187,204,0.55)]" />
                          )}
                        </button>
                      </li>
                    );
                  })}
                </ul>
              </div>
            ))}
          </nav>
        </div>
      </aside>
    </>
  );
}
```

### 7.7 `app/components/SlideShell.tsx`

```tsx
import type { ReactNode } from "react";

type Props = {
  number?: string;
  eyebrow?: string;
  title: string;
  description?: string;
  children: ReactNode;
  variant?: "default" | "appendix";
};

export default function SlideShell({ number, eyebrow, title, description, children, variant = "default" }: Props) {
  const isAppendix = variant === "appendix";
  return (
    <article className={`relative slide-enter min-h-screen ${isAppendix ? "appendix-bg" : ""}`}>
      <div className="px-6 sm:px-10 lg:px-14 pt-10 sm:pt-14 pb-4">
        <div className="flex items-center gap-2.5 mb-3">
          {number && (
            <span className={`inline-flex items-center justify-center h-7 min-w-[28px] px-2 rounded-md text-[11px] font-mono font-semibold ${
              isAppendix ? "bg-[#EFF0F2] text-[#555555] ring-1 ring-[#D5D7DA]"
                         : "bg-brand-50 text-brand-700 ring-1 ring-brand-500/25"
            }`}>{number}</span>
          )}
          {eyebrow && (
            <span className={`text-[11px] font-semibold uppercase tracking-[0.18em] ${isAppendix ? "text-[#A0A0A0]" : "text-brand-600"}`}>
              {eyebrow}
            </span>
          )}
        </div>
        <h2 className="text-2xl sm:text-4xl font-bold tracking-tight text-black leading-tight">{title}</h2>
        {description && (
          <p className="mt-3 text-sm sm:text-[15px] text-[#555555] leading-relaxed">{description}</p>
        )}
      </div>
      <div className="px-6 sm:px-10 lg:px-14 pb-16 space-y-5">{children}</div>
    </article>
  );
}
```

### 7.8 `app/components/Card.tsx`

```tsx
import type { ReactNode } from "react";

export function CardGrid({ cols = 2, children }: { cols?: 2|3|4; children: ReactNode }) {
  const grid = cols===4 ? "sm:grid-cols-2 lg:grid-cols-4" : cols===3 ? "sm:grid-cols-2 lg:grid-cols-3" : "sm:grid-cols-2";
  return <div className={`grid grid-cols-1 ${grid} gap-3.5`}>{children}</div>;
}

export function Card({ title, badge, icon, accent, children }: {
  title: string; badge?: string; icon?: ReactNode;
  accent?: "brand"|"mint"|"navy"|"slate"; children: ReactNode;
}) {
  const accentColor =
    accent==="mint" ? "from-emerald-100" :
    accent==="navy" ? "from-brand-100/70" :
    accent==="slate" ? "from-surface-200" : "from-brand-50";
  return (
    <div className="group relative rounded-2xl paper p-4 sm:p-5 transition hover:-translate-y-0.5 hover:border-brand-500/50 hover:shadow-glow">
      <div className={`pointer-events-none absolute inset-0 rounded-2xl bg-gradient-to-br ${accentColor} via-transparent to-transparent opacity-60`} />
      <div className="relative">
        <div className="flex items-center gap-2 mb-1.5">
          {icon && <span className="text-base text-brand-600">{icon}</span>}
          <h3 className="font-semibold text-black text-[15px] flex-1">{title}</h3>
          {badge && (
            <span className="text-[10px] font-medium px-1.5 py-0.5 rounded-md bg-brand-50 text-brand-700 ring-1 ring-brand-500/25">
              {badge}
            </span>
          )}
        </div>
        <div className="text-[13.5px] leading-relaxed text-[#555555]">{children}</div>
      </div>
    </div>
  );
}
```

### 7.9 `app/components/Callout.tsx` — 4 variants (warn·danger 없음)

```tsx
import type { ReactNode } from "react";

type Variant = "info" | "success" | "muted" | "emphasis";
const styles: Record<Variant,string> = {
  info:     "bg-brand-50 border-brand-500/30 text-[#333333]",
  success:  "bg-emerald-100 border-emerald-500/40 text-[#333333]",
  muted:    "bg-surface-50 border-[#DEDEDE] text-[#555555]",
  emphasis: "bg-brand-600 border-transparent text-white",   // PPT Featured 패널 이식
};
const titleColor: Record<Variant,string> = {
  info: "text-brand-800", success: "text-emerald-700", muted: "text-black", emphasis: "text-white",
};
const icons: Record<Variant,string> = { info:"ℹ", success:"✓", muted:"·", emphasis:"◆" };

export default function Callout({ variant="info", title, children }:
  { variant?: Variant; title?: string; children: ReactNode }) {
  return (
    <div className={`rounded-xl border p-3.5 sm:p-4 shadow-card ${styles[variant]}`}>
      {title && (
        <p className={`font-semibold mb-1 flex items-center gap-2 text-[14px] ${titleColor[variant]}`}>
          <span aria-hidden className="opacity-80">{icons[variant]}</span>
          <span>{title}</span>
        </p>
      )}
      <div className="text-[13.5px] leading-relaxed">{children}</div>
    </div>
  );
}
```

### 7.10 `app/components/BlockFlow.tsx` (구조 동일 — 다크 키트 §7.10과 같은 코드, 스타일은 globals.css)

```tsx
import { Fragment } from "react";
import type { ReactNode } from "react";

export type BlockFlowItem = { num?: string; title: string; sub?: string; icon?: ReactNode };

export default function BlockFlow({ items, compact=false }:
  { items: BlockFlowItem[]; compact?: boolean }) {
  return (
    <div className="w-full">
      <div className="flex flex-col sm:flex-row items-stretch gap-1.5 sm:gap-0">
        {items.map((it, i) => (
          <Fragment key={i}>
            <div className={`block-flow-card sm:flex-[4] sm:min-w-0 ${compact ? "py-2" : ""}`}>
              {it.num && <span className="num">STEP {it.num}</span>}
              <div className="flex items-center gap-1.5 min-w-0">
                {it.icon && <span className="text-base text-brand-600 shrink-0" aria-hidden>{it.icon}</span>}
                <span className="title">{it.title}</span>
              </div>
              {it.sub && <p className="sub">{it.sub}</p>}
            </div>
            {i < items.length - 1 && <Connector />}
          </Fragment>
        ))}
      </div>
    </div>
  );
}

function Connector() {
  return (
    <>
      <svg width="18" height="20" viewBox="0 0 18 20" className="sm:hidden mx-auto text-[#A0A0A0]" aria-hidden>
        <line x1="9" y1="0" x2="9" y2="12" stroke="currentColor" strokeWidth="2" className="flow-line-anim" />
        <polygon points="9,19 3,11 15,11" fill="currentColor" />
      </svg>
      <div className="hidden sm:flex sm:flex-[1] sm:min-w-[24px] items-center self-center text-[#A0A0A0]" aria-hidden>
        <svg viewBox="0 0 100 14" preserveAspectRatio="none" className="flex-1 h-3.5 min-w-0">
          <line x1="0" y1="7" x2="100" y2="7" stroke="currentColor" strokeWidth="2"
            vectorEffect="non-scaling-stroke" className="flow-line-anim-h" />
        </svg>
        <svg width="11" height="14" viewBox="0 0 11 14" className="shrink-0" aria-hidden>
          <polygon points="11,7 0,1 0,13" fill="currentColor" />
        </svg>
      </div>
    </>
  );
}
```

### 7.11 `app/components/FlowDiagram.tsx` (다크 키트 §7.11과 동일 코드)

```tsx
import type { ReactNode } from "react";

export type FlowStep = { title: string; body?: ReactNode };

export default function FlowDiagram({ steps, compact=false }:
  { steps: FlowStep[]; compact?: boolean }) {
  return (
    <ol className="list-none p-0 m-0 space-y-0">
      {steps.map((s, i) => (
        <li key={i}>
          <div className={`flow-card ${compact ? "py-2.5 px-3.5" : ""}`}>
            <div className="flow-number">{i + 1}</div>
            <div className="flow-content">
              <p className="flow-title">{s.title}</p>
              {s.body && <div className="flow-body">{s.body}</div>}
            </div>
          </div>
          {i < steps.length - 1 && <Arrow />}
        </li>
      ))}
    </ol>
  );
}
function Arrow() {
  return (
    <div className="flow-arrow py-0.5" aria-hidden>
      <svg width="20" height="32" viewBox="0 0 20 32" className="block mx-auto">
        <line x1="10" y1="0" x2="10" y2="22" stroke="currentColor" strokeWidth="2" className="flow-line-anim" />
        <polygon points="10,31 4,21 16,21" fill="currentColor" />
      </svg>
    </div>
  );
}
```

### 7.12 `app/components/DataTable.tsx` + So-What 바 (PPT §4.5 이식)

```tsx
import type { ReactNode } from "react";

export default function DataTable({ head, rows, emphasizeCol }: {
  head: ReactNode[]; rows: ReactNode[][]; emphasizeCol?: number;   // To-Be 열 인덱스 등
}) {
  return (
    <div className="overflow-x-auto rounded-xl paper">
      <table className="w-full border-collapse text-[14px]">
        <thead>
          <tr className="bg-[#DEDEDE]">
            {head.map((h, i) => (
              <th key={i} className={`text-left py-2.5 px-3.5 text-[12px] uppercase tracking-wider font-bold whitespace-nowrap ${
                i === emphasizeCol ? "text-brand-600" : "text-black"
              }`}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((r, ri) => (
            <tr key={ri} className={`border-b border-[#DEDEDE]/70 last:border-0 transition hover:bg-brand-50/60 ${
              ri % 2 === 1 ? "bg-surface-50" : "bg-white"
            }`}>
              {r.map((c, ci) => (
                <td key={ci} className={`py-2.5 px-3.5 align-top ${
                  ci === 0 ? "text-black font-medium"
                  : ci === emphasizeCol ? "text-brand-700 font-semibold"
                  : "text-[#555555]"
                }`}>{c}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/** 표·차트 아래 한 줄 결론 — PPT So-What 바 */
export function SoWhat({ children }: { children: ReactNode }) {
  return <p className="sowhat">{children}</p>;
}
```

### 7.13 `app/components/Kpi.tsx` — 네이비 KPI (그라디언트 텍스트 미사용)

```tsx
import type { ReactNode } from "react";

export function KpiGrid({ cols = 4, children }: { cols?: 2|3|4; children: ReactNode }) {
  const grid = cols===4 ? "grid-cols-2 lg:grid-cols-4" : cols===3 ? "grid-cols-1 sm:grid-cols-3" : "grid-cols-2";
  return <div className={`grid ${grid} gap-3`}>{children}</div>;
}

export function Kpi({ value, suffix, label, sub }:
  { value: string; suffix?: string; label: string; sub?: string }) {
  return (
    <div className="rounded-2xl paper p-4 sm:p-5 text-center relative overflow-hidden">
      <div className="absolute -top-10 -right-10 h-28 w-28 rounded-full bg-brand-600/10 blur-2xl" />
      <p className="relative text-3xl sm:text-4xl font-extrabold text-brand-600 leading-none">
        {value}{suffix && <span className="text-lg text-[#A0A0A0] ml-1 font-bold">{suffix}</span>}
      </p>
      <p className="relative mt-2 text-[12px] text-[#555555] font-medium">{label}</p>
      {sub && <p className="relative mt-0.5 text-[11px] text-[#A0A0A0]">{sub}</p>}
    </div>
  );
}
```

### 7.14 슬라이드 등록 패턴 · `app/page.tsx` (다크 키트 §7.12·7.14와 동일)

```tsx
// app/slides/index.tsx
import type { ComponentType } from "react";
import Overview from "./Overview";

export const slides: Record<string, ComponentType> = { overview: Overview };
export const slideIds = Object.keys(slides);
export const defaultSlideId = "overview";

// app/page.tsx
import HomeShell from "@/app/HomeShell";
export default function HomePage() { return <HomeShell />; }
```

### 7.15 Hero(Overview) 예시 — 라이트

```tsx
import BlockFlow from "@/app/components/BlockFlow";

export default function Overview() {
  return (
    <article className="slide-enter min-h-screen">
      <div className="px-6 sm:px-10 lg:px-14 pt-12 sm:pt-20 pb-12">
        <div className="inline-flex items-center gap-2 rounded-full border border-brand-500/25 bg-brand-50 px-3 py-1 text-[11px] font-semibold text-brand-700">
          <span className="inline-block h-1.5 w-1.5 rounded-full bg-brand-400 animate-pulse" />
          v1.0 · Internal
        </div>
        <h1 className="mt-5 text-4xl sm:text-6xl font-extrabold tracking-tight leading-[1.05] text-black">
          Project <span className="gradient-text">Title</span>
          <br />Subtitle
        </h1>
        <p className="mt-5 max-w-2xl text-base sm:text-lg text-[#555555] leading-relaxed">
          Hero 설명 문장.
        </p>
        <BlockFlow items={[
          { num:"01", title:"Step A", sub:"한줄 설명" },
          { num:"02", title:"Step B" },
          { num:"03", title:"Step C" },
        ]} compact />
      </div>
    </article>
  );
}
```

> **Hero 배경 정책**: 다크 키트 v1.1+와 동일 — 첫 페이지에 별도 글로우·패턴 오버레이를 두지 않는다. `gradient-text`(Hero 한도 1회)와 페이퍼 카드로만 강조.

### 7.16 CTA 버튼 3단계 (다크 키트 §7.15 위계 이식)

| 강조 단계 | 스타일 | 용도 |
|---|---|---|
| **L1 — Primary** | `bg-brand-600 hover:bg-brand-700 text-white shadow-glow` | 페이지의 단 하나의 최상위 액션 |
| **L2 — Emphasized** | `bg-brand-50 hover:bg-brand-100 text-brand-700 font-semibold ring-2 ring-brand-500/40 hover:ring-brand-500/70 hover:-translate-y-0.5 shadow-card transition-all` | 잘 보여야 하는 보조 액션 (1~2개) |
| **L3 — Ghost** | `bg-transparent hover:bg-brand-50 ring-1 ring-brand-500/30 text-brand-600` | 페이지 내 보조 링크 |

> 위계 룰: 한 슬라이드 안에 L1은 1개, L2는 1~2개까지 (다크 키트와 동일).

---

## 8. 인터랙션 명세

| 요소 | 상태 | 스타일 |
|---|---|---|
| 사이드바 항목 | Default | `text-[#555555]` |
| | Hover | `bg-surface-200 text-black` |
| | Active | brand-50 그라디언트 BG + ring-brand-500/25 + 좌측 navy 막대(cyan glow) + 우측 cyan 도트 |
| Card | Hover | `-translate-y-0.5` + `border-brand-500/50` + `shadow-glow` |
| 버튼 | 모바일 토글 | `active:scale-95` + `shadow-glow` |
| 슬라이드 진입 | — | `key={activeId}` 리마운트 → `slide-enter` 0.4s 페이드+업 |
| dash flow | — | `stroke-dasharray 4 4` · 0.9s linear infinite (다크 키트와 동일) |
| 키보드 / URL 해시 | — | 다크 키트 §8.6–8.7과 동일 (←/→, `history.replaceState`) |

---

## 9. 반응형 브레이크포인트 (다크 키트와 동일)

| 폭 | 동작 |
|---|---|
| < 640px | 사이드바 숨김(우하단 토글), BlockFlow 세로, CardGrid 1열 |
| ≥ 640px (sm) | BlockFlow 가로, CardGrid 2열 |
| ≥ 1024px (lg) | 사이드바 sticky 노출, CardGrid 3/4열 |
| 본문 max | `max-w-[82rem]`, 좌우 `px-6 sm:px-10 lg:px-14` |
| 사이드바 | `w-[280px]` 고정 |

---

## 10. 디자인 적용 체크리스트

1. Next.js 14 App Router + Tailwind 3.4, §7.1 config·§7.3 globals 그대로.
2. `<html>`에 `dark` 클래스 **없음**, `color-scheme: light`.
3. 색상 = 회사 8색 + 구조 중립색만. amber·rose 등 의미색 0개.
4. 텍스트: 제목 `co-black` / 본문 `#555555` / 메타 `#A0A0A0`(본문 금지).
5. 카드 = `.paper` (흰 BG + `#DEDEDE` 보더 + shadow-card). `.glass` 없음.
6. KPI는 `brand-600` 솔리드. `.gradient-text`는 문서 3회 이내.
7. 표: `#DEDEDE` thead + zebra + So-What 네이비 바. As-Is/To-Be 표는 To-Be 열 `emphasizeCol` 강조.
8. 강조·경고는 Callout `emphasis`(navy 솔리드) — warn/danger variant 사용 금지.
9. `npm run build` 통과 · ←/→ 키보드 · URL 해시 · 모바일 토글 · dash 애니메이션 동작.
10. 사이드바 활성: navy 막대 + cyan 글로우(rgba(27,187,204,0.55)) 확인.
11. 3개 이상 카드성 자식을 쌓는 컨테이너에는 `space-y-3` (다크 키트 §10.3.2 룰 동일 적용).
12. 두 줄 강제 히어로 문장은 명시적 `<br />` (자연 줄바꿈 금지 — 다크 키트 §10.3.1 동일).

---

## 11. 다크 키트와의 관계

- **레이아웃·컴포넌트 구조·인터랙션·반응형·타이포 스케일은 두 키트가 동일**하다. 다른 것은 §4의 컬러 시스템과 표면 처리(.glass ↔ .paper)뿐.
- 기존 다크 덱을 라이트로 전환할 때는 §4.8 매핑 테이블만 적용하면 된다 (컴포넌트 로직 수정 불필요).
- 한 프로젝트에서 두 테마를 동시 지원하려면 본 킷을 기본으로 하고 `darkMode: "class"` + 다크 키트 토큰을 `dark:` variant로 얹는다.
- **불일치 발견 시 우선순위**: 컬러·강조 규칙은 PPT 가이드(v2.1) > 본 킷 > 다크 키트 순으로 정합화한다.

---

## Changelog

| 버전 | 일자 | 변경 |
|---|---|---|
| **v1.0** | 2026-07-10 | 최초 릴리스 — **Claude Fable 5와 공동 제작.** `DA_WEB_darkUI_KIT.md` v1.3의 레이아웃·컴포넌트·인터랙션 체계 위에 `DA_ppt_design_guide.md` v2.1 라이트 컬러 시스템(흰 캔버스 `#F4F5F7`/`#FFFFFF` · 회사 8색 · 네이비 프라이머리 · Elevation 5단계 · Hero Gradient 한도)을 이식. 개선/정정: ① 다크 키트 §5의 잔존 바이올렛 gradient-text 값과 사이드바 글로우 `rgba(139,169,255)` 잔재를 회사 토큰으로 정정 ② Callout에서 amber/rose 의미색 제거, PPT §1.3 하드 룰로 통일(emphasis 네이비 솔리드로 대체) ③ PPT의 So-What 바·DataTable 강조열(As-Is/To-Be)·Elevation 스케일을 웹 컴포넌트로 신규 이식 ④ 다크→라이트 토큰 매핑 테이블(§4.8) 제공. |

---

## 끝.

`DA_ppt_design_guide.md`(문서) · `DA_WEB_darkUI_KIT.md`(웹 다크) · **`DA_WEBUI_KIT.md`(웹 라이트, 본 문서)** 세 가이드는 같은 회사 8색 시스템을 공유합니다. 변경 사항이 생기면 Changelog에 누적 기록하세요.
