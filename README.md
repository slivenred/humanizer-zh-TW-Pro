# humanizer-zh-TW-Pro

[![Validate](https://github.com/slivenred/humanizer-zh-TW-Pro/actions/workflows/validate.yml/badge.svg)](https://github.com/slivenred/humanizer-zh-TW-Pro/actions/workflows/validate.yml)

台灣繁中去 AI slop 編輯 skill，讓文字有內容、說得清楚，也保留作者自己的聲音。可用於改寫、輕修或只審稿；已經自然的文字可以不改。

這是一份給 Claude Code、Codex、OpenCode 等 agent 使用的編輯規則，不是 deterministic 改寫程式。效果取決於模型、原文與保留條件；不提供 AI 生成機率或偵測器通過保證。

## 這版和一般繁中版差在哪

- 追蹤 `blader/humanizer` v2.8.2 的 33 種 AI writing patterns，並選擇性吸收上游品質修正。
- 加入台灣繁中語感：避免陸式商業腔、翻譯腔、斜線 buzzword 串。
- 加入 false-positive 保護：不要看到一個破折號、「此外」或被引用的 AI 詞就硬改。
- 加入 voice matching 隔離：只學作者節奏和語域，不把樣本裡的故事、數字或立場搬進正文。
- 加入語意保真規則：保護主體、數值與單位、條件、否定、歸因、因果和先後關係。
- 禁止用假人味填空，也不能把宣傳詞偷換成「操作簡單、穩定、省時」等未經原文支持的主張。
- 保留原文視角、段落功能與資訊密度；除非使用者要求，不把 humanize 做成摘要。
- 保留引述、URL、frontmatter、表格、程式碼、placeholder、錯誤訊息和 SEO 關鍵字，避免被改壞。
- 區分只審稿、輕修與改寫：先看段落有沒有內容與功能，再修詞句；複查只修實際問題，不強制重寫第二版。
- 詞表是線索，不能誤刪「閉環控制、鏈路聚合、核心 dump」等術語，也不強制拆掉必要的三項清單。

本輪實讀六個主要 GitHub 競品，採用任務分流、最小修改與雙側回歸檢查。比較來源、取捨及對應修改見 [競品研究](docs/competitor-review.md)。

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

手動複製時，將 `SKILL.md` 和 `references/` 一起放進對應 skill 目錄。一般改稿讀主檔即可，完整範例按需載入；維護用 scripts 和 tests 不需在使用時執行。

## 使用

基本用法：

```text
請用 humanizer-zh-tw-pro 幫我改寫下面這段，保留所有價格、來源與限制條件：

[貼上文字]
```

只審稿、不改全文：

```text
請用 humanizer-zh-tw-pro 只審稿。指出有問題的原句、影響與局部建議，先不要改寫全文或檔案。
```

保留已經自然的稿子：

```text
請用 humanizer-zh-tw-pro 必要時小修；沒有實質問題就原樣保留，只給正文。
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
請用 humanizer-zh-tw-pro 審閱並改寫這篇 SEO 頁面。
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

> 這功能不是不好，但現在的流程真的有點卡。每次都要先匯出 CSV，再手動丟到另一個工具；做到第三次就開始懷疑人生。

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

這個 repo 包含 42 組、10 類維護用 forward-test cases，其中有一組 600 字以上的長文。案例同時包含需要清理的稿子與應保留的文字，用來檢查事實關係、作者聲音、任務範圍，以及是否把 humanize 做成摘要。它們不是逐字標準答案。

檢查 repo 與 corpus 一致性：

```bash
python3 scripts/validate_repo.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

如果本機沒有 PyYAML，先執行 `python3 -m pip install PyYAML`。GitHub Actions 也會在 push 和 pull request 時跑同一個檢查。

repo validator 檢查 frontmatter、33 種模式、版本／授權／corpus 一致性、文件連結與 CI 結構；這些是結構檢查，不會呼叫模型或證明改寫品質。

實際 forward-test 要把案例的 `request`、`input` 交給執行 agent，再由另一位編輯或 agent 依 `must_preserve`、`must_avoid`、`success_checks` 審閱。保存完整回應、執行環境與審閱依據後，可重跑離線檢查：

```bash
python3 scripts/check_forward_outputs.py tests/results/2026-10-08-pro6.json
```

離線 checker 只核對記錄格式、版本、案例 ID 和明確要求逐字保留的 `protected_literals`。語意、聲音、是否越出任務範圍，都依記錄中的編輯審閱，不能由字串比對證明。退出碼 0 表示本次提交案例審閱通過且 literals 完整；部分案例通過不等於全部 42 組通過。方法與限制見 [驗證指南](docs/evaluation.md)。

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

### 1.0.0-pro.6

- 新增只審稿與不改稿的分支，預設最小修改，複查不再強制第二版。
- 新增篇章資訊檢查、技術術語例外與來源文字指令隔離，保留提案／計畫狀態。
- 修正計畫語氣與第一人稱範例；33 種模式與編號維持不變。
- corpus 擴充至 42 組；新增實際輸出記錄、離線 literal checker、回歸測試與競品取捨文件。
- 完整改稿範例移至按需載入的 reference；來源基準仍為 v2.8.2，本輪研究另檢視上游 main 的 v3.1.0。

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
