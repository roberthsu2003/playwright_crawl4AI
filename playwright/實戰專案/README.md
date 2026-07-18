# 第十三章：真實網站實戰專案

這一章不再使用 `example.com` 式的假網站。每完成一章課程，就做一個可以真正執行、看得到成果的小專案。

> 外部網站可能改版。若選擇器失效，先用瀏覽器開發者工具觀察新結構，再修正程式；這也是實戰的一部分。

## 學習地圖

| 完成章節 | 實戰專案 | 真實網站 | 主要功能 | 成果 |
|---|---|---|---|---|
| 01 簡介 | [01 網站健康檢查](專案01_網站健康檢查/README.md) | Example Domain | 啟動瀏覽器、導航、標題、截圖 | `homepage.png` |
| 02 基礎操作 | [02 線上表單自動填寫](專案02_線上表單自動填寫/README.md) | Selenium Web Form | fill、select、check、click | 表單送出驗證 |
| 03 元素定位 | [03 購物網站元素定位](專案03_購物網站元素定位/README.md) | SauceDemo | role、label、test id、CSS、filter | 購物車摘要 |
| 04 等待與同步 | [04 動態內容等待](專案04_動態內容等待/README.md) | The Internet | 自動等待、明確等待、條件等待 | `Hello World!` |
| 05 資料擷取 | [05 線上書店資料擷取](專案05_線上書店資料擷取/README.md) | Books to Scrape | 多元素、文字、屬性、分頁 | `books.csv` |
| 06 進階互動 | [06 進階互動巡檢](專案06_進階互動巡檢/README.md) | The Internet | hover、鍵盤、滾動、上傳、下載 | 下載檔案 |
| 07 多頁面與框架 | [07 多視窗與 iframe](專案07_多視窗與iframe/README.md) | The Internet | popup、alert、iframe | 三項互動結果 |
| 08 截圖與錄影 | [08 網頁存證報告](專案08_網頁存證報告/README.md) | Wikipedia | 整頁/元素/區域截圖、錄影、PDF | `output/` 報告檔 |
| 09 網路請求與回應 | [09 API 監聽與 Mock](專案09_API監聽與Mock/README.md) | JSONPlaceholder | request/response、expect_response、route | 真實與 Mock JSON |
| 10 登入與 Cookie | [10 登入狀態保存](專案10_登入狀態保存/README.md) | SauceDemo | 登入、Cookie、localStorage、storage state | `auth.json` |
| 11 反爬蟲對策 | [11 禮貌爬蟲](專案11_禮貌爬蟲/README.md) | HTTPBingo | User-Agent、locale、viewport、限速 | 瀏覽器標頭報告 |
| 12 效能優化 | [12 平行爬取優化](專案12_平行爬取優化/README.md) | Books to Scrape | async、平行 context、擋資源、重試 | `books_parallel.json` |

## 快速開始

請在專案根目錄執行：

```bash
uv sync
uv run playwright install chromium
uv run python playwright/實戰專案/專案01_網站健康檢查/main.py
```

每個 `main.py` 都可獨立執行，成果會放在該專案的 `output/` 目錄。
若不使用 uv，也可以改用 `pip install -r playwright/實戰專案/requirements.txt`，再執行 `playwright install chromium`。

## AI 介面升級

完成核心專案後，可以用 tkinter、PySide6/PyQtGraph、Gradio、Dash、Flask、Streamlit 或 FastAPI 將它升級為桌面 App、儀表板、網站或 API。

[開啟「AI 介面設計 Prompt 手冊」—包含 12 份可直接複製的完整 Prompt →](AI介面設計Prompt.md)

## 教學流程（每個專案約 60～90 分鐘）

1. **先手動操作**：學生先用瀏覽器完成一次任務。
2. **讀懂半成品**：教師刪除一至三個關鍵區塊，讓學生補完。
3. **執行與觀察**：先用 `headless=False` 觀察，成功後再改為 `True`。
4. **驗收成果**：不只看程式沒有錯誤，還要檢查輸出檔與頁面狀態。
5. **延伸挑戰**：更換資料、增加欄位、加入錯誤處理或比較效能。

## 共同驗收標準

- [ ] 程式能從專案根目錄執行。
- [ ] 元素定位優先使用 role、label 或穩定屬性，不依賴過長 CSS/XPath。
- [ ] 不以長時間 `wait_for_timeout()` 代替正確等待。
- [ ] 使用 `try/finally` 或 context manager 確保瀏覽器關閉。
- [ ] 不把真實密碼、Cookie 或私人資料提交到 Git。
- [ ] 對外部網站控制速度，不嘗試繞過 CAPTCHA 或存取限制。

## 延伸挑戰

| 專案 | 挑戰任務 |
|---|---|
| 01 | 加入 Firefox 與 WebKit，輸出三種瀏覽器比較表。 |
| 02 | 加入日期、顏色、滑桿與檔案欄位。 |
| 03 | 只將價格低於 20 美元的商品加入購物車。 |
| 04 | 刻意把 timeout 調短，截圖記錄失敗畫面。 |
| 05 | 可指定類別與頁數，並輸出平均價格。 |
| 06 | 加入 drag and drop、雙擊與右鍵選單。 |
| 07 | 加入 confirm 與 prompt，比較 accept/dismiss。 |
| 08 | 建立含時間戳的檔名，並定時產生報告。 |
| 09 | Mock 404 與 500，驗證前端錯誤畫面。 |
| 10 | 檢查狀態檔過期時自動重新登入。 |
| 11 | 讀取 robots.txt，為不同網域設定不同間隔。 |
| 12 | 實測 1、3、5 個 context 的時間與記憶體差異。 |

## 網站使用原則

SauceDemo、The Internet、Books to Scrape、Quotes to Scrape、Selenium Web Form、JSONPlaceholder 與 HTTPBingo 是公開測試/練習服務。Wikipedia 為公開內容網站。即使是測試站，仍應低頻率執行；不要將這些範例改成對社群網站自動發文、繞過驗證或大量請求。

[ ← 返回主目錄](../README.md)
