# 04_毛寶企業 多賣場產品與競品價格每日監控系統 (Playwright Async)

這是一個專為產品經理（PM）設計的 **Playwright 非同步 (Async API)** 自動化多賣場價格監控與競品追蹤工具。

---

## 📌 專案背景與情境故事

假設你是**毛寶企業（Maobao）**的產品經理（PM），毛寶旗下擁有多款知名家庭清潔產品（如貼身衣物手洗精、冷洗精、小蘇打洗碗精、洗衣槽去污劑等），並上架在台灣各大主流電商賣場（如 PChome 24h、momo購物網、Yahoo購物中心等）。

作為 PM，你需要：
1. **跨賣場每日監控**：即時掌握毛寶 5 大主力產品在 **PChome 24h購物**、**momo購物網** 與 **Yahoo購物中心** 上的最新上架價格與促銷商品標題。
2. **競品多賣場追蹤**：同時追蹤各大競爭品牌（如白蘭、妙管家、南僑水晶、橘子工坊、威猛先生）在各大賣場的商品規格與價格。
3. **無輸出誤導之價格比較**：由於各品牌與商品在不同賣場的包裝規格/單位差異較大（例如 1000g vs 300gX12盒 vs 4000g），本系統專注於客觀列出各大賣場即時價格，不進行直接相減或百分比之價格優劣計算。
4. **高效平行併發抓取**：利用 **Playwright 非同步平行併發 (Async Concurrent Crawling)** 技術，同時跨品類、跨賣場查詢數十個商品，將抓取時間縮短至僅需 3~5 秒！

---

## 🎯 監控之 5 大毛寶主力產品與競品清單

| 編號 | 品類 | 毛寶本家主力產品 | 對應競品品牌與產品 |
| :---: | :--- | :--- | :--- |
| **P001** | **貼身衣物手洗精** | 毛寶 貼身衣物手洗精 1000g | • 白蘭 貼身衣物手洗精<br>• 妙管家 貼身衣物手洗精 |
| **P002** | **洗衣槽清潔劑** | 毛寶 洗衣槽去污劑 | • 妙管家 洗衣槽專用清潔劑<br>• 威猛先生 洗衣槽清潔劑 |
| **P003** | **洗碗精** | 毛寶 小蘇打洗碗精 | • 南僑水晶 小蘇打洗碗精<br>• 橘子工坊 洗碗精 |
| **P004** | **冷洗精** | 毛寶 天然冷洗精 | • 白蘭 冷洗精<br>• 妙管家 冷洗精 |
| **P005** | **濃縮洗衣精** | 毛寶 PM2.5防霾抗菌濃縮洗衣精 | • 白蘭 濃縮洗衣精<br>• 妙管家 濃縮洗衣精 |

---

## 🏬 監控之三大電商賣場平台

1. **PChome 24h購物** (使用 API 非同步抓取，反應極快)
2. **momo購物網** (使用 Playwright DOM 解析)
3. **Yahoo購物中心** (使用 Playwright DOM 解析)

---

## ⚡ 同步 (Sync) vs 非同步 (Async) 比較

| 特性 | 同步 Playwright (`sync_api`) | 非同步 Playwright (`async_api`) |
| :--- | :--- | :--- |
| **執行方式** | 順序執行 (Sequential)，一個賣場與商品查完才查下一個 | 平行併發 (Concurrent)，跨賣場、跨商品同時發起非同步任務 |
| **資源利用** | CPU 與網路大多時間在等待網頁回應 (I/O Bound) | 善用 `asyncio` Event Loop，等待 I/O 時自動切換執行其他任務 |
| **抓取速度** | 抓取 5 大品類跨 3 大賣場需約 40~90 秒 | 抓取所有跨賣場商品僅需 **3~5 秒**（速度提升 10 倍以上） |
| **適用情境** | 單一簡單頁面操作、線性教學範例 | **大規模資料爬取、多商品價格監控、多賣場併發追蹤** |

---

## 🛠️ 執行前準備與步驟

### 1. 移動至專案目錄

```bash
cd "playwright/延伸專案/04_毛寶與競品價格監控_async"
```

### 2. 執行監控程式

使用 `uv` 執行：
```bash
uv run main.py
```
*(程式將自動開啟非同步瀏覽器分頁，平行並發查詢各大賣場商品價格！)*

---

## 📄 輸出成果與報表說明

執行完成後，系統會自動在終端機輸出格式化報表，並匯出兩種格式的報告：

### 1. 終端機跨賣場價格監控報表 (Console Table)
清楚列出各品類、品牌在三大賣場的搜尋商品標題與售價：

```text
================================================================================
毛寶企業 (Maobao) 多賣場產品與競品價格每日監控系統 [Playwright Async版]
================================================================================
📦 載入設定完成！監控 5 大品類，跨賣場：PChome 24h, momo購物網, Yahoo購物中心...

🚀 開始平行併發查詢品類：【貼身衣物手洗精】跨賣場數據...
...
✓ 所有品類跨賣場抓取完成！總耗時僅：3.53 秒 (非同步併發加速)
================================================================================

📊 【毛寶 vs 競品 多賣場即時價格監控報表】
註：因各商品包裝規格與單位不同，本報表僅呈現原始監控售價，不進行價差比較與優勢計算
------------------------------------------------------------------------------------------
品類           品牌       賣場           搜尋商品標題                           售價
------------------------------------------------------------------------------------------
貼身衣物手洗精      [毛寶]     PChome 24h   貼身衣物手洗精-3D SOUSOU(1000g)         $109
                      momo購物網      【毛寶】貼身衣物手洗精-玫瑰-SOUSOU_onpack(1.. $109
                      Yahoo購物中心    毛寶 貼身衣物手洗精1000g(果漾西西里)           $99
             [白蘭]     PChome 24h   未找到相關商品                          未找到
                      momo購物網      【毛寶】貼身衣物手洗精-3D-SOUSOU_onpack(1.. $109
                      Yahoo購物中心    白蘭 酵素除菌手洗精 520G                  $79
...
```

