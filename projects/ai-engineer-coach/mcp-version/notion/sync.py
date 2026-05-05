"""
Notion 自动记录脚本
每次对话后自动将 trainee.json 数据同步到 Notion Database
"""
import json
import os
import sys
from datetime import datetime, timedelta

# ── 依赖 ──────────────────────────────────────────────────────────
try:
    from notion_client import NotionClient
except ImportError:
    print("[coach] notion-client 未安装，正在安装...")
    os.system(f"{sys.executable} -m pip install notion-client -q")
    from notion_client import NotionClient

# ── 路径 ──────────────────────────────────────────────────────────
WORKSPACE = os.path.expanduser(r"C:\Users\mengdejun\.qclaw\workspace")
TRAINEE_PATH = os.path.join(WORKSPACE, "projects", "ai-engineer-coach", "mcp-version")
CONFIG_FILE = os.path.join(TRAINEE_PATH, "config.json")
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(WORKSPACE, ".env")

# ── 加载环境变量（NOTION_API_KEY）───────────────────────────────
def load_env():
    env = {}
    path = os.path.join(SCRIPTS_DIR, ".env")
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    k, v = line.split("=", 1)
                    env[k.strip()] = v.strip()
    return env

# ── 读取 trainee.json（从教练 skill 目录）────────────────────────
def load_trainee():
    paths = [
        os.path.expanduser(r"~\.qclaw\skills\ai-engineer-coach\DATA\trainee.json"),
        os.path.join(WORKSPACE, "projects", "ai-engineer-coach", "trainee.json"),
    ]
    for p in paths:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return {}

# ── 生成 Notion Page 内容 ─────────────────────────────────────────
def build_page(data: dict) -> dict:
    """将 trainee.json 的关键字段转换为 Notion Page"""
    phase = data.get("phase", "exploring")
    stats = data.get("stats", {})
    goal = data.get("goal", {})
    level = data.get("level", 1)
    exp = data.get("exp", 0)

    # 阶段描述
    phase_desc = {
        "exploring": "探索期",
        "validating": "验证期",
        "stable": "稳定期",
        "expanding": "扩张期",
    }.get(phase, phase)

    # 里程碑状态
    milestones = goal.get("milestones", [])
    milestone_status = []
    for m in milestones:
        emoji = "✅" if m.get("done") else "⬜"
        desc = m.get("desc", "")
        milestone_status.append(f"{emoji} {desc}")

    # 近期记录摘要（最近5条）
    records = data.get("records", [])
    recent = records[-5:] if records else []
    records_summary = "\n".join([
        f"- {r.get('date','')} | {r.get('client','')} | {r.get('amount',0)}元 | {r.get('status','')}"
        for r in recent
    ]) if recent else "暂无记录"

    # 练功 streak
    dp = data.get("dailyPractice", {})
    streak_lines = []
    for kind in ["writing", "thinking", "expressing"]:
        s = dp.get(kind, {})
        streak_lines.append(f"- {kind}: 连续{s.get('streak', 0)}天 / 共{s.get('completed', 0)}次")

    # 本次同步内容
    content = f"""## 📊 训练档案快照

**等级**：Lv{level} ({exp} EXP)
**阶段**：{phase_desc}
**成功定义**：{goal.get('successDefinition', '未定义')}
**当前方向**：{goal.get('direction', '未选择')}

---

### 🏆 里程碑
{chr(10).join(milestone_status)}

---

### 📈 数据统计
- 总交易数：{stats.get('totalDeals', 0)}
- 总收入：{stats.get('totalRevenue', 0)}元
- 连续有收入周数：{stats.get('consecutiveWeeksWithIncome', 0)}周

---

### 📝 练功记录
{chr(10).join(streak_lines)}

---

### 📋 近期交易记录
{records_summary}
"""

    return {
        "parent": {"database_id": get_config()["notion"]["databaseId"]},
        "properties": {
            "名称": {
                "title": [{"text": {"content": f"训练快照 {datetime.now().strftime('%Y-%m-%d')}"}}]
            },
            "日期": {"date": {"start": datetime.now().strftime("%Y-%m-%d")}},
            "类型": {"select": {"name": "数据快照"}},
            "等级": {"number": level},
            "EXP": {"number": exp},
            "阶段": {"select": {"name": phase_desc}},
            "总收入": {"number": stats.get("totalRevenue", 0)},
            "交易数": {"number": stats.get("totalDeals", 0)},
            "状态": {"status": {"name": "已记录"}},
        },
        "children": [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {"rich_text": [{"text": {"content": "📊 训练档案快照"}}]}
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {"rich_text": [{"text": {"content": content}}]}
            }
        ]
    }

# ── 配置读写 ──────────────────────────────────────────────────────
def get_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {"notion": {"apiKey": "", "databaseId": "", "status": "pending_setup"}}

def save_config(cfg: dict):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

# ── 主函数 ────────────────────────────────────────────────────────
def main():
    print("[coach-notion] 开始同步到 Notion...")

    cfg = get_config()
    if cfg["notion"]["status"] != "ready":
        print("[coach-notion] ❌ Notion 未配置：config.json 中 notion.status != 'ready'")
        print("[coach-notion] 请先设置 NOTION_API_KEY 和 databaseId")
        sys.exit(1)

    data = load_trainee()
    if not data:
        print("[coach-notion] ❌ 未找到 trainee.json")
        sys.exit(1)

    env = load_env()
    api_key = os.environ.get("NOTION_API_KEY") or env.get("NOTION_API_KEY") or cfg["notion"].get("apiKey", "")

    if not api_key:
        print("[coach-notion] ❌ 未设置 NOTION_API_KEY 环境变量")
        sys.exit(1)

    try:
        from notion_client import NotionClient
        client = NotionClient(api_key)
        page = build_page(data)
        result = client.create_page(**page)
        print(f"[coach-notion] ✅ 同步成功！Page ID: {result.get('id', result)}")
    except Exception as e:
        print(f"[coach-notion] ❌ 同步失败：{e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
