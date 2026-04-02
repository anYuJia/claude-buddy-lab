<div align="center">

# 🧪 Claude Buddy Lab

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-Web_UI-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)

**搜索、预览并应用自定义 Claude Code 伙伴**

**二进制修补，一键搞定。**

[English](README.md)

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

本工具搜索数百万个 salt，找到你想要的，直接修补进去。

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
