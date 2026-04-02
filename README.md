<div align="center">

# 🧪 Claude Buddy Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)

每个 Claude Code 用户在终端里都有一个独特的 ASCII 伙伴（Buddy）。
它由 `hash(userId + salt)` 确定性生成 — 不同的 salt 会产生完全不同的物种、稀有度、属性和外观。
然而这个 salt 是硬编码在 Claude Code 的二进制文件中的，正常情况下无法修改。

**本工具提供了一个可视化的 Web 界面，让你暴力搜索数百万个 salt 组合，
实时预览每个 salt 对应的伙伴，找到心仪的那个后一键修补到二进制文件中。**

支持按物种、稀有度、眼睛、帽子、闪光等条件筛选，还能随时恢复为原始伙伴。

[English](README_EN.md)

---

<img src="img/web-preview.png" width="720">

</div>

## 快速开始

```bash
git clone https://github.com/anYuJia/claude-buddy-lab.git
cd claude-buddy-lab
pip3 install flask
python3 cli.py --open
```

<div align="center">

| 搜索结果 | Claude Code 中的效果 |
|:---:|:---:|
| <img src="img/search-results.png" width="420"> | <img src="img/buddy-in-claude.png" width="260"> |

</div>

## 工作原理

> Buddy = `hash(userId + salt)` — salt 硬编码在 Claude 二进制文件中。

1. **搜索** — 遍历数百万个 salt，按你的条件筛选匹配的伙伴
2. **预览** — 在网页上查看 ASCII 精灵图、属性面板、稀有度和闪光状态
3. **修补** — 在二进制文件中定位旧 salt 字节，等长替换为新 salt
4. **签名** — macOS 上自动重新 ad-hoc 签名（`codesign`）
5. **记录** — 原始 salt 保存到 `~/.claude-buddy-lab.json`，随时可恢复

## API

```
GET  /api/meta       — 元数据 + 二进制状态
GET  /api/binary     — 当前 salt 检测
POST /api/preview    — 预览伙伴
POST /api/search     — 条件搜索
POST /api/apply      — 修补二进制
POST /api/restore    — 恢复原始
```

<div align="center">

---

MIT License

</div>
