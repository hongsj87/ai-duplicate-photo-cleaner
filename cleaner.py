#!/usr/bin/env python3
"""
AI 智能清理重复照片 - 主程序入口
Usage: python cleaner.py --scan /path/to/photos [--clean] [--threshold 90] [--report out.html]
"""
import click
import send2trash
from pathlib import Path
from core.scanner import PhotoScanner
from core.reporter import Reporter


@click.command()
@click.option("--scan", required=True, help="要扫描的照片目录")
@click.option("--clean", is_flag=True, default=False, help="自动清理重复照片（移入回收站）")
@click.option("--threshold", default=90, show_default=True, help="相似度阈值 0-100")
@click.option("--report", default=None, help="生成HTML报告路径（如 report.html）")
@click.option("--workers", default=4, show_default=True, help="并行线程数")
def main(scan, clean, threshold, report, workers):
    """🤖 AI 智能清理重复照片"""
    click.echo(f"\n🔍 扫描目录: {scan}")
    scanner = PhotoScanner(threshold=threshold, workers=workers)

    photos = scanner.scan(scan)
    click.echo(f"📷 发现照片: {len(photos)} 张")

    if not photos:
        click.echo("没有找到照片，退出。")
        return

    hashes = scanner.compute_hashes(photos)
    groups = scanner.find_duplicates(hashes)

    click.echo(f"\n🎯 发现重复组: {len(groups)} 组")
    total_dups = sum(len(g) - 1 for g in groups)
    click.echo(f"🗑️  可清理照片: {total_dups} 张")

    if report:
        r = Reporter()
        r.generate_html(groups, len(photos), report)

    if clean and groups:
        click.echo("\n🧹 开始清理...")
        cleaned = 0
        for group in groups:
            sizes = [p.stat().st_size for p in group]
            keep = group[sizes.index(max(sizes))]
            for p in group:
                if p != keep:
                    send2trash.send2trash(str(p))
                    cleaned += 1
                    click.echo(f"  🗑️  {p.name}")
        click.echo(f"\n✅ 已清理 {cleaned} 张重复照片（已移入回收站）")
    elif not clean and groups:
        click.echo("\n💡 使用 --clean 参数执行清理操作")

    click.echo("\n🎉 完成！")


if __name__ == "__main__":
    main()
