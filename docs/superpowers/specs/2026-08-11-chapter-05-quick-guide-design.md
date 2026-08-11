# Chapter 05 快速概念版設計

## 目的

比照第六章的快速版模式，另外製作一份可在約 8 分鐘內讀完的第五章快速版，幫助讀者先建立「為什麼需要一致性雜湊」的整體因果鏈。原始講義 `chapter-05-consistent-hashing.md` 保持不變。

讀完後，讀者應該能說明：傳統 `hash mod N` 為什麼會在伺服器數量變動時引發大規模快取失效、Hash Ring 如何把影響範圍限縮到「相鄰資料」、以及為什麼還需要 Virtual Nodes 來解決分布不均。

## 讀者與語氣

延用第六章快速版的原則：日常用語優先、技術名詞先講用途、不假設讀者已熟悉 Hash Ring 或 Virtual Nodes、名詞出現前先交代它解決的問題。

## 輸出形式與範圍

新增單檔 HTML artifact：`chapter-05-consistent-hashing-quick-guide.html`，不修改原始第五章。視覺與互動系統與第六章版本一致（同一套 CSS token、layout、導覽與 details 自我檢查模式），維持系列一致性。

快速版涵蓋：

- 傳統 `hash(key) mod N` 的 rehashing 問題（Cache Miss Storm）
- Hash Ring：伺服器與 key 都放上環，順時針找負責節點
- 新增 / 移除伺服器時，只有相鄰資料受影響
- 基本版分布不均的兩個問題（弧長不均、key 分布偏斜）與熱點問題
- Virtual Nodes 如何讓分布趨近均勻，並把伺服器增減的影響打散到整個環

不深入 SHA-1 計算細節、環的二分查找實作、或各資料庫（Dynamo/Cassandra）差異比較。

## 閱讀動線

1. **Recap（一分鐘）**：從 `hash(key) mod N` 的直覺模型切入，畫出「新增/移除伺服器 → mod 結果全變」的具體例子。
2. **因果鏈總覽**：一條簡短路線圖，對應原始講義的因果鏈（mod N 問題 → Hash Ring → 分布不均 → Virtual Nodes）。
3. **三個概念區塊**，格式與第六章相同（現在的問題 / 怎麼做 / 代價 / 一句話）：
   - Hash Ring
   - 分布不均與熱點問題
   - Virtual Nodes
4. **收尾**：問題/解法/代價表格 + 三題自我檢查（details 收合）。

## 驗收標準

- 一般讀者可在約 8 分鐘內讀完主要內容。
- 開頭先建立 `mod N` 模型與具體失效例子，之後才出現 Hash Ring 等術語。
- 每個新名詞第一次出現時都有一句白話用途說明。
- 讀完後能回答：為什麼 mod N 會大規模失效、Hash Ring 如何限縮影響範圍、為什麼還需要 Virtual Nodes。
- 原始 `chapter-05-consistent-hashing.md` 沒有任何變更。
- HTML 可直接開啟，桌面與手機寬度下都沒有文字溢出或控制項重疊。
- 視覺與互動風格與 `chapter-06-key-value-store-quick-guide.html` 一致（同一 token 系統）。

## 非目標

- 不取代完整第五章。
- 不增加完整面試問答或參考解答。
- 不修改或重新匯出既有 Notion 頁面。
- 不依賴外部字型、圖片、JavaScript 套件或網路連線。
