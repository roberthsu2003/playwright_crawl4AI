# Crawl4AI JsonCssExtractionStrategy Schema 完整教學

> 本文件從零開始教你如何使用 `JsonCssExtractionStrategy` 的 Schema 定義，讓你能夠精準地從 HTML 中提取結構化資料。

---

## 目錄

1. [什麼是 Schema？](#1-什麼是-schema)
2. [基本架構](#2-基本架構)
3. [欄位類型 (type) 完整說明](#3-欄位類型-type-完整說明)
4. [實戰範例：從簡單到複雜](#4-實戰範例從簡單到複雜)
5. [常見錯誤與解決方案](#5-常見錯誤與解決方案)
6. [速查表](#6-速查表)

---

## 1. 什麼是 Schema？

Schema（結構描述）就像是一份「資料擷取說明書」，告訴爬蟲：

- **去哪裡找** → 使用 CSS 選擇器 (selector)
- **找什麼** → 定義欄位名稱 (name)
- **怎麼處理** → 指定資料類型 (type)

### 簡單比喻

想像你要從一本書中摘錄筆記：

| 你的動作 | Schema 對應 |
|---------|------------|
| 「找出所有章節標題」 | `baseSelector: ".chapter"` |
| 「記下標題文字」 | `selector: ".title", type: "text"` |
| 「記下頁碼」 | `selector: ".page-num", type: "text"` |

---

## 2. 基本架構

### 2.1 最小可用 Schema

```python
schema = {
    "name": "資料集名稱",           # 幫這組資料取個名字
    "baseSelector": ".item",        # 重複區塊的 CSS 選擇器
    "fields": [                     # 要擷取的欄位陣列
        {
            "name": "欄位名稱",
            "selector": ".class-name",
            "type": "text"
        }
    ]
}
```

### 2.2 架構圖解

```
schema
├── name          → 資料集名稱（自訂）
├── baseSelector  → 指向「重複出現的區塊」
└── fields[]      → 欄位定義陣列
    ├── field 1
    │   ├── name      → 欄位名稱（自訂）
    │   ├── selector  → CSS 選擇器（相對於 baseSelector）
    │   └── type      → 資料類型
    ├── field 2
    └── ...
```

### 2.3 重要觀念：baseSelector

`baseSelector` 是整個 Schema 的核心，它決定了「資料的邊界」。

**HTML 範例：**
```html
<div class="product">           <!-- 第一個產品 -->
    <h3 class="name">耳機</h3>
    <span class="price">$100</span>
</div>
<div class="product">           <!-- 第二個產品 -->
    <h3 class="name">手錶</h3>
    <span class="price">$200</span>
</div>
```

**正確設定：**
```python
"baseSelector": ".product"  # ✅ 會找到 2 個產品
```

**錯誤設定：**
```python
"baseSelector": ".name"     # ❌ 會找到 2 個名稱，但無法關聯價格
```

---

## 3. 欄位類型 (type) 完整說明

### 3.1 type: "text" — 純文字

**用途：** 擷取單一元素的文字內容

```python
{
    "name": "標題",
    "selector": ".title",
    "type": "text"
}
```

**HTML：** `<h1 class="title">Hello World</h1>`  
**輸出：** `"標題": "Hello World"`

---

### 3.2 type: "text" + "all": True — 多個純文字（舊方法）

**用途：** 擷取所有匹配元素的文字，回傳陣列

```python
{
    "name": "標籤",
    "selector": ".tag",
    "type": "text",
    "all": True
}
```

**HTML：**
```html
<span class="tag">科技</span>
<span class="tag">生活</span>
```

**輸出：** `"標籤": ["科技", "生活"]`

> ⚠️ **注意：** 這種方式只適合「平行、獨立」的元素，不適合有關聯性的巢狀資料。

---

### 3.3 type: "attribute" — 屬性值

**用途：** 擷取 HTML 屬性（如 href, src, data-* 等）

```python
{
    "name": "連結",
    "selector": "a",
    "type": "attribute",
    "attribute": "href"
}
```

**HTML：** `<a href="https://example.com">點我</a>`  
**輸出：** `"連結": "https://example.com"`

---

### 3.4 type: "html" — 原始 HTML

**用途：** 保留 HTML 標籤結構

```python
{
    "name": "內容",
    "selector": ".content",
    "type": "html"
}
```

**HTML：** `<div class="content"><b>重要</b>訊息</div>`  
**輸出：** `"內容": "<b>重要</b>訊息"`

---

### 3.5 type: "list" — 簡單列表 ⭐

**用途：** 擷取多個同類元素，每個元素可定義子欄位

```python
{
    "name": "特色",
    "selector": ".feature",
    "type": "list",
    "fields": [
        {"name": "內容", "type": "text"}
    ]
}
```

**HTML：**
```html
<li class="feature">防水</li>
<li class="feature">輕量</li>
```

**輸出：**
```json
"特色": [
    {"內容": "防水"},
    {"內容": "輕量"}
]
```

---

### 3.6 type: "nested" — 單一巢狀物件 ⭐

**用途：** 擷取一個包含多個子欄位的區塊

```python
{
    "name": "作者資訊",
    "selector": ".author",
    "type": "nested",
    "fields": [
        {"name": "姓名", "selector": ".name", "type": "text"},
        {"name": "頭像", "selector": "img", "type": "attribute", "attribute": "src"}
    ]
}
```

**HTML：**
```html
<div class="author">
    <span class="name">王小明</span>
    <img src="avatar.jpg">
</div>
```

**輸出：**
```json
"作者資訊": {
    "姓名": "王小明",
    "頭像": "avatar.jpg"
}
```

---

### 3.7 type: "nested_list" — 巢狀物件列表 ⭐⭐⭐（最重要！）

**用途：** 擷取多個結構相同的區塊，每個區塊包含多個子欄位

> 🎯 **這是解決「評論只抓到一個」問題的關鍵！**

```python
{
    "name": "評論",
    "selector": ".review",
    "type": "nested_list",
    "fields": [
        {"name": "評論者", "selector": ".reviewer", "type": "text"},
        {"name": "評分", "selector": ".rating", "type": "text"},
        {"name": "內容", "selector": ".comment", "type": "text"}
    ]
}
```

**HTML：**
```html
<div class="review">
    <span class="reviewer">張三</span>
    <span class="rating">5星</span>
    <p class="comment">很棒！</p>
</div>
<div class="review">
    <span class="reviewer">李四</span>
    <span class="rating">4星</span>
    <p class="comment">還不錯</p>
</div>
```

**輸出：**
```json
"評論": [
    {
        "評論者": "張三",
        "評分": "5星",
        "內容": "很棒！"
    },
    {
        "評論者": "李四",
        "評分": "4星",
        "內容": "還不錯"
    }
]
```

---

## 4. 實戰範例：從簡單到複雜

### 4.1 Level 1：基本商品列表

**目標 HTML：**
```html
<div class="product">
    <h3 class="name">藍牙耳機</h3>
    <span class="price">$999</span>
</div>
<div class="product">
    <h3 class="name">智慧手錶</h3>
    <span class="price">$1999</span>
</div>
```

**Schema：**
```python
schema = {
    "name": "商品",
    "baseSelector": ".product",
    "fields": [
        {"name": "名稱", "selector": ".name", "type": "text"},
        {"name": "價格", "selector": ".price", "type": "text"}
    ]
}
```

---

### 4.2 Level 2：包含列表的商品

**目標 HTML：**
```html
<div class="product">
    <h3 class="name">藍牙耳機</h3>
    <ul class="features">
        <li>降噪</li>
        <li>防水</li>
    </ul>
</div>
```

**Schema：**
```python
schema = {
    "name": "商品",
    "baseSelector": ".product",
    "fields": [
        {"name": "名稱", "selector": ".name", "type": "text"},
        {
            "name": "特色",
            "selector": ".features li",
            "type": "list",
            "fields": [
                {"name": "項目", "type": "text"}
            ]
        }
    ]
}
```

---

### 4.3 Level 3：包含多筆評論的商品（完整範例）

**目標 HTML：**
```html
<div class="product">
    <h3 class="name">藍牙耳機</h3>
    <span class="price">$999</span>
    
    <div class="review">
        <span class="user">小明</span>
        <span class="star">★★★★★</span>
        <p class="text">超讚！</p>
    </div>
    <div class="review">
        <span class="user">小華</span>
        <span class="star">★★★★☆</span>
        <p class="text">不錯用</p>
    </div>
</div>
```

**Schema：**
```python
schema = {
    "name": "商品",
    "baseSelector": ".product",
    "fields": [
        {"name": "名稱", "selector": ".name", "type": "text"},
        {"name": "價格", "selector": ".price", "type": "text"},
        {
            "name": "評論",
            "selector": ".review",
            "type": "nested_list",      # ⭐ 關鍵！
            "fields": [
                {"name": "用戶", "selector": ".user", "type": "text"},
                {"name": "評分", "selector": ".star", "type": "text"},
                {"name": "內容", "selector": ".text", "type": "text"}
            ]
        }
    ]
}
```

**輸出：**
```json
[
    {
        "名稱": "藍牙耳機",
        "價格": "$999",
        "評論": [
            {"用戶": "小明", "評分": "★★★★★", "內容": "超讚！"},
            {"用戶": "小華", "評分": "★★★★☆", "內容": "不錯用"}
        ]
    }
]
```

---

## 5. 常見錯誤與解決方案

### ❌ 錯誤 1：用 "all": True 處理關聯資料

```python
# 錯誤寫法
{
    "name": "評論者", "selector": ".reviewer", "type": "text", "all": True
},
{
    "name": "評分", "selector": ".rating", "type": "text", "all": True
}
```

**問題：** 評論者和評分會分開成兩個陣列，無法對應。

**輸出（錯誤）：**
```json
{
    "評論者": ["小明", "小華"],
    "評分": ["5星", "4星"]
}
```

**✅ 正確寫法：**
```python
{
    "name": "評論",
    "selector": ".review",
    "type": "nested_list",
    "fields": [
        {"name": "評論者", "selector": ".reviewer", "type": "text"},
        {"name": "評分", "selector": ".rating", "type": "text"}
    ]
}
```

---

### ❌ 錯誤 2：baseSelector 選錯層級

```python
# 錯誤：選到太細的層級
"baseSelector": ".product-name"  # ❌

# 正確：選到包含所有資料的區塊
"baseSelector": ".product"       # ✅
```

---

### ❌ 錯誤 3：忘記 fields 是陣列

```python
# 錯誤
"fields": {"name": "標題", "selector": ".title", "type": "text"}  # ❌

# 正確
"fields": [{"name": "標題", "selector": ".title", "type": "text"}]  # ✅
```

---

## 6. 速查表

### 類型選擇指南

| 情境 | 使用類型 | 範例 |
|------|---------|------|
| 單一文字 | `"type": "text"` | 標題、價格 |
| 多個獨立文字 | `"type": "list"` | 標籤、特色 |
| 單一屬性 | `"type": "attribute"` | 連結、圖片 |
| 保留 HTML | `"type": "html"` | 富文本內容 |
| 單一巢狀區塊 | `"type": "nested"` | 作者資訊 |
| 多個巢狀區塊 | `"type": "nested_list"` | 評論、訂單項目 |

### 決策樹

```
需要擷取的資料是...

├── 單一元素？
│   ├── 要文字 → type: "text"
│   ├── 要屬性 → type: "attribute"
│   └── 要 HTML → type: "html"
│
└── 多個元素？
    ├── 各元素獨立（無子欄位）→ type: "list"
    └── 各元素有結構（有子欄位）→ type: "nested_list" ⭐
```

---

## 總結

記住這個黃金法則：

> **當你需要擷取「多個有結構的區塊」時，永遠使用 `nested_list`！**

例如：評論、訂單項目、商品規格、時間軸事件... 這些都適合用 `nested_list`。

---

*文件版本：1.0 | 適用於 Crawl4AI 0.7.x*
