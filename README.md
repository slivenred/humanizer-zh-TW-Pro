# humanizer-zh-TW-Pro

[![Validate](https://github.com/slivenred/humanizer-zh-TW-Pro/actions/workflows/validate.yml/badge.svg)](https://github.com/slivenred/humanizer-zh-TW-Pro/actions/workflows/validate.yml)

台灣繁中版 AI 寫作痕跡清理 skill。  
它不是 deterministic 改寫程式，而是一份給 Claude Code、Codex、OpenCode 等 agent 使用的編輯規則。效果取決於執行它的模型、原文品質，以及你給的保留條件。

## 這版和一般繁中版差在哪

- 追蹤 `blader/humanizer` v2.8.2 的 33 種 AI writing patterns，並選擇性吸收上游品質修正。
- 加入台灣繁中語感：避免陸式商業腔、翻譯腔、斜線 buzzword 串。
- 加入 false-positive 保護：不要看到一個破折號、「此外」或被引用的 AI 詞就硬改。
- 加入 voice matching 隔離：只學作者節奏和語域，不把樣本裡的故事、數字或立場搬進正文。
- 加入語意保真規則：保護主體、數值與單位、條件、否定、歸因、因果和先後關係。
- 禁止用假人味填空，也不能把宣傳詞偷換成「操作簡單、穩定、省時」等未經原文支持的主張。
- 保留原文視角、段落功能與資訊密度；除非使用者要求，不把 humanize 做成摘要。
- 保留引述、URL、frontmatter、表格、程式碼、placeholder、錯誤訊息和 SEO 關鍵字，避免被改壞。
- 加入二次審稿流程：先改，再問「哪裡還像 AI？哪裡被洗太平？」再修一次。

## 安裝

### Skills CLI

安裝到所有支援的 agent：

```bash
npx skills add slivenred/humanizer-zh-TW-Pro -g --agent '*'
```

CLI 會辨識 repo 內的 `humanizer-zh-tw-pro` skill。也可以使用下方方式手動安裝到單一 agent。

### Codex

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/slivenred/humanizer-zh-TW-Pro.git ~/.codex/skills/humanizer-zh-tw-pro
```

### Claude Code

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/slivenred/humanizer-zh-TW-Pro.git ~/.claude/skills/humanizer-zh-tw-pro
```

### OpenCode

```bash
mkdir -p ~/.config/opencode/skills
git clone https://github.com/slivenred/humanizer-zh-TW-Pro.git ~/.config/opencode/skills/humanizer-zh-tw-pro
```

也可以只把 `SKILL.md` 複製到對應 skill 目錄。

## 使用

基本用法：

```text
請用 humanizer-zh-tw-pro 幫我改寫下面這段，保留所有價格、來源與限制條件：

[貼上文字]
```

帶作者聲音樣本：

```text
請用 humanizer-zh-tw-pro 改寫。這是我的寫作樣本，請保留我的句子節奏和用詞：

[貼上樣本]

下面是要改的文字：

[貼上文字]
```

用於 SEO 頁面：

```text
請用 humanizer-zh-tw-pro 審閱這篇 SEO 頁面。
不要新增未驗證事實，不要刪掉價格、日期、來源、比較條件或但書。
只輸出可直接發布的正文。
```

## 範本案例：使用前／使用後

以下範例呈現這個 skill 的目標行為；實際措辭會依模型、原文和使用者要求不同。判斷效果時，應檢查事實、語意關係、作者聲音和受保護內容是否保留，而不是要求逐字相同。

### 產品與 SEO：保留價格、功能與限制

**使用前：**

> 這款圖片壓縮工具在 2026 年 6 月推出 Pro 方案，每月 US$9，支援 WordPress 外掛，但目前不支援 AVIF。它是一站式、革命性的影像優化解決方案，能全方位賦能你的內容生態。

**使用後：**

> 這款圖片壓縮工具於 2026 年 6 月推出 Pro 方案，每月 US$9，支援 WordPress 外掛，目前不支援 AVIF。

**效果觀察：**

- 保留推出日期、方案名稱、價格、WordPress 外掛和 AVIF 限制。
- 移除「一站式、革命性、全方位賦能」等沒有實質資訊的宣傳詞。
- 沒有自行補上折扣、壓縮率或其他產品功能。

### 作者聲音：去掉公式開場，不洗掉吐槽

**使用前：**

> 老實說？這功能不是不好，但現在的流程真的有點卡。每次要先匯出 CSV，再手動丟到另一個工具，做到第三次就會開始懷疑人生。

**使用後：**

> 這功能不是不好，但現在的流程真的有點卡。每次都要先匯出 CSV，再手動丟到另一個工具；做到第三次，我就開始懷疑人生。

**效果觀察：**

- 拿掉「老實說？」這類公式化開場，保留原本直接、帶吐槽的語氣。
- 保留匯出 CSV、手動轉交工具和重複操作的具體流程。
- 沒把負面經驗改成中性公告，也沒有捏造自動同步等功能。

### 來源歸因：保留誰說了什麼

**使用前：**

> 根據 [Acme 2026 年 7 月更新紀錄](https://example.com/changelog/2026-07)，Acme 表示新的批次匯入功能可把等待時間縮短 30%。這是廠商公布的測試結果，而且功能仍是 Beta，目前不提供給歐盟帳號。業界普遍認為這項突破將重塑內容生態。

**使用後：**

> 根據 [Acme 2026 年 7 月更新紀錄](https://example.com/changelog/2026-07)，Acme 表示，新的批次匯入功能可將等待時間縮短 30%。這是廠商公布的測試結果；功能仍是 Beta，目前不提供給歐盟帳號。

**效果觀察：**

- 保留具名來源、原始連結，以及「30% 是 Acme 公布的結果」這層歸因。
- 保留 Beta 狀態與歐盟帳號限制，沒有把廠商測試寫成客觀定論。
- 移除沒有來源的「業界普遍認為」，也沒有補寫第三方背書。

## Forward-test corpus

這個 repo 另外包含 34 組、10 類維護用 forward-test cases，其中包含一組 600 字以上的長文案例。它們用來避免後續版本越改越重、把事實關係和作者聲音改壞，或把 humanize 做成摘要。這不是標準答案集，而是列出每個樣本必須保留、必須避免和人工審閱時要看的行為。

檢查 repo 與 corpus 一致性：

```bash
python3 scripts/validate_repo.py
```

如果本機沒有 PyYAML，先執行 `python3 -m pip install PyYAML`。GitHub Actions 也會在 push 和 pull request 時跑同一個檢查。

這個總檢查會驗證官方 skill frontmatter 契約、33 組 pattern 的核心內容、`SKILL.md` / `README.md` / `CHANGELOG.md` / `agents/openai.yaml` / `LICENSE` / forward-test corpus 的一致性，以及 GitHub Actions 的結構。人工 forward-test 時，從 `tests/forward_cases.json` 挑選案例，使用該案例的 `request` 和 `input` 跑一次 skill，再用 `must_preserve`、`must_avoid`、`success_checks` 做審閱。只有在案例暴露明確失敗時，才修改 `SKILL.md`。

## 33 種模式

### 內容模式

| # | 模式 |
|---:|---|
| 1 | 過度放大意義、歷史定位和大趨勢 |
| 2 | 過度強調知名度和媒體露出 |
| 3 | 膚淺的補充分析 |
| 4 | 宣傳和廣告腔 |
| 5 | 模糊歸因和含糊權威 |
| 6 | 公式化的「挑戰與未來展望」 |

### 語言模式

| # | 模式 |
|---:|---|
| 7 | 過度使用 AI 詞彙 |
| 8 | 逃避簡單的「是 / 有 / 可以」 |
| 9 | 否定式排比和尾端否定 |
| 10 | 三段式過度使用 |
| 11 | 同義詞輪替 |
| 12 | 假範圍 |
| 13 | 被動語態和無主詞片段 |

### 風格模式

| # | 模式 |
|---:|---|
| 14 | 破折號和連字號濫用 |
| 15 | 粗體過度使用 |
| 16 | 內嵌標題式列表 |
| 17 | 英文標題 Title Case 濫用 |
| 18 | 表情符號裝飾 |
| 19 | 引號與標點不一致 |

### 對話殘留和保留語

| # | 模式 |
|---:|---|
| 20 | 聊天機器人對話殘留 |
| 21 | 知識截止與猜測補洞 |
| 22 | 諂媚和過度認同 |
| 23 | 填充短語 |
| 24 | 過度保留和模糊化 |
| 25 | 通用正向結論 |

### v2.8 / Pro 補強模式

| # | 模式 |
|---:|---|
| 26 | 複合形容詞、斜線名詞和 buzzword 串 |
| 27 | 權威姿態和說服腔 |
| 28 | 路標式開場和公告 |
| 29 | 碎片化標題 |
| 30 | 變更紀錄腔 |
| 31 | 製造出來的金句和戲劇短句 |
| 32 | 格言公式 |
| 33 | 假裝坦白的修辭開場 |

## 版本紀錄

### 1.0.0-pro.5

- 追蹤上游至 `blader/humanizer` v2.8.2，吸收 secondhand-text false-positive 與「不要靠刪短完成 humanize」的品質修正；33 種模式不變。
- 新增語意保真、假人味、voice sample 隔離、宣傳詞不是證據，以及結構化內容保護規則。
- 修正多組會示範補寫新事實的前／後範例、直接引述誤改與中文主詞過度補齊問題，並重寫完整範例。
- forward-test corpus 從 24 組擴充為 34 組，加入方案關係、長文完整度、具名歸因、矛盾、markup、false positive、作者立場與未知行為者案例。
- repo validator 會檢查上游版本、官方 frontmatter 契約、核心 pattern 內容與 CI 結構；corpus validator 會鎖定 34 組案例並要求長文覆蓋。
- README 新增三組使用前／使用後案例，並新增 `CHANGELOG.md` 保存 release 紀錄。

### 1.0.0-pro.4

- 新增「不要硬改的內容」護欄，保護直接引述、逐字稿、法規/合約原文、品牌名、產品名、UI 標籤、程式碼、API、命令、錯誤訊息和 SEO 目標關鍵字。
- 明確要求原文看起來不自然時，優先改周圍說明文字，避免把結構化內容或引用內容改壞。

### 1.0.0-pro.3

- 強化交付前自檢，明確核對人名、品牌、產品、價格、日期、版本、來源、不確定語氣和限制條件。
- 補清楚正文與審稿說明的分界，避免把「此處需要來源」或編輯註解混進可發布內容。
- 收緊範例使用邊界，只有在任務允許查證且已查到來源時，才可加入有來源佐證的新資訊。

### 1.0.0-pro.2

- 改寫 skill trigger description，讓 Codex 更容易在「去 AI 味」、humanize、台灣繁中改寫和 SEO 審稿情境中正確觸發。
- 新增範例使用邊界，明確要求不得從示範句自行補功能、日期、數據、來源、排名或效果。
- 將 SEO 保護用語中的 `caveat` 改成更自然的「但書」。

### 1.0.0-pro.1

- 以 `blader/humanizer` v2.8.0 為基底，完整保留 33 種模式的結構。
- 在地化為台灣繁中，補入陸式商業腔、翻譯腔、SEO 內容保護、事實保留規則。
- 加入 false-positive 保護，避免把已有作者聲音的文章磨平。
- 加入 voice matching 和二次審稿流程。

## 授權與來源

MIT。

本專案是衍生版本，主要來源：

- [`blader/humanizer`](https://github.com/blader/humanizer) v2.8.2，MIT。
- [`kevintsai1202/Humanizer-zh-TW`](https://github.com/kevintsai1202/Humanizer-zh-TW)，MIT，作為既有繁中版本差異參考。
- Wikipedia: [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)。

若你公開發布 fork，請保留原 MIT copyright notice 與此來源說明。
