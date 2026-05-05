# AI 教练 MCP 版 · 搭建指南

> 让教练自动记录、自动提醒、自动生成周报

---

## 📦 已创建的文件

```
projects/ai-engineer-coach/mcp-version/
├── config.json              ← MCP 配置（Notion + Cron 设置）
├── notion/
│   └── sync.py             ← 自动同步 trainee.json → Notion
└── weekly-report/
    └── generate.py         ← 生成周报内容
```

---

## 📋 设置清单（需要你操作的部分）

### ✅ 已完成（系统自动）

- [x] **每日练功提醒** Cron 已注册（ID: `4052f541...`，周一~五 9:00 发微信）
- [x] **每周周报** Cron 已注册（ID: `b718aac9...`，每周一 9:00 发微信）
- [x] 周报生成脚本（Python，直接读 trainee.json 生成数据）
- [x] Notion 同步脚本框架（Python）

### ⬜ Notion 设置（需要你操作）

**Step 1：创建 Notion Database**

1. 打开 Notion，新建一个空白页面
2. 在页面内输入 `/database` 选择"数据库"
3. 添加以下属性（和 config.json 中一致）：

| 属性名 | 类型 |
|--------|------|
| 名称 | 标题 |
| 日期 | 日期 |
| 类型 | 选择 |
| 等级 | 数字 |
| EXP | 数字 |
| 阶段 | 选择 |
| 总收入 | 数字 |
| 交易数 | 数字 |
| 状态 | 状态 |
| 备注 | 文本 |

**Step 2：获取 Database ID**

1. 打开刚创建的 Database
2. 复制浏览器 URL：
   ```
   https://www.notion.so/你的工作区/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
                                                   ↑
                                                   这段就是 Database ID
   ```
   （形如 `a1b2c3d4e5f6g7h8i9j0...`）

3. 复制 Database ID 后，告诉我，我来帮你写入 config.json

**Step 3：获取 API Key（如果需要）**

1. 去 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 名字随意（如 "AI教练"）
4. 选择目标工作区
5. 复制生成的 API Key（`secret_xxx...`）
6. 在 Database 页面右上角 Share → 添加你的 integration

---

## 📁 文件说明

### notion/sync.py

每次对话后（或手动触发），将 `trainee.json` 的数据同步到 Notion Database：

```bash
python notion/sync.py
# 输出：✅ 同步成功！Page ID: xxx
```

**触发时机**（教练 Skill 自动触发）：
- 用户完成一个 Sprint
- 用户完成一个里程碑
- 用户要求"同步到 Notion"

### weekly-report/generate.py

生成上周训练数据报告文本，用于 Cron job 发到微信：

```bash
python weekly-report/generate.py
# 输出周报内容
```

---

## 🔧 手动触发命令

| 命令 | 效果 |
|------|------|
| `python notion/sync.py` | 同步数据到 Notion |
| `python weekly-report/generate.py` | 生成周报文本 |
| 在微信对教练说"同步" | 触发 Notion 同步 |
| 在微信对教练说"周报" | 触发周报生成 |

---

## ❓ 常见问题

**Q：Notion API Key 怎么获取？**
A：https://www.notion.so/my-integrations → New integration → 复制 secret

**Q：Database ID 是什么？**
A：Database 的 URL 末尾 `?v=` 前面那一段字母数字混合字符串

**Q：可以不发到微信吗？**
A：可以改配置改到其他渠道，但现在微信是唯一已登录的渠道

**Q：每日提醒可以改时间吗？**
A：可以，告诉我新时间，我来修改 cron 任务

---

*本指南对应 ai-engineer-coach MCP 版本 v1.0*
