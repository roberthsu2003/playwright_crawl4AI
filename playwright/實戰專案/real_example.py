"""第 13 章已拆成 12 個獨立實戰專案。

執行本檔會列出所有入口；請再選擇想練習的 main.py。
"""

from pathlib import Path


chapter_dir = Path(__file__).resolve().parent

print("第 13 章：真實網站實戰專案\n")
for project_dir in sorted(chapter_dir.glob("專案*")):
    entry = project_dir / "main.py"
    if entry.exists():
        print(f"- {project_dir.name}: {entry}")

print("\n請先閱讀 README.md，再執行各專案。")
