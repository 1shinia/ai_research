import json
with open(r"C:\Users\Administrator\.qwenpaw\workspaces\default\agent.json", encoding="utf-8") as f:
    cfg = json.load(f)
ch = cfg["channels"]["wechat"]
print(json.dumps({k: ch[k] for k in ["enabled", "filter_tool_messages", "filter_thinking", "message_merge_enabled", "message_merge_delay_ms"]}, indent=2, ensure_ascii=False))
