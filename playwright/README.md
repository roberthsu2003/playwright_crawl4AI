# Python Playwright 完整教學講義

## 課程簡介
本課程專為只會簡單 Python 的學員設計，從 Playwright 基礎開始，循序漸進地學習網頁自動化與爬蟲技術。

## 資料夾導覽

| 資料夾 | 內容 | 入口 |
|---|---|---|
| `課程章節/` | 第 01～12 章講義、本機 Demo 與真實網站範例 | [課程章節導覽](課程章節/README.md) |
| `實戰專案/` | 12 個與章節對應的真實網站專案 | [實戰專案導覽](實戰專案/README.md) |
| `延伸專案/` | PTT、維基百科與高鐵綜合型專案 | [延伸專案導覽](延伸專案/README.md) |

---

## 課程大綱

### **[第一章：Playwright 簡介](課程章節/第01章_Playwright簡介/README.md)**
#### 1.1 什麼是 Playwright？
- Web 自動化測試工具
- 與 Selenium 的比較
- Playwright 的優勢（速度快、支援多瀏覽器、更穩定）

#### 1.2 Playwright 的應用場景
- 網頁爬蟲（抓取動態網站資料）
- 自動化測試
- 網頁截圖與 PDF 生成
- 表單自動填寫

#### 1.3 環境安裝與設定
- Python 環境檢查
- 安裝 Playwright：`pip install playwright`
- 下載瀏覽器驅動：`playwright install`
- 第一個測試程式

---

### **[第二章：基礎操作](課程章節/第02章_基礎操作/README.md)**
#### 2.1 啟動瀏覽器
- 同步 vs 異步（sync/async）模式
- 啟動 Chromium、Firefox、WebKit
- 有頭模式 vs 無頭模式（headless）

#### 2.2 頁面導航
- 開啟網頁：`page.goto()`
- 等待頁面載入
- 頁面刷新與返回

#### 2.3 基本互動操作
- 點擊元素：`click()`
- 輸入文字：`fill()` 和 `type()`
- 選擇下拉選單
- 勾選核取方塊與單選按鈕

---

### **[第三章：元素定位](課程章節/第03章_元素定位/README.md)**
#### 3.1 CSS 選擇器
- 基本 CSS 選擇器語法
- 類別、ID、屬性選擇器
- 組合選擇器

#### 3.2 XPath 定位
- XPath 基礎語法
- 相對路徑與絕對路徑
- 常用 XPath 表達式

#### 3.3 Playwright 內建定位器
- `get_by_text()`：根據文字定位
- `get_by_role()`：根據角色定位
- `get_by_label()`：根據標籤定位
- `get_by_placeholder()`：根據提示文字定位
- `get_by_test_id()`：根據測試 ID 定位

#### 3.4 定位策略最佳實踐
- 優先順序建議
- 如何處理動態元素

---

### **[第四章：等待與同步](課程章節/第04章_等待與同步/README.md)**
#### 4.1 為什麼需要等待？
- 網頁載入的非同步性質
- 常見的時機問題

#### 4.2 自動等待機制
- Playwright 的智慧等待
- 預設超時時間設定

#### 4.3 明確等待
- `wait_for_selector()`：等待元素出現
- `wait_for_load_state()`：等待頁面狀態
- `wait_for_timeout()`：固定時間等待（應避免）

#### 4.4 等待事件
- 等待導航完成
- 等待請求/回應
- 自訂等待條件

---

### **[第五章：資料擷取](課程章節/第05章_資料擷取/README.md)**
#### 5.1 獲取元素內容
- `inner_text()`：取得文字內容
- `text_content()`：取得所有文字
- `inner_html()`：取得 HTML 內容

#### 5.2 獲取屬性值
- `get_attribute()`：取得元素屬性
- 常用屬性（href、src、value 等）

#### 5.3 處理多個元素
- `query_selector_all()`：取得所有符合的元素
- 迴圈處理元素列表
- 批量資料擷取

#### 5.4 實作：爬取商品列表
- 實際案例：電商網站商品資訊

---

### **[第六章：進階互動](課程章節/第06章_進階互動/README.md)**
#### 6.1 滑鼠操作
- 懸停（hover）
- 拖曳（drag and drop）
- 雙擊與右鍵點擊

#### 6.2 鍵盤操作
- 按鍵輸入
- 組合鍵（Ctrl、Shift 等）
- 特殊按鍵

