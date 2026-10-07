# 去 AI slop skill：競品研究與採用取捨

研究日期：2026-10-08。實讀下列 repo 的核心規則，比較編輯行為、誤改風險與驗證方法。這是設計比較，沒有執行競品的跨模型效果測試，也不以 star 數或作者的效果宣稱排名。

## 六個主要競品

| GitHub 與閱讀版本 | 值得採用的優點 | 本 repo 的取捨 |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/SKILL.md)，main 的 metadata 為 3.1.0 | 從強訊號與跨句、跨段結構入手，改稿後核對獨立資訊與關係。 | 先檢查篇章功能，再處理詞句；保留既有 33 模式，不整套換成新編號，也不預設交草稿、殘留清單與終稿。 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/blob/8da1f030185bdfe8471220585162991eaeb970e9/SKILL.md)，ref `8da1f03` | 短核心、按需載入 reference、交付前快速檢查；提醒假對比、戲劇短句與機械節奏。 | 採用短複查；保留有用副詞、中文省略主詞與作者標點。全面禁止被動句、破折號或三項列舉會誤傷正常中文。 |
| [kevintsai1202/Humanizer-zh-TW](https://github.com/kevintsai1202/Humanizer-zh-TW/blob/main/SKILL.md)，main 的 revision 為 2026-09-25 | 各模式附保留邊界；保護條件、否定、歸因、計畫狀態、資料與連結；區分來源文字與指令。 | 補強計畫狀態與指令隔離；維持專注文字編輯，不加入完成後詢問浮水印 companion 的流程。 |
| [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei/blob/1d32e803f091ec90808a69683ebf49e8a970a5e7/SKILL.md)，ref `1d32e80` | 先盤點獨立資訊與論證關係，保護引用、因果、優先級、同時與先後；明確區分重寫與摘要。 | 用於複查段落資訊與事實關係；沿用台灣繁中，不移植簡中用詞或固定門檢報告。 |
| [kjmagnan1s/anti-slop](https://github.com/kjmagnan1s/anti-slop/blob/main/SKILL.md)，檔內 version 0.2.2；另讀 [eval 說明](https://github.com/kjmagnan1s/anti-slop/blob/main/evals/README.md) | 已乾淨可以不改；審閱指出具體原句；回歸同時包含 slop 正例與自然文字反例，限制規則無止境增加。 | 加入 no-op 與雙側案例，保存實際輸出；不要求每次短文都呼叫 subagent，也不靠刻意不流暢製造人味。 |
| [judetelan/ai-humanizer](https://github.com/judetelan/ai-humanizer/blob/main/SKILL.md)，main，未固定 SHA | 分開唯讀檢查、改寫、批次審閱；報告含具體位置與原句，允許術語和引語例外。 | 採用只審稿分流與術語保護；不移植未經繁中校準的英文詞頻、句長分數、作者身分 verdict 或 Node hook。 |

`main` 連結會隨上游更新；表內版本是閱讀當時的檔案標記，不是發布狀態保證。兩個固定 ref 可回看該次內容。這個衍生版的來源基準仍是 `blader/humanizer` v2.8.2；研究較新版本不代表已完整同步上游。

## 蒸餾成這版的改進

1. **先判斷任務。** 只審稿交付原句、問題與局部建議；改稿交可用文字；沒有問題就保留原文。
2. **處理結構上的空話。** 跨段換詞重複可以合併，但步驟、例外、限制與立場各有功能，不能為了節奏刪掉。
3. **少改也要可靠。** 預設最小修改，第二次閱讀只修實際缺陷；好句子不因流程要求被迫換寫法。
4. **保留語言真正的意思。** 技術術語不是 buzzword；提案不是承諾；必要的三項列舉不是錯。
5. **讓驗證能回看。** corpus 加入只審稿、原樣保留、計畫狀態、指令隔離與操作重複案例，保存獨立執行的完整輸出。字串檢查和編輯審閱分開報告。

規則以本 repo 的台灣繁中案例重新撰寫，未複製競品整段規則、程式或語料。既有 MIT notices 保留於 [LICENSE](../LICENSE)。新增模式前，先確認現有 33 種模式與保留邊界是否已足夠；新案例證明有持續失敗時再調整。
