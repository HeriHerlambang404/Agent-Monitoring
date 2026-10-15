import json
import os
import sqlite3
import time

home = os.environ.get("HERMES_HOME") or os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes")
db_path = os.path.join(home, "state.db")
result = {"updatedAt": time.time(), "sessions": []}
try:
    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=1) as db:
        rows = db.execute("""
            SELECT id, title, source, model, started_at, ended_at, message_count,
                   tool_call_count, input_tokens, output_tokens, last_activity_at,
                   last_activity_description, cwd, git_repo_root
            FROM sessions
            WHERE archived = 0
            ORDER BY COALESCE(last_activity_at, started_at) DESC
            LIMIT 20
        """).fetchall()
        for row in rows:
            (sid, title, source, model, started, ended, messages, tools,
             input_tokens, output_tokens, activity_at, activity_desc, cwd, repo) = row
            result["sessions"].append({
                "id": sid,
                "title": title or "Untitled session",
                "source": source,
                "model": model,
                "startedAt": started,
                "endedAt": ended,
                "active": ended is None,
                "messageCount": messages or 0,
                "toolCallCount": tools or 0,
                "inputTokens": input_tokens or 0,
                "outputTokens": output_tokens or 0,
                "lastActivityAt": activity_at,
                "lastActivity": activity_desc or "No activity description",
                "cwd": cwd,
                "repo": repo,
                "recentMessages": [
                    {"role": msg[0], "tool": msg[1], "content": msg[2] or "", "timestamp": msg[3]}
                    for msg in db.execute(
                        """SELECT role, tool_name, substr(COALESCE(content, ''), 1, 180), timestamp
                           FROM messages WHERE session_id = ?
                           ORDER BY timestamp DESC LIMIT 5""", (sid,)
                    ).fetchall()
                ],
            })
except Exception as exc:
    result["error"] = type(exc).__name__
    result["message"] = "Hermes session store unavailable"
# ASCII-safe output keeps Windows CMD/charmap from failing on agent emoji.
print(json.dumps(result, ensure_ascii=True))