#### 6.3 滾動操作
- 滾動到元素位置
- 滾動到頁面底部
- 處理無限滾動頁面

#### 6.4 檔案上傳與下載
- 上傳檔案
- 下載檔案並儲存

---

### **[第七章：多頁面與框架處理](課程章節/第07章_多頁面與框架處理/README.md)**
#### 7.1 處理多個分頁
- 開啟新分頁
- 切換分頁
- 關閉分頁

#### 7.2 處理彈出視窗
- 監聽彈出視窗
- 處理 alert、confirm、prompt

#### 7.3 處理 iframe
- 切換到 iframe
- 在 iframe 中操作元素

#### 7.4 實作：處理多視窗網站

---

### **[第八章：截圖與錄影](課程章節/第08章_截圖與錄影/README.md)**
#### 8.1 頁面截圖
- 全頁面截圖
- 元素截圖
- 自訂截圖區域

#### 8.2 錄製操作影片
- 開始錄影
- 停止並儲存影片

#### 8.3 生成 PDF
- 將網頁儲存為 PDF
- PDF 格式設定

---

### **[第九章：網路請求與回應](課程章節/第09章_網路請求與回應/README.md)**
#### 9.1 監聽網路請求
- 攔截 API 請求
- 查看請求內容

#### 9.2 模擬網路回應
- Mock API 回應
- 修改回應內容

#### 9.3 處理 AJAX 請求
- 等待特定 API 完成
- 獲取 API 回應資料

#### 9.4 實作：抓取動態載入的資料

---

### **[第十章：登入與 Cookie 處理](課程章節/第10章_登入與Cookie處理/README.md)**
#### 10.1 自動登入
- 填寫登入表單
- 處理驗證碼（手動介入）

#### 10.2 Cookie 管理
- 儲存 Cookie
- 載入已儲存的 Cookie
- 保持登入狀態

#### 10.3 Session 保存
- 儲存瀏覽器上下文
- 重複使用登入狀態

---

### **[第十一章：反爬蟲對策](課程章節/第11章_反爬蟲對策/README.md)**
#### 11.1 常見的反爬蟲機制
- User-Agent 檢測
- IP 限制
- JavaScript 挑戰

#### 11.2 應對策略
- 設定 User-Agent
- 使用代理伺服器
- 控制請求速度

#### 11.3 模擬真實使用者行為
- 隨機延遲
- 滑鼠軌跡模擬
- 視窗大小設定

---

### **[第十二章：效能優化](課程章節/第12章_效能優化/README.md)**
#### 12.1 提升爬蟲速度
- 禁用圖片載入
- 禁用 CSS
- 禁用字體載入

#### 12.2 平行處理
- 多個瀏覽器上下文
- 多執行緒爬取
- 批次處理

#### 12.3 資源管理
- 正確關閉瀏覽器
- 記憶體管理
- 錯誤處理與重試機制

---

### **[第十三章：實戰專案](實戰專案/README.md)**
- 12 個章節各有一個對應的真實網站專案
- 涵蓋表單、定位、等待、爬取、多視窗、截圖、API、登入狀態與效能優化
- 每個專案都有可執行 `main.py`、輸出成果與延伸挑戰
- 練習網站包含 SauceDemo、The Internet、Books to Scrape、Wikipedia 等
- [12 份可直接複製的 AI 介面設計 Prompt](實戰專案/AI介面設計Prompt.md)

---

## 完整實戰專案

### **[專案一：PTT 熱門文章爬蟲](延伸專案/01_PTT熱門文章爬蟲/README.md)**
- 爬取 PTT 熱門看板文章
- 擷取文章標題、作者、日期等資訊
- 資料儲存與處理

### **[專案二：維基百科搜尋器](延伸專案/02_維基百科搜尋器/README.md)**
- 自動搜尋維基百科關鍵字
- 擷取搜尋結果與文章內容
- 多語言支援

### **[專案三：台灣高鐵時刻表查詢](延伸專案/03_台灣高鐵時刻表查詢/README.md)**
- 自動查詢高鐵時刻表
- Cookie 管理與保存
- 動態時間計算（現在時間 + 1 小時）
- 表單自動填寫與資料擷取
- 票價資訊抓取

---

## 附錄

