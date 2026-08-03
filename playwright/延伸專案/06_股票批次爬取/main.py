"""
06_股票批次爬取 (Playwright Async 版 - 無 GUI)
--------------------------------------------------
本專案示範如何使用 Async Playwright 進行多支股票的非同步併發爬取與速率控制。
核心功能：
1. 整合 twstock 提供 CLI 熱門股票搜尋與選擇
2. 使用 asyncio.Semaphore 進行並行數與速率限制，保護目標伺服器
3. 終端機格式化批次報表輸出
4. 導出 CSV / JSON 檔案
"""

import sys
import time
import asyncio
import twstock

from stock_batch_scraper import batch_fetch_stocks, export_to_csv, export_to_json

def search_stocks_with_twstock(query: str) -> list[dict]:
    """
    使用 twstock 根據代碼或名稱關鍵字搜尋股票清單
    """
    query = query.strip().lower()
    results = []
    
    for code, info in twstock.codes.items():
        # 過濾一般 4 位數上市/上櫃股票
        if len(code) == 4 and (info.type == '股票' or getattr(info, 'market', '') in ['上市', '上櫃']):
            if query in code.lower() or query in info.name.lower():
                results.append({
                    "code": code,
                    "name": info.name,
                    "market": getattr(info, 'market', '台股'),
                    "group": getattr(info, 'group', '')
                })
    return results

def display_batch_results(data_list: list[dict]):
    """在終端機列印格式化批次股票報表"""
    print("\n" + "=" * 90)
    print(f"{'股票代碼':<10} {'股票名稱':<12} {'即時價格':<12} {'漲跌金額/幅度':<16} {'資料更新時間':<20}")
    print("-" * 90)
    
    for item in data_list:
        code = item.get("股票代碼", "N/A")
        name = item.get("股票名稱", "N/A")
        price = item.get("即時價格", "N/A")
        chg = item.get("漲跌資訊", "N/A")
        time_str = item.get("資料時間", "N/A")
        
        print(f"{code:<10} {name:<12} {price:<12} {chg:<16} {time_str:<20}")
        
    print("=" * 90 + "\n")

async def run_batch_scrape(stock_codes: list[str]):
    """執行批次抓取與結果顯示流程"""
    print(f"\n🚀 開始批次爬取 {len(stock_codes)} 支股票: {', '.join(stock_codes)}")
    start_time = time.time()
    
    results = await batch_fetch_stocks(stock_codes, max_concurrency=3)
    elapsed = time.time() - start_time
    
    print(f"\n✨ 批次爬取完成！總耗時: {elapsed:.2f} 秒")
    display_batch_results(results)
    
    return results

def cli_menu():
    """CLI 文字選單介面"""
    default_popular_stocks = ["2330", "2317", "2454", "2308", "3008"]
    last_results = []
    
    while True:
        print("\n==========================================")
        print(" 📈 Playwright 股票批次爬取系統 (CLI 版)")
        print("==========================================")
        print(" [1] 預設熱門股票批次抓取 (2330, 2317, 2454, 2308, 3008)")
        print(" [2] 關鍵字搜尋股票並選擇批次抓取 (twstock)")
        print(" [3] 自訂股票代碼清單 (用逗號分隔)")
        print(" [4] 匯出最近一次抓取結果 (CSV / JSON)")
        print(" [0] 離開系統")
        print("------------------------------------------")
        
        choice = input("請選擇操作選項 (0-4): ").strip()
        
        if choice == "1":
            last_results = asyncio.run(run_batch_scrape(default_popular_stocks))
            
        elif choice == "2":
            keyword = input("\n請輸入股票代碼或名稱關鍵字 (例如 23 或 晶圓): ").strip()
            if not keyword:
                print("⚠️ 關鍵字不可為空！")
                continue
                
            matches = search_stocks_with_twstock(keyword)
            if not matches:
                print(f"❌ 查無符合 '{keyword}' 的股票！")
                continue
                
            print(f"\n找到 {len(matches[:20])} 筆符合條件的股票 (最多顯示 20 筆):")
            for idx, item in enumerate(matches[:20], 1):
                print(f" [{idx:2d}] {item['code']} - {item['name']} ({item['market']})")
                
            input_indices = input("\n請輸入要爬取的序號 (用逗號分隔，例如 1,2,3 或 'all'): ").strip()
            if not input_indices:
                continue
                
            selected_codes = []
            if input_indices.lower() == "all":
                selected_codes = [item['code'] for item in matches[:20]]
            else:
                for parts in input_indices.split(","):
                    if parts.strip().isdigit():
                        idx = int(parts.strip()) - 1
                        if 0 <= idx < len(matches[:20]):
                            selected_codes.append(matches[idx]['code'])
                            
            if selected_codes:
                last_results = asyncio.run(run_batch_scrape(selected_codes))
            else:
                print("⚠️ 未選擇任何有效股票！")
                
        elif choice == "3":
            user_input = input("\n請輸入股票代碼清單 (用逗號分隔，例: 2330, 2317): ").strip()
            if not user_input:
                print("⚠️ 代碼不可為空！")
                continue
            codes = [c.strip() for c in user_input.split(",") if c.strip()]
            if codes:
                last_results = asyncio.run(run_batch_scrape(codes))
                
        elif choice == "4":
            if not last_results:
                print("⚠️ 目前無抓取結果可供匯出，請先執行爬取作業！")
                continue
            export_choice = input("請選擇匯出格式 (1: CSV, 2: JSON, 3: 兩者皆是): ").strip()
            if export_choice in ["1", "3"]:
                export_to_csv(last_results)
            if export_choice in ["2", "3"]:
                export_to_json(last_results)
                
        elif choice == "0":
            print("\n👋 感謝使用股票批次爬取系統！")
            break
        else:
            print("⚠️ 無效的選項，請重新輸入！")

async def main():
    # 如果命令列包含股票代碼參數，直接非互動批次爬取
    if len(sys.argv) > 1:
        stock_codes = sys.argv[1:]
        results = await run_batch_scrape(stock_codes)
        export_to_csv(results)
    else:
        cli_menu()

if __name__ == "__main__":
    asyncio.run(main())
