# Task
台灣銀行牌告匯率查詢：可指定幣別代碼（預設 USD），擷取現金買入與現金賣出匯率

# Parameters
| name     | type | source phrase from task            | default | allowed / format                          |
|----------|------|------------------------------------|---------|-------------------------------------------|
| currency | str  | "可指定幣別代碼（預設 USD）"          | "USD"   | 台灣銀行支援的 ISO 4217 代碼，如 USD、EUR、JPY、GBP 等 |

# Critical Points
- [ ] CP1: 成功導航至台灣銀行牌告匯率頁面
- [ ] CP2: 匯率表格已載入，列數 > 0
- [ ] CP3: 找到指定幣別（currency 參數）的列
- [ ] CP4: 擷取「現金買入」匯率（非空值）
- [ ] CP5: 擷取「現金賣出」匯率（非空值）
- [ ] CP6: step 0 params 行寫入 log，結果輸出至 final_script_log.txt
