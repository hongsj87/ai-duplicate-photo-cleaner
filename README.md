# 🤖 AI 智能清理重复照片

> 使用感知哈希（pHash）+ 深度学习特征提取，自动检测并清理重复/相似照片，释放磁盘空间。

## ✨ 功能特性

- 🔍 **多算法检测**：MD5精确匹配 + pHash感知哈希 + CNN特征向量三重检测
- 📊 **相似度评分**：0-100分量化相似度，可自定义阈值
- 🗂️ **智能分组**：自动将重复照片分组，保留最高质量版本
- 🖼️ **支持格式**：JPG、PNG、HEIC、WebP、BMP、GIF
- 🚀 **批量处理**：多线程并行扫描，万张照片分钟级完成
- 🛡️ **安全模式**：默认移入回收站，不直接删除
- 📈 **详细报告**：HTML/JSON格式扫描报告

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 基本用法

```bash
# 扫描目录，预览重复照片（不删除）
python cleaner.py --scan /path/to/photos

# 扫描并自动清理（移入回收站）
python cleaner.py --scan /path/to/photos --clean

# 设置相似度阈值（默认90）
python cleaner.py --scan /path/to/photos --threshold 85

# 生成HTML报告
python cleaner.py --scan /path/to/photos --report report.html
```

## 📁 项目结构

```
ai-duplicate-photo-cleaner/
├── cleaner.py          # 主程序入口
├── core/
│   ├── scanner.py      # 文件扫描模块
│   ├── hasher.py       # 哈希计算模块
│   ├── comparator.py   # 相似度比较模块
│   └── reporter.py     # 报告生成模块
├── requirements.txt    # 依赖列表
└── tests/              # 单元测试
```

## 🧠 算法原理

1. **MD5精确匹配**：字节级完全相同的照片
2. **感知哈希(pHash)**：将图片缩放为32×32灰度图，计算DCT哈希，汉明距离<10视为相似
3. **CNN特征提取**：使用MobileNetV2提取512维特征向量，余弦相似度>0.95视为相似

## 📄 License

MIT License
