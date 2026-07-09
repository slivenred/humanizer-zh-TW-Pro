# Changelog

本檔記錄 `humanizer-zh-tw-pro` 的使用者可見變更。版本號與 `SKILL.md` metadata、README 版本紀錄同步。

## [1.0.0-pro.5] - 2026-07-10

### Added

- 新增語意保真契約，保護主體、數值與單位、條件、否定、比較方向、來源歸因、因果與先後關係。
- 新增假人味、voice sample 污染、過度壓縮、secondhand text 與結構化內容保護。
- Forward-test corpus 從 24 組擴充為 34 組，加入方案關係、長文完整度、具名歸因、矛盾、markup、false positive、作者立場與未知行為者案例。
- README 新增三組使用前／使用後案例，涵蓋產品與 SEO、作者聲音及來源歸因。
- README 新增 Skills CLI 安裝方式。

### Changed

- 上游追蹤基準從 `blader/humanizer` v2.8.0 更新至 v2.8.2；33 種模式與編號維持不變。
- 重寫完整範例，讓改寫前後保留相同視角、資訊範圍、數字與限制。
- 更新預設 invocation prompt，要求保留原文視角、細節、事實關係與作者聲音。
- 強化 repo validator，加入 changelog 版本同步、核心 pattern 內容、CI 結構和固定 corpus 數量檢查。

### Fixed

- 修正多組前／後範例把抽象 AI 腔改寫成新功能、效果或來源的問題。
- 修正直接引述、中文自然省略主詞、無來源宣傳背書與「宣傳詞被偷換成溫和產品主張」的處理邊界。
- 修正長文案例的 heading 計數與既有 corpus 中幾項互相衝突的保留條件。

### Validation

- `python3 scripts/validate_repo.py` 通過：34 組案例、10 類別，並具備長文覆蓋。
- 官方 skill validator 通過。
- 8 組全新 agent forward tests 通過，涵蓋事實關係、作者聲音、引述、來源、長文與受保護 markup。
- 負向 validator 測試確認：停用 CI、清空 pattern 內容與 corpus 數量漂移都會被拒絕。

## [1.0.0-pro.4]

- 保護直接引述、逐字稿、法規／合約、品牌與產品名稱、UI 標籤、程式碼、命令、錯誤訊息及 SEO 關鍵字。

## [1.0.0-pro.3]

- 強化交付前事實核對、正文與審稿說明分離，以及範例的來源邊界。

## [1.0.0-pro.2]

- 改善 skill trigger description，並明確禁止從範例補寫功能、日期、數據、來源、排名或效果。

## [1.0.0-pro.1]

- 以 `blader/humanizer` v2.8.0 為基底建立台灣繁中 Pro 版本，加入 false-positive、voice matching、SEO 與事實保留規則。
