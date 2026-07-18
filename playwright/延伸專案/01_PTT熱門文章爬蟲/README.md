# 專案一：PTT 熱門文章爬蟲 📰

## 🎯 專案目標

學習使用 Playwright 爬取 PTT (批踢踢) 的熱門文章，並將資料儲存為 CSV 檔案。

### 學習重點
- ✅ 網頁導航與頁面載入等待
- ✅ 列表資料的批量擷取
- ✅ CSS 選擇器的實際應用
- ✅ 資料儲存為 CSV 格式
- ✅ 基本的錯誤處理
- ✅ 為 Crawl4AI 打基礎：文字內容擷取

---

## 📋 功能說明

這個爬蟲可以：
1. 自動開啟 PTT 網頁版
2. 爬取熱門看板（如 Gossiping 八卦版）的文章列表
3. 擷取每篇文章的：
   - 推文數（人氣）
   - 文章標題
   - 作者
   - 發文日期
4. 將資料儲存為 CSV 檔案，方便後續分析

---

## 🔧 環境需求

```bash
# 確認 Python 版本（需要 3.8 以上）
python --version

# 安裝 Playwright
pip install playwright

# 下載瀏覽器驅動
playwright install chromium
```

---

## 📂 專案結構

```
01_PTT熱門文章爬蟲/
├── README.md           # 專案說明文件
├── ptt_scraper.py      # 主程式
├── requirements.txt    # 套件需求
└── output/             # 輸出資料夾（執行後自動建立）
    └── ptt_articles.csv
```

---

## 🚀 使用方法

### 1. 基本執行

```bash
# 執行爬蟲（預設爬取 Gossiping 看板前 20 筆）
python ptt_scraper.py
```

### 2. 指定看板和數量

```python
# 在 main() 函式中修改參數
board_name = "Tech_Job"    # 改成科技職場板
article_count = 50         # 爬取 50 篇文章
```

### 3. 單獨使用某個函式

```python
# 只爬取，不儲存
articles = scrape_ptt_articles(board="Beauty", max_articles=10)

# 只顯示統計
show_statistics(articles)

# 只儲存 CSV
save_to_csv(articles, board="Beauty")
```

---

## 📖 程式碼解析

### 程式架構說明

本專案使用**函式導向設計**，適合 Python 初學者理解。主要包含 4 個函式：

#### 1️⃣ `scrape_ptt_articles()` - 爬取文章
```python
def scrape_ptt_articles(board="Gossiping", max_articles=20, headless=False):
    """爬取 PTT 看板的文章列表"""
    # 步驟 1: 啟動瀏覽器
    # 步驟 2: 前往看板頁面
    # 步驟 3: 處理 18 歲確認頁面
    # 步驟 4: 等待文章列表載入
    # 步驟 5: 擷取文章資料
    # 步驟 6: 關閉瀏覽器
    return articles_data  # 返回文章列表
```

#### 2️⃣ `save_to_csv()` - 儲存 CSV
```python
def save_to_csv(articles_data, board="Gossiping", filename=None):
    """將文章資料儲存為 CSV 檔案"""
    # 使用 csv.DictWriter 寫入檔案
    # 自動產生時間戳記檔名
```

#### 3️⃣ `show_statistics()` - 顯示統計
```python
def show_statistics(articles_data):
    """顯示文章的統計資訊"""
    # 計算平均推文數
    # 找出熱門文章 TOP 3
```

#### 4️⃣ `main()` - 主程式
```python
def main():
    """執行完整的爬蟲流程"""
    articles = scrape_ptt_articles(board="Gossiping", max_articles=20)
    show_statistics(articles)
    save_to_csv(articles)
```

### 為什麼使用函式而不是類別？

對於 Python 初學者：
- ✅ **更直觀**：每個函式做一件事，容易理解
- ✅ **易於修改**：想改哪個功能就改哪個函式
- ✅ **方便測試**：可以單獨執行每個函式
- ✅ **減少概念負擔**：不需要理解 `self`、`__init__` 等

---

## 🎓 學習步驟建議

### 第一階段：理解程式結構（30 分鐘）
1. 閱讀完整程式碼
2. 理解每個函式的用途
3. 找出 CSS 選擇器對應的網頁元素

### 第二階段：實際執行（20 分鐘）
1. 執行程式，觀察瀏覽器自動操作
2. 檢查生成的 CSV 檔案
3. 嘗試修改看板名稱

### 第三階段：程式改造（40 分鐘）
挑戰任務：
- [ ] 修改程式，增加「網址」欄位
- [ ] 只抓取推文數 > 10 的文章
- [ ] 新增爬取多個看板的功能
- [ ] 加入進度條顯示（提示：使用 `tqdm` 套件）

---

## ⚠️ 注意事項

### 法律與道德
- ✅ **合理使用**：PTT 是公開論壇，但請適量爬取
- ✅ **尊重流量**：不要短時間內大量請求，避免造成伺服器負擔
- ✅ **遵守規範**：參考 [PTT 使用者條款](https://www.ptt.cc/about.html)

### 常見問題

**Q1: 為什麼會出現「找不到元素」的錯誤？**
- A: PTT 網頁可能載入較慢，增加等待時間：
  ```python
  page.wait_for_selector("div.r-ent", timeout=10000)
  ```

**Q2: 為什麼 CSV 檔案中文亂碼？**
- A: 使用 `utf-8-sig` 編碼（已在程式中設定）：
  ```python
  open("file.csv", "w", encoding="utf-8-sig")
  ```

**Q3: 如何爬取更多頁文章？**
- A: 需要處理分頁，點擊「上頁」按鈕：
  ```python
  page.click("a:has-text('‹ 上頁')")
  page.wait_for_load_state("networkidle")
  ```

---

## 🔗 相關資源

- [PTT 網頁版](https://www.ptt.cc/bbs/index.html)
- [Playwright 定位器教學](https://playwright.dev/python/docs/locators)
- [CSS 選擇器速查表](https://www.w3schools.com/cssref/css_selectors.php)
- [Python CSV 模組文件](https://docs.python.org/zh-tw/3/library/csv.html)

---

## 📈 進階擴展

完成基礎功能後，可以嘗試：

1. **增加篩選功能**
   - 只抓特定關鍵字的文章
   - 篩選特定時間區間

2. **資料分析**
   - 統計最熱門的文章類型
   - 分析發文時間分布

3. **視覺化呈現**
   - 使用 `matplotlib` 繪製推文數分布圖
   - 製作文字雲（WordCloud）

4. **自動化排程**
   - 使用 `schedule` 套件定時執行
   - 每日自動爬取並發送通知

---

## ✅ 學習檢核表

完成本專案後，你應該能夠：

- [ ] 使用 Playwright 開啟網頁並導航
- [ ] 使用 CSS 選擇器定位元素
- [ ] 批量擷取列表資料
- [ ] 處理網頁的互動操作（如按鈕點擊）
- [ ] 將資料儲存為 CSV 格式
- [ ] 基本的錯誤處理與除錯

---

[← 返回課程目錄](../../README.md) | [下一個專案：維基百科搜尋器 →](../02_維基百科搜尋器/README.md)
