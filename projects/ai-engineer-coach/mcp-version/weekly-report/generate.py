"""
自动周报脚本
每周一早上生成训练数据总结，发到微信
由 OpenClaw Cron 定时触发
"""
import json
import os
import sys
from datetime import datetime, timedelta

WORKSPACE = os.path.expanduser(r"C:\Users\mengdejun\.qclaw\workspace")
SKILL_DIR  = os.path.expanduser(r"~\.qclaw\skills\ai-engineer-coach\DATA")
CONFIG_FILE = os.path.join(WORKSPACE, "projects", "ai-engineer-coach", "mcp-version", "config.json")

# ── 读取 trainee.json ─────────────────────────────────────────────
def load_trainee():
    path = os.path.join(SKILL_DIR, "trainee.json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return {}

# ── 计算上周数据 ───────────────────────────────────────────────────
def compute_weekly_stats(data: dict) -> dict:
    """从 records 中提取上周（本周之前的7天）的数据"""
    records = data.get("records", [])
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())   # 本周一
    last_week_end = week_start - timedelta(days=1)         # 上周日
    last_week_start = last_week_end - timedelta(days=6)     # 上周一

    last_week_records = []
    for r in records:
        try:
            rdate = datetime.strptime(r.get("date", ""), "%Y-%m-%d").date()
            if last_week_start <= rdate <= last_week_end:
                last_week_records.append(r)
        except ValueError:
            continue

    # 本周数据（用于对比）
    this_week_records = []
    for r in records:
        try:
            rdate = datetime.strptime(r.get("date", ""), "%Y-%m-%d").date()
            if week_start <= rdate <= today:
                this_week_records.append(r)
        except ValueError:
            continue

    dp = data.get("dailyPractice", {})
    streaks = {
        k: v.get("streak", 0) for k, v in dp.items()
    }

    return {
        "last_week": last_week_records,
        "this_week": this_week_records,
        "last_week_deals": len([r for r in last_week_records if r.get("status") == "paid"]),
        "last_week_revenue": sum(r.get("amount", 0) for r in last_week_records if r.get("status") == "paid"),
        "this_week_deals": len([r for r in this_week_records if r.get("status") == "paid"]),
        "this_week_revenue": sum(r.get("amount", 0) for r in this_week_records if r.get("status") == "paid"),
        "streaks": streaks,
        "week_label": f"{last_week_start.strftime('%m/%d')}–{last_week_end.strftime('%m/%d')}",
    }

# ── 生成周报文本 ───────────────────────────────────────────────────
def build_weekly_report(data: dict) -> str:
    stats = compute_weekly_stats(data)
    goal = data.get("goal", {})
    level = data.get("level", 1)
    exp = data.get("exp", 0)
    phase = data.get("phase", "exploring")
    phase_names = {"exploring": "探索期", "validating": "验证期", "stable": "稳定期", "expanding": "扩张期"}
    phase_name = phase_names.get(phase, phase)

    # 等级称号
    titles = {1: "新手", 2: "入门", 3: "验证者", 4: "稳定者", 5: "高手", 6: "专家", 7: "宗师"}
    title = titles.get(level, "新手")

    # 里程碑进度
    milestones = goal.get("milestones", [])
    ms_lines = []
    for m in milestones:
        done = m.get("done", False)
        desc = m.get("desc", "未定义")
        ms_lines.append(f"{'✅' if done else '⬜'} {desc}")

    # 上周亮点记录
    last_records = stats["last_week"]
    highlight = ""
    if last_records:
        paid = [r for r in last_records if r.get("status") == "paid"]
        if paid:
            r = paid[-1]
            highlight = f"💰 最近成交：{r.get('client','?')} · {r.get('amount',0)}元"
        else:
            pending = last_records[-1]
            highlight = f"🔄 进行中：{pending.get('client','?')} · {pending.get('status','')}"

    # EXP 进度条
    exp_thresholds = [0, 100, 300, 600, 1000, 1500, 2500]
    cur = exp
    nxt = next((exp_thresholds[i+1] for i, t in enumerate(exp_thresholds[:-1]) if cur <= t), 2500)
    progress = int((cur / nxt) * 10)
    exp_bar = "█" * progress + "░" * (10 - progress)

    report = f"""📊 AI教练 · 上周训练报告
{stats['week_label']}

━━━━━━━━━
📍 阶段：{phase_name} · Lv{level} {title}
⚡ EXP：{exp_bar} {exp}/{nxt}
━━━━━━━━━

🏆 里程碑
{chr(10).join(ms_lines)}

📈 上周数据
• 成交笔数：{stats['last_week_deals']}笔
• 收入：{stats['last_week_revenue']}元
• 练功连续天数：写作{stats['streaks'].get('writing',0)}天 | 思考{stats['streaks'].get('thinking',0)}天 | 表达{stats['streaks'].get('expressing',0)}天

{highlight if highlight else '💡 本周继续推进...'}

━━━━━━━━━
🎯 本周目标
• {'完成第一笔交易' if stats['last_week_deals'] == 0 and stats['this_week_deals'] == 0 else '继续获客'}
• 每天练功
• {'推进里程碑1' if not milestones[0].get('done') else '推进里程碑2'}
━━━━━━━━━"""

    return report

# ── 主函数（供 Cron agent 调用）───────────────────────────────────
def main():
    print("[coach-weekly] 生成周报...")
    data = load_trainee()
    if not data:
        print("[coach-weekly] ❌ 未找到 trainee.json")
        sys.exit(1)
    report = build_weekly_report(data)
    print("[coach-weekly] 周报内容：")
    print(report)
    return report   # Cron job 的 agentTurn message 直接用这段文本

if __name__ == "__main__":
    main()
