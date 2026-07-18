# 專案二：維基百科關鍵字搜尋器 🔍

## 🎯 專案目標

學習使用 Playwright 自動化搜尋維基百科，擷取多個關鍵字的結構化資訊，並儲存為 JSON 格式。

### 學習重點
- ✅ 表單操作與搜尋功能
- ✅ 結構化內容擷取（摘要、分類、資訊框）
- ✅ 多頁面資料整合
- ✅ JSON 資料儲存與讀取
- ✅ 進階元素定位技巧
- ✅ 為 Crawl4AI 打基礎：複雜結構解析

---

## 📋 功能說明

這個搜尋器可以：
1. 自動搜尋維基百科的多個關鍵字
2. 擷取每個條目的：
   - 標題
   - 摘要（前兩段落）
   - 分類標籤
   - 資訊框（Infobox）資料
   - 外部連結數量
   - 條目網址
3. 將資料整理為結構化 JSON 格式
4. 支援批次查詢與結果匯出

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
02_維基百科搜尋器/
├── README.md              # 專案說明文件
├── wiki_searcher.py       # 主程式
├── requirements.txt       # 套件需求
└── output/                # 輸出資料夾（執行後自動建立）
    ├── wiki_results.json  # 搜尋結果
    └── wiki_summary.txt   # 文字摘要報告
```

---

## 🚀 使用方法

### 1. 基本執行

```bash
# 執行搜尋器（預設搜尋 Python、Playwright、Web Scraping）
python wiki_searcher.py
```

### 2. 自訂搜尋關鍵字

```python
# 在 main() 函式中修改關鍵字列表
keywords = [
    "人工智慧",
    "機器學習",
    "深度學習"
]
```

### 3. 單一關鍵字查詢

```python
# 直接呼叫函式搜尋單一條目
result = search_wiki_keyword("台灣", language="zh")
print(result["summary"])
```

### 4. 切換語言

```python
# 在 main() 函式中修改
wiki_language = "en"  # 改為英文維基百科
```

---

## 📖 程式碼解析

### 程式架構說明

本專案使用**函式導向設計**，適合 Python 初學者理解。主要包含 8 個函式：

#### 核心搜尋函式

##### 1️⃣ `search_wiki_keyword()` - 搜尋單一關鍵字
```python
def search_wiki_keyword(keyword, language="zh", headless=False):
    """在維基百科搜尋單一關鍵字"""
    # 步驟 1-5: 開啟瀏覽器、搜尋、檢查結果
    # 步驟 6-10: 擷取標題、摘要、分類、資訊框、統計
    return result  # 返回字典
```

##### 2️⃣ `search_multiple_keywords()` - 批次搜尋
```python
def search_multiple_keywords(keywords, language="zh", headless=False):
    """批次搜尋多個關鍵字"""
    results = []
    for keyword in keywords:
        result = search_wiki_keyword(keyword, language, headless)
        if result:
            results.append(result)
    return results
```

#### 資料擷取函式

##### 3️⃣ `extract_summary()` - 擷取摘要
```python
def extract_summary(page):
    """擷取維基百科條目的摘要段落"""
    # 取得前兩個有實質內容的段落
```

##### 4️⃣ `extract_categories()` - 擷取分類
```python
def extract_categories(page):
    """擷取維基百科條目的分類標籤"""
    # 從頁面底部取得分類
```

##### 5️⃣ `extract_infobox()` - 擷取資訊框
```python
def extract_infobox(page):
    """擷取維基百科條目的資訊框資料"""
    # 解析 table.infobox 的 th 和 td
```

##### 6️⃣ `extract_statistics()` - 擷取統計
```python
def extract_statistics(page):
    """擷取參考資料、章節、外部連結數量"""
```

#### 資料儲存函式

##### 7️⃣ `save_to_json()` - 儲存 JSON
```python
def save_to_json(results, language="zh", filename=None):
    """將搜尋結果儲存為 JSON 檔案"""
```

##### 8️⃣ `save_summary_report()` - 產生報告
```python
def save_summary_report(results, filename=None):
    """產生並儲存文字摘要報告"""
