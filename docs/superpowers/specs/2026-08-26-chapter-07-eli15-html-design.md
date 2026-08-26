# Chapter 07 ELI15 HTML 導讀設計

## 目的

新增一份約 15 分鐘可讀完的獨立 HTML 導讀，讓第一次接觸分散式系統的讀者能從真實應用理解唯一 ID，而不是先背 Snowflake 名詞與 bit 配置。

新文件不取代既有 30 分鐘講義或 10 分鐘 quick guide，也不修改 Notion 頁面。它以一筆球鞋訂單的完整旅程作為主線，依序遇到撞號、中央瓶頸、排序與離線產生等問題，最後用實際產品情境完成 ID 選型。

## 交付範圍

- 新增 `chapter-07-unique-id-generator-eli15.html`。
- 單一自包含 HTML，使用 inline CSS 與 vanilla JavaScript。
- 不使用外部套件、字型、圖片、網路請求或建置流程。
- 不修改下列既有內容：
  - `chapter-07-design-a-unique-id-generator.md`
  - `chapter-07-unique-id-generator-quick-guide.html`
  - `notion-pages.json`
  - 已建立的 Chapter 07 Notion 頁面

## 讀者與語氣

- 讀者心智年齡約 15 歲，不假設熟悉 UUID、Snowflake、資料庫索引或分散式協調。
- 用自然的繁體中文短句解釋，技術詞只在讀者已經遇到相應問題後出現。
- 不用幼兒化語氣；比喻之後必須立刻對回真實系統。
- 每個概念都回答四件事：在哪裡會用、現在遇到什麼問題、這個解法怎麼處理、代價是什麼。

## 敘事主線

採用「A 主線 + C 結尾選型」：

1. **小明按下購買**
   - 前端先用 temporary ID 顯示「訂單建立中」。
   - 後端需要替訂單產生永久 ID。
   - 說明永久 ID 是資料長期使用的名字，不只是畫面編號。
2. **三台伺服器同時接單**
   - Load Balancer 把請求分到不同伺服器。
   - 如果每台都從 101 開始數，可能產生相同 ID。
   - 從實際撞號後果帶出唯一性：訂單互相覆蓋、付款對錯人、查詢拿錯資料。
3. **四次發號嘗試**
   - 單一資料庫自增：簡單，但所有人都要排同一個櫃台。
   - 多主奇偶號：可分流，但擴充與時間順序變複雜。
   - UUIDv4：各自產生，但很長且不適合本章的 64-bit、時間排序需求。
   - Ticket Server：短且有序，但中央發號服務又成為依賴。
4. **推導 Snowflake**
   - 把 ID 類比為包裹標籤，標記「什麼時候、哪台機器、同一毫秒第幾筆」。
   - 先理解 timestamp、machine identity、sequence 的責任，再補充 64-bit bit 配置。
   - 強調不是完全零協調，而是從每筆請求協調，縮小成部署時分配節點身分。
5. **現實故障**
   - 時鐘倒退：可能回到用過的號碼範圍。
   - sequence 用完：必須等下一毫秒或分流，不能繞回零。
   - machine ID 重複：兩台機器進入同一個 ID 空間。
   - 前端 JavaScript：Snowflake 應以字串傳輸與保存，不能任意轉成 `Number`。
6. **情境選型**
   - 小型單機後台：優先考慮資料庫自增。
   - 離線 App：考慮 UUIDv7 或 ULID。
   - 大量內部訂單或事件：需要 64-bit、時間趨勢與高吞吐時考慮 Snowflake。
   - 公開訂單網址：內部可用 Snowflake，外部另用不可推測的 public ID。

## 15 分鐘節奏

- 0-2 分鐘：ID 在真實產品中的責任。
- 2-6 分鐘：三台伺服器撞號與四種方案。
- 6-10 分鐘：Snowflake 三段資訊與 64-bit 配置。
- 10-12 分鐘：三種故障與前端大型整數。
- 12-15 分鐘：四個實際情境的選型練習。

## 視覺設計

