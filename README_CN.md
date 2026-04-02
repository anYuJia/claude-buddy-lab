# Claude Buddy Lab

**搜索、预览并应用自定义 Claude Code 伙伴 - 通过二进制修补实现。**

[English](README.md)

<p align="center">
  <img src="img/web-preview.png" width="720" alt="Web 界面">
</p>

## 功能特性

- **二进制修补** — 直接修补 Claude Code 二进制文件，不是改配置文件。
- **搜索引擎** — 暴力搜索数百万个 salt，找到你想要的伙伴。
- **实时预览** — ASCII 精灵图、属性、稀有度、闪光状态，应用前一目了然。
- **一键应用** — 在网页上直接应用，原始 salt 自动记录以便恢复。
- **中英双语** — 自动检测浏览器语言。
- **一键恢复** — 随时恢复为默认伙伴。

## 截图

| Web 界面 | 搜索结果 | Claude Code 中的效果 |
|:---:|:---:|:---:|
| ![Web](img/web-preview.png) | ![搜索](img/search-results.png) | ![伙伴](img/buddy-in-claude.png) |

## 快速开始

```bash
git clone https://github.com/anYuJia/claude-buddy-lab.git
cd claude-buddy-lab
pip3 install flask

# 启动（自动打开浏览器）
python3 cli.py --open
```

打开 http://127.0.0.1:8080 — 搜索你想要的伙伴，预览后点击 **应用**。

### 启动参数

```bash
python3 cli.py                # 启动服务
python3 cli.py --open         # 启动并打开浏览器
python3 cli.py --port 9090    # 自定义端口
python3 cli.py --host 0.0.0.0 # 监听所有接口
```

## 工作原理

Claude Code 的伙伴由 `hash(userId + salt)` 决定。salt（`friend-2026-401`，15 字符）硬编码在二进制文件中。

本工具：
1. **搜索**数百万个 salt 值，找到能生成你想要的伙伴的那个
2. **修补**二进制文件 — 用新 salt 替换旧的（等长替换）
3. 在 macOS 上**重新签名**（`codesign`）
4. **记录**原始 salt 到 `~/.claude-buddy-lab.json` 以便恢复

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/meta` | 元数据 + 二进制状态 |
| GET | `/api/binary` | 当前二进制 salt |
| POST | `/api/preview` | 预览指定 userId + salt 的伙伴 |
| POST | `/api/search` | 按条件搜索 salt |
| POST | `/api/apply` | 修补二进制文件应用新 salt |
| POST | `/api/restore` | 恢复原始 salt |

## 依赖

- Python 3.8+
- Flask: `pip3 install flask`
- 已安装 Claude Code

## 许可证

MIT
