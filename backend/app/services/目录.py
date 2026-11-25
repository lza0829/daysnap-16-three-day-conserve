from app.db import 连接


def 总览() -> dict:
    conn = 连接()
    try:
        def 数(sql: str) -> int:
            return int(conn.execute(sql).fetchone()[0])

        d: dict = {
            "账户数": 数("SELECT COUNT(*) FROM 账户"),
            "流水数": 数("SELECT COUNT(*) FROM 变动流水 WHERE 命运='已入账'"),
            "快照数": 数("SELECT COUNT(*) FROM 周期快照 WHERE 状态='有效'"),
            "差额行数": 数("SELECT COUNT(*) FROM 差额行"),
            "断档数": 数("SELECT COUNT(*) FROM 断档记录"),
            "跳变数": 数("SELECT COUNT(*) FROM 跳变记录"),
            "旁置数": 数("SELECT COUNT(*) FROM 旁置簿"),
            "抽取批次数": 数("SELECT COUNT(*) FROM 抽取批次"),
            "回放批次数": 数("SELECT COUNT(*) FROM 回放批次"),
        }
        # 三日连环守恒（口径 A：独立证明表）。老库可能尚未建链表，防御性补建。
        try:
            from app.modules.三日连环守恒 import 确保链表

            确保链表(conn)
            d["连环证明数"] = 数("SELECT COUNT(*) FROM 守恒证明")
            d["连环通过数"] = 数("SELECT COUNT(*) FROM 守恒证明 WHERE 通过=1")
            d["连环链批数"] = 数("SELECT COUNT(*) FROM 链式批")
            r = conn.execute(
                "SELECT 链号 FROM 守恒证明 ORDER BY rowid DESC LIMIT 1"
            ).fetchone()
            d["最近链号"] = r["链号"] if r else ""
        except Exception:
            d.setdefault("连环证明数", 0)
            d.setdefault("连环通过数", 0)
            d.setdefault("连环链批数", 0)
            d.setdefault("最近链号", "")
        return d
    finally:
        conn.close()
