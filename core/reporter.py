import json
from pathlib import Path
from typing import List
from datetime import datetime


REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>AI 重复照片清理报告</title>
<style>
  body { font-family: -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; }
  h1 { color: #1a1a2e; }
  .summary { background: #f0f4ff; border-radius: 8px; padding: 20px; margin: 20px 0; }
  .group { border: 1px solid #ddd; border-radius: 8px; margin: 16px 0; padding: 16px; }
  .group h3 { margin: 0 0 8px; color: #555; }
  .file { font-family: monospace; font-size: 13px; color: #333; padding: 4px 0; }
  .keep { color: #27ae60; font-weight: bold; }
  .dup { color: #e74c3c; }
</style>
</head>
<body>
<h1>🤖 AI 重复照片清理报告</h1>
<div class="summary">
  <p><strong>扫描时间：</strong>{scan_time}</p>
  <p><strong>扫描照片总数：</strong>{total_photos}</p>
  <p><strong>发现重复组数：</strong>{total_groups}</p>
  <p><strong>可释放空间：</strong>{saved_mb:.1f} MB</p>
</div>
{groups_html}
</body>
</html>"""


class Reporter:
    def generate_html(self, groups: List[List[Path]], total_photos: int, output: str):
        saved_bytes = 0
        groups_html = ""
        for i, group in enumerate(groups, 1):
            sizes = [p.stat().st_size for p in group]
            keep = group[sizes.index(max(sizes))]
            saved_bytes += sum(sizes) - max(sizes)
            items = ""
            for p in group:
                cls = "keep" if p == keep else "dup"
                label = " ← 保留" if p == keep else " ← 删除"
                items += f'<div class="file {cls}">{p}{label}</div>\n'
            groups_html += f'<div class="group"><h3>重复组 #{i}</h3>{items}</div>\n'

        html = REPORT_TEMPLATE.format(
            scan_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            total_photos=total_photos,
            total_groups=len(groups),
            saved_mb=saved_bytes / 1024 / 1024,
            groups_html=groups_html,
        )
        Path(output).write_text(html, encoding="utf-8")
        print(f"Report saved: {output}")

    def generate_json(self, groups: List[List[Path]], output: str):
        data = [{"group": i + 1, "files": [str(p) for p in g]} for i, g in enumerate(groups)]
        Path(output).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"JSON report saved: {output}")
