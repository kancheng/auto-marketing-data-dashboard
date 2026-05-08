# auto-marketing-data-dashboard

車商行銷數據的端到端專案，完整包含以下流程：

1. 產生 Excel（車商行銷原始資料）
2. 由 Python 讀取 Excel 並輸出 JSON（供前端儀表板使用）
3. 單檔 `dashboard.html`（CSS/JS 內嵌）讀取預設 JSON 做數據呈現
4. 根據 JSON 輸出 PDF 數據視覺化報告

## 專案結構

- `scripts/generate_excel.py`：建立 `data/dealer_marketing_data.xlsx`
- `scripts/excel_to_json.py`：將 Excel 轉成 `data/marketing_dashboard.json`
- `scripts/export_pdf_report.py`：輸出 `output/marketing_report.pdf`
- `dashboard.html`：前端儀表板（內嵌 CSS + JS）
- `data/`：資料輸入與中間輸出
- `output/`：報告輸出

## 安裝

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 執行步驟

```bash
python scripts/generate_excel.py
python scripts/excel_to_json.py
python scripts/export_pdf_report.py
```

執行完成後會得到：

- `data/dealer_marketing_data.xlsx`
- `data/marketing_dashboard.json`
- `output/marketing_report.pdf`

## 開啟儀表板

建議在專案根目錄啟動本地伺服器：

```bash
python -m http.server 8000
```

瀏覽器打開 `http://localhost:8000/dashboard.html`，即可讀取 `data/marketing_dashboard.json` 顯示 KPI、趨勢與活動表格。