```

### 為什麼使用函式而不是類別？

對於 Python 初學者：
- ✅ **模組化設計**：每個函式獨立完成一個任務
- ✅ **容易重組**：可以自由組合不同函式
- ✅ **降低學習門檻**：專注在邏輯流程，不需要理解物件導向概念
- ✅ **方便測試**：可以單獨測試每個函式

---

## 🎓 學習步驟建議

### 第一階段：理解搜尋流程（20 分鐘）
1. 手動在維基百科搜尋一個關鍵字
2. 觀察網頁結構（開啟開發者工具 F12）
3. 找出摘要、分類、資訊框的 HTML 結構
4. 對照程式碼中的選擇器

### 第二階段：執行與測試（30 分鐘）
1. 執行程式，觀察自動搜尋過程
2. 檢查生成的 JSON 檔案
3. 嘗試搜尋不同類型的條目：
   - 人物：`"比爾·蓋茲"`
   - 地點：`"台北101"`
   - 概念：`"量子計算"`
   - 事件：`"2024年巴黎奧運"`

### 第三階段：功能擴展（50 分鐘）
挑戰任務：
- [ ] 增加「參考資料數量」欄位
- [ ] 擷取條目的圖片網址
- [ ] 增加語言切換功能（中文/英文維基）
- [ ] 如果搜尋結果是「消歧義頁面」，列出所有選項
- [ ] 加入「相關條目」的連結擷取

---

## ⚠️ 注意事項

### 法律與道德
- ✅ **尊重版權**：維基百科採用 CC BY-SA 授權，可以使用但需標示來源
- ✅ **合理使用**：避免短時間大量請求
- ✅ **遵守 robots.txt**：參考 [維基百科爬蟲政策](https://meta.wikimedia.org/wiki/User-Agent_policy)

### 常見問題

**Q1: 為什麼有些條目找不到資訊框？**
- A: 不是所有條目都有資訊框，程式已加入檢查：
  ```python
  if page.locator("table.infobox").is_visible():
      # 擷取資訊框
  else:
      infobox = {}  # 空字典
  ```

**Q2: 如何處理搜尋不到的關鍵字？**
- A: 檢查標題是否包含「查無此頁」：
  ```python
  title = page.locator("h1").inner_text()
  if "查無" in title or "does not exist" in title:
      return None  # 表示找不到
  ```

**Q3: JSON 檔案太大怎麼辦？**
- A: 可以分批儲存或壓縮：
  ```python
  import gzip
  import json

  with gzip.open("results.json.gz", "wt", encoding="utf-8") as f:
      json.dump(data, f)
  ```

**Q4: 如何搜尋英文維基百科？**
- A: 修改 base_url：
  ```python
  self.base_url = "https://en.wikipedia.org"
  ```

---

## 🔗 相關資源

- [維基百科首頁](https://zh.wikipedia.org/)
- [維基百科 API 文件](https://www.mediawiki.org/wiki/API:Main_page)
- [Playwright Locators 進階用法](https://playwright.dev/python/docs/locators)
- [Python JSON 模組教學](https://docs.python.org/zh-tw/3/library/json.html)

---

## 📈 進階擴展

完成基礎功能後，可以嘗試：

### 1. 建立知識圖譜
```python
# 擷取「另見」章節的相關連結
related_links = page.locator("div#另見 + ul a").all()
for link in related_links:
    related_title = link.inner_text()
    # 繼續搜尋相關條目，建立關聯圖
```

### 2. 多語言比對
```python
# 比對中文和英文維基的同一條目
zh_result = search_wiki("https://zh.wikipedia.org", "Python")
en_result = search_wiki("https://en.wikipedia.org", "Python")
# 分析兩者的差異
```

### 3. 自動產生摘要報告
```python
# 使用 AI 或自然語言處理產生摘要
from transformers import pipeline

summarizer = pipeline("summarization")
short_summary = summarizer(long_text, max_length=130)
```

### 4. 建立命令列介面（CLI）
```python
import argparse

parser = argparse.ArgumentParser(description='維基百科搜尋器')
parser.add_argument('keywords', nargs='+', help='要搜尋的關鍵字')
parser.add_argument('--lang', default='zh', help='語言（zh/en）')
args = parser.parse_args()

# 執行：python wiki_searcher.py Python Playwright --lang en
```

---

## 🔄 與專案一的差異

| 特性 | 專案一（PTT爬蟲） | 專案二（維基搜尋器） |
|------|------------------|---------------------|
| **資料來源** | 列表頁面 | 搜尋結果 + 內容頁 |
| **互動方式** | 簡單導航 | 表單填寫 + 搜尋 |
| **資料結構** | 扁平（標題、作者） | 巢狀（摘要、資訊框） |
| **儲存格式** | CSV（表格） | JSON（樹狀） |
| **難度** | ⭐⭐ | ⭐⭐⭐ |

---

## ✅ 學習檢核表

完成本專案後，你應該能夠：

- [ ] 使用 Playwright 操作搜尋表單
- [ ] 擷取複雜的巢狀結構資料
- [ ] 處理條件判斷（資訊框存在與否）
- [ ] 將資料儲存為 JSON 格式
- [ ] 批次處理多個查詢
- [ ] 建立資料匯總與統計功能
- [ ] 理解結構化資料的重要性

---

## 🎯 專案整合建議

完成兩個專案後，可以嘗試整合應用：

**範例：PTT 新聞條目自動查詢器**
1. 從 PTT 爬取新聞標題（專案一）
2. 擷取標題中的關鍵實體（人名、地名）
3. 自動在維基百科查詢這些關鍵字（專案二）
4. 產生「新聞背景知識報告」

這樣就能完整實踐從資料擷取到知識整合的流程！

---

[← 上一個專案：PTT 爬蟲](../01_PTT熱門文章爬蟲/README.md) | [返回課程目錄](../../README.md)