### A. 常用 Playwright API 速查表
- [Playwright Python API 參考](https://playwright.dev/python/docs/api/class-playwright)
- [頁面操作 API](https://playwright.dev/python/docs/api/class-page)
- [元素定位器 API](https://playwright.dev/python/docs/api/class-locator)

### B. CSS 選擇器與 XPath 對照表
- [CSS 選擇器官方指南](https://developer.mozilla.org/zh-TW/docs/Web/CSS/CSS_Selectors)
- [XPath 語法參考](https://developer.mozilla.org/zh-TW/docs/Web/XPath)
- [Playwright 定位器策略](https://playwright.dev/python/docs/locators)

### C. 常見錯誤與解決方案
- [Playwright 疑難排解指南](https://playwright.dev/python/docs/troubleshooting)
- [常見問題 FAQ](https://playwright.dev/python/docs/intro#known-issues)
- [調試技巧](https://playwright.dev/python/docs/debug)

### D. 學習資源推薦
#### 官方資源
- [Playwright 官方網站](https://playwright.dev/)
- [Python 版本文件](https://playwright.dev/python)
- [快速入門教學](https://playwright.dev/python/docs/intro)
- [範例程式碼庫](https://github.com/microsoft/playwright-python/tree/main/examples)
- [官方 YouTube 頻道](https://www.youtube.com/channel/UC46Zj8pDH5tDosqm1gd7WTg)

#### 相關技術文件
- [W3C WebDriver 規範](https://w3c.github.io/webdriver/)
- [Chromium DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [Firefox Remote Debugging](https://firefox-source-docs.mozilla.org/devtools/backend/protocol.html)

#### 社群資源
- [GitHub Issues](https://github.com/microsoft/playwright-python/issues)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/playwright)
- [Discord 社群](https://discord.gg/playwright-840196519495999508)
- [Reddit 討論區](https://www.reddit.com/r/playwright/)

#### 進階學習
- [測試最佳實踐](https://playwright.dev/python/docs/best-practices)
- [CI/CD 整合指南](https://playwright.dev/python/docs/ci)
- [Docker 部署](https://playwright.dev/python/docs/docker)
- [效能調優指南](https://playwright.dev/python/docs/browsers#performance)

---

## 學習建議
1. **循序漸進**：從第一章開始，按照章節順序學習
2. **實際操作**：每章節都建議實際執行程式碼
3. **修改練習**：嘗試修改範例程式碼，理解每個參數的作用
4. **實戰專案**：每完成一章，立即完成該章對應的真實網站專案
5. **自主練習**：實作自己的小專案，應用所學技能

## 學習路徑建議

### 初學者路徑（1-2 週）
1. 第 01 章：Playwright 簡介（環境安裝）
2. 第 02 章：基礎操作（啟動瀏覽器、頁面導航）
3. 第 03 章：元素定位（CSS 選擇器、內建定位器）
4. 第 05 章：資料擷取（獲取文字、屬性）
5. **專案二：維基百科搜尋器**（入門實戰）

### 進階路徑（2-3 週）
1. 第 04 章：等待與同步
2. 第 06 章：進階互動
3. 第 10 章：登入與 Cookie 處理
4. **專案三：台灣高鐵時刻表查詢**（進階實戰）
5. **專案一：PTT 熱門文章爬蟲**（綜合應用）

### 專業路徑（3-4 週）
1. 第 07 章：多頁面與框架處理
2. 第 09 章：網路請求與回應
3. 第 11 章：反爬蟲對策
4. 第 12 章：效能優化
5. 第 13 章：實戰專案（完整應用）

## 前置知識
- 基本 Python 語法（變數、迴圈、函式）
- 基礎 HTML 結構認識
- 命令列操作基礎
- 不需要網頁開發經驗

## 環境需求
- Python 3.8 或以上版本
- 穩定的網路連線
- 至少 2GB 可用硬碟空間（用於瀏覽器驅動）
- 建議使用 VS Code 或 PyCharm 等 IDE

## 快速開始

### 1. 安裝 Playwright
```bash
pip install playwright
playwright install chromium
```

### 2. 執行第一個範例
```bash
uv run python playwright/課程章節/第01章_Playwright簡介/real_example.py
```

### 3. 嘗試實戰專案
```bash
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py
```

## 課程特色
- ✅ 專為 Python 初學者設計
- ✅ 完整的章節式教學
- ✅ 12 個章節對應的真實網站實戰專案
- ✅ 豐富的程式碼範例
- ✅ 詳細的中文說明文件
- ✅ 循序漸進的學習路徑