採用「故事捲動式」單欄主內容：

- 桌面為 sticky 左側旅程導覽加右側內容。
- 手機將導覽改為可水平捲動的進度列。
- 內容使用全寬段落與少量有語意的工具框，不把每一段包成卡片。
- 每個場景依序顯示：
  - `SCENE` 標籤
  - 情境標題
  - 真實系統流程
  - 現在的問題
  - 解法
  - 代價
  - 一句話結論
- 使用既有系列色彩：
  - paper `#f7f8f5`
  - surface `#ffffff`
  - ink `#17201b`
  - muted `#5e6a63`
  - problem `#b4473a`
  - solution `#16745b`
  - system `#245f9e`
  - warning `#9a6a12`
- 不使用漸層、裝飾性光球、外部圖片或行銷式 hero。
- 固定格式的流程圖、Snowflake bit 帶與選型控制設定穩定尺寸，互動時不造成 layout shift。

## 互動

### 先猜猜看

每個關鍵問題使用原生 `details/summary` 或漸進增強按鈕。讀者先看到問題，展開後才看到答案、原因與代價。停用 JavaScript 時答案仍可透過原生控制閱讀。

### Snowflake 拆解

提供 timestamp、machine identity、sequence 三個可點選區段：

- 點選後更新下方說明與實際例子。
- 選取狀態同時使用色彩、文字與 `aria-pressed`，不只依賴顏色。
- 互動不改變 bit 帶的寬高。

### 情境選型

提供四題單選情境：

- 讀者選擇後立即顯示建議方案。
- 每個答案都說明原因與代價，不只顯示對錯。
- 未啟用 JavaScript 時，完整建議放在原生 `details` 中。

### 導覽

- 使用 `IntersectionObserver` 更新目前閱讀位置。
- 不支援 `IntersectionObserver` 時，所有連結仍可正常錨點跳轉。
- 尊重 `prefers-reduced-motion`，核心理解不依賴動畫。

## 內容正確性

- Snowflake 主線使用 `timestamp + node identity + sequence`。
- 原章示例配置維持 `1 + 41 + 5 + 5 + 12 = 64 bits`。
- 清楚區分唯一、趨勢遞增、嚴格連號與不可猜測。
- UUIDv7、ULID 只出現在選型，不展開成另一份技術講義。
- 理論吞吐不寫成實測效能。
- ID 不等於授權；公開 ID 與內部主鍵可分開設計。

## 響應式與可及性

- 支援 1440x900 桌面與 390x844 手機視窗。
- 內容不得產生頁面水平溢出；只有明確標示的程式碼或圖表容器可水平捲動。
- 所有互動可使用鍵盤完成，並有可見的 `:focus-visible` 樣式。
- 文字與背景符合可讀對比。
- 控制項有固定高度，長文字可換行且不重疊。
- 使用語意化 heading、nav、main、section、button、details 與 table。

## 驗收標準

- 新 HTML 可直接開啟，不需要 dev server 或外部資源。
- 讀者能回答：
  - 為什麼多台伺服器會讓流水號變難？
  - Snowflake 的三段資訊各自避免什麼衝突？
  - 哪些情境不需要 Snowflake？
- 內容包含至少三種真實應用：訂單、聊天訊息或事件、公開網址或離線 App。
- 所有「先猜猜看」、Snowflake 拆解與四題選型互動可用。
- JavaScript 語法檢查通過，無 console error。
- 桌面與手機均無文字重疊、不可理解的裁切或整頁水平溢出。
- 原講義、原 quick guide、Notion mapping 的實作前後雜湊一致。
- Git diff 只包含新 HTML、已核准的規格與後續計畫文件；不包含 Visual Companion 暫存內容。

## 非目標

- 不重寫或取代 30 分鐘正式講義。
- 不修改既有 quick guide。
- 不同步或更新 Notion。
- 不實作可部署的 ID 生成服務。
- 不做套件或雲端產品推薦。
- 不把所有 UUID 版本或 Snowflake 變體納入範圍。
