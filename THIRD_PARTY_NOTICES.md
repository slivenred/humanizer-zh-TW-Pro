# 第三方來源與授權聲明

核對日期：2026-10-08。本檔區分既有衍生來源、這次研究參考，以及 Wikipedia 的來源鏈；列出參考專案不表示本 repo 收錄其全部程式或文字。

## 本 repo 的授權範圍

- 原創程式、編輯指令、測試與其他原創內容依根目錄 [LICENSE](LICENSE) 的 MIT 條款發布。既有 MIT 上游的 copyright 與 permission notice 保留。
- `SKILL.md` 中從「33 種 AI 寫作模式」至「False positives：不要誤殺真人文字」之前的模式目錄，以及 `README.md` 的對應 33 種模式表，作為 Wikipedia 來源鏈的在地化改作，依 **CC BY-SA 4.0** 發布。原創補充一併以此授權發布，避免下游需要逐句判別目錄內的來源。
- `SKILL.md` 的 `MIT AND CC-BY-SA-4.0` 表示檔案內含這兩種授權範圍，不表示可任選 MIT 來取代 CC BY-SA 條件。根目錄 MIT LICENSE 不覆蓋第三方原本適用的授權。

## Wikipedia 衍生內容

作者：**Wikipedia contributors**；原頁由 WikiProject AI Cleanup 社群維護。

- 原始來源：[Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)。
- 作者與修訂紀錄：[page history](https://en.wikipedia.org/w/index.php?title=Wikipedia:Signs_of_AI_writing&action=history)。
- 授權：[Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/)，[完整條款](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en)。
- 來源鏈：Wikipedia 的模式整理經 `blader/humanizer` 轉為 agent skill，再由本 repo 在地化；`kevintsai1202/Humanizer-zh-TW` 也作為既有繁中版本參考。上游的 MIT 標示不取消 Wikipedia 衍生內容的條件。
- 本 repo 的變更：改為台灣繁中，重寫說明與示例，整理為 33 種模式，加入台灣用詞、SEO／事實保留、false-positive、作者聲音與語意保護。本檔沒有指定無法核實的歷史 Wikipedia revision ID。

散布或改作上述模式目錄時，保留作者署名、來源與授權連結，標明自己的變更；改作部分依 CC BY-SA 4.0 或其允許的相容授權分享，不對該部分加上授權禁止的限制。授權與下游使用條件以連結中的完整條款為準。其他原創程式與獨立內容維持 MIT。

## GitHub 來源與使用方式

| 來源及已核對的 LICENSE | 使用方式 | 上游 copyright notice |
|---|---|---|
| [blader/humanizer](https://github.com/blader/humanizer/blob/main/LICENSE) | 既有主要衍生基準為 v2.8.2；本輪另研究 main v3.1.0，未完整同步。 | Copyright (c) 2025 Siqi Chen |
| [kevintsai1202/Humanizer-zh-TW](https://github.com/kevintsai1202/Humanizer-zh-TW/blob/main/LICENSE) | 既有繁中差異參考；保留原上游 notice。 | Copyright (c) 2026 歸藏 |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop/blob/8da1f030185bdfe8471220585162991eaeb970e9/LICENSE) | 本輪參考短核心與複查方式；未移植整段規則或例文。 | Copyright (c) 2025 Hardik Pandya |
| [LifelongLazyLearner/qu-ai-wei](https://github.com/LifelongLazyLearner/qu-ai-wei/blob/1d32e803f091ec90808a69683ebf49e8a970a5e7/LICENSE) | 本輪參考資訊與關係核對；未移植原文或程式。 | Copyright (c) 2026 @LifelongLazyLearner |
| [kjmagnan1s/anti-slop](https://github.com/kjmagnan1s/anti-slop/blob/main/LICENSE)，[來源紀錄](https://github.com/kjmagnan1s/anti-slop/blob/main/CREDITS.md) | 本輪參考 no-op 與雙側回歸方法；未移植 detector、規則庫或語料。 | Copyright (c) 2026 Kevin Magnan |
| [judetelan/ai-humanizer](https://github.com/judetelan/ai-humanizer/blob/main/LICENSE) | 本輪參考檢查／改寫分流及術語例外；未移植 Node detector、hook 或詞表。 | Copyright (c) 2026 judetelan |

上述六份 LICENSE 均為 MIT。表內 notices 保留來源的原字句；研究參考來源不因此被標成實際程式依賴或本 repo 全部內容的著作權人。這次新增 checker、測試與案例由本 repo 撰寫。`references/editing-examples.md` 的完整改稿例則搬自本 repo 既有 `SKILL.md`。

## 上述 MIT 來源的完整 permission notice

下列共通條款連同上表各來源的 copyright notice，保留各 MIT 來源的授權文字；它僅適用於相應 MIT 材料，不替代上面的 CC BY-SA 範圍。

```text
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