### 2. Markdown 競品日報 (`price_report.md`)
自動產生標準 GFM (GitHub Flavored Markdown，即支援表格、自動連結與任務清單的 Markdown 語法) 表格，包含商品連結、賣場標示，方便 PM 直接複製發送 Email 或匯入 Notion/Slack 報告。

### 3. JSON 詳細數據 (`price_report.json`)
完整保留時間戳記、耗時與各賣場原始抓取資料，利於後續整合至資料庫或前端 Dashboard 儀表板。

---

## 💡 程式碼核心亮點說明

### 1. 非同步併發跨賣場抓取 (`asyncio.gather`)
```python
# 同時在 PChome 24h、momo購物網、Yahoo購物中心平行併發抓取
stores_tasks = [
    fetch_pchome(context, keyword),
    fetch_momo(context, keyword),
    fetch_yahoo(context, keyword)
]
store_results = await asyncio.gather(*stores_tasks)
```

### 2. 結構化抽離 (`products_config.json`)
將監控賣場清單與監控商品關鍵字獨立寫在 `products_config.json` 中，未來的 PM 只需要修改 JSON 即可增加監控賣場或品項，無須修改 `main.py` 程式碼！

---

## 🔑 關鍵技術 (Key Technical Concepts)

1. **Playwright Async API & `asyncio` 協程 (Coroutines)**：
   - 使用 `async with async_playwright()` 與 `await` 進行非同步網頁操作。
   - 配合 `asyncio.gather(*tasks)` 實現跨品類、跨賣場的多維度平行併發抓取 (Concurrent Fetching)，大幅減少 I/O 等待時間。

2. **混合式抓取策略 (Hybrid Scraping Approach)**：
   - **API 直接請求 (API Direct Fetching)**：針對提供公開搜尋 API 的平台（如 PChome 24h 的 `ecshweb.pchome.com.tw`），優先使用 `context.request.get()` 發送高效率 HTTP 請求。
   - **Playwright DOM 解析 (Headless Page Crawling)**：針對渲染複雜的 SPA / 動態電商平台（如 momo購物網、Yahoo購物中心），使用非同步 Page 載入與 Locator 提取。

3. **頁面載入優化與 Event 等待控制**：
   - 避免使用 `wait_until="networkidle"` 導致現代電商平台（包含背景輪詢與廣告追蹤）發生超時拖慢問題。
   - 改用 `wait_until="domcontentloaded"` 搭配精準 Locator 等待，兼顧穩定度與效能。

4. **組態驅動設計 (Configuration-Driven Architecture)**：
   - 商品、品類與賣場定義全面抽離至 `products_config.json`，實現無須修改程式碼即可動態擴充監控項目的架構。

5. **正則表達式數據清洗 (Regex Data Sanitization)**：
   - 透過 `re.sub(r"[^\d]", "", price_text)` 從混有貨幣符號、折價券標籤或促銷字眼中精確提取整數售價。

---

## ⚠️ 注意事項 (Important Considerations & Best Practices)

1. **避免數值化價格比較（單位不一致問題）**：
   - 各品牌或不同賣場上架的商品規格與包裝（如 1000g 單瓶 vs 300gX12盒箱購 vs 4000g補充桶）單位落差極大。
   - **請勿**直接以 `售價 A - 售價 B` 進行價差計算或百分比比較，避免產出具誤導性的商業分析報告。

2. **電商 DOM 選擇器 (Selectors) 的維護與更新**：
   - 電商平台（特別是 momo 與 Yahoo）會定期更新 DOM 結構或 CSS class。若搜尋結果顯示「未找到相關商品」，需即時檢查並更新 `main.py` 中的 Locator 選擇器。

3. **頻率控管與反爬蟲偽裝**：
   - 雖然非同步併發速度極快，但在大規模擴充監控商品時，建議適當設定 User-Agent 與請求間隔，避免引發電商平台的防爬蟲機制或 IP 封鎖。

4. **搜尋關鍵字的精準度**：
   - 關鍵字若過於寬泛（如僅搜尋「毛寶」），容易抓到非目標商品；若過於嚴格，可能在某些賣場查無結果。建議在 `products_config.json` 中配置經過測試的通用商品名稱。

5. **例外處理與防護機制 (Graceful Exception Handling)**：
   - 單一賣場連線超時或商品下架不應導致整體程式中斷。各抓取模組皆需包含 `try-except` 容錯，確保報表能穩定匯出。

---

## 相關資源

- [Playwright Async API 官方文件](https://playwright.dev/python/docs/api/class-playwright)
- [Python asyncio 官方教學](https://docs.python.org/zh-tw/3/library/asyncio.html)
- [毛寶企業官網](https://www.maobao.com.tw/)
