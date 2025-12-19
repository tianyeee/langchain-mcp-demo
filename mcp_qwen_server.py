#!/usr/bin/env python3
"""
MCP (Model Context Protocol) 服务器 - FastMCP 风格

按照 https://docs.langchain.org.cn/oss/python/langchain/mcp 文档实现
提供计算器和时间工具供 Qwen 模型使用
"""

import os
import sqlite3
import logging
from fastmcp import FastMCP

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 创建 FastMCP 实例
mcp = FastMCP("QwenMCPTools")

# 数据库路径
DB_PATH = "wish_list.db"

@mcp.tool()
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间
    
    Args:
        format: 时间格式字符串（默认："%Y-%m-%d %H:%M:%S"）
        
    Returns:
        当前时间字符串
    """
    import datetime
    return datetime.datetime.now().strftime(format)


def init_wish_list_database():
    """初始化心愿列表数据库
    
    创建wish_list表并插入心愿数据
    """
    # 连接数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 创建心愿列表表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS wish_list (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )
    """)
    
    # 插入心愿数据
    wish_data = [
        ("天定山滑雪", "在天定山滑雪场享受滑雪乐趣"),
        ("南湖公园钓鱼", "在南湖公园进行休闲钓鱼活动"),
        ("南溪湿地公园搭帐篷露营", "在南溪湿地公园搭帐篷露营，亲近自然"),
        ("伪满皇宫博物院参观", "参观伪满皇宫博物院，了解历史"),
        ("长春动植物园看雪饼猴", "在长春动植物园观看网红【雪饼猴】和西游主题演出"),
        ("夜游新民大街", "夜晚游览新民大街，欣赏城市夜景"),
        ("净月潭看蓝冰", "在净月潭观看蓝冰奇景")
    ]
    
    # 先清空表，避免重复数据
    cursor.execute("DELETE FROM wish_list")
    
    # 插入数据
    cursor.executemany(
        "INSERT INTO wish_list (name, description) VALUES (?, ?)",
        wish_data
    )
    
    conn.commit()
    conn.close()
    logger.info(f"✅ 心愿列表数据库已初始化，保存位置: {os.path.abspath(DB_PATH)}")


@mcp.tool()
def query_wish_list(query: str = "") -> str:
    """查询心愿列表
    
    Args:
        query: 查询条件（可选），可以是心愿名称或关键词
        
    Returns:
        查询结果，格式为JSON字符串
    """
    try:
        # 连接数据库
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if query:
            # 模糊查询
            cursor.execute(
                "SELECT name, description FROM wish_list WHERE name LIKE ? OR description LIKE ?",
                (f"%{query}%", f"%{query}%")
            )
        else:
            # 查询所有心愿
            cursor.execute("SELECT name, description FROM wish_list")
        
        # 获取结果
        results = cursor.fetchall()
        conn.close()
        
        # 格式化为JSON
        import json
        wish_list = [{
            "name": row[0],
            "description": row[1]
        } for row in results]
        
        return json.dumps(wish_list, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)


if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("🚀 MCP 服务器启动")
    logger.info("=" * 60)
    
    # 初始化心愿列表数据库
    init_wish_list_database()
    
    logger.info("服务器配置:")
    logger.info("  - 传输协议: streamable-http")
    logger.info("  - 主机地址: 0.0.0.0")
    logger.info("  - 端口: 8000")
    logger.info("  - MCP 路径: /mcp")
    logger.info("")
    logger.info("可用工具:")
    #logger.info("  - calculator: 执行数学计算")
    logger.info("  - get_current_time: 获取当前时间")
    logger.info("  - query_wish_list: 查询心愿列表")
    logger.info("")
    logger.info("按 Ctrl+C 停止服务器")
    logger.info("=" * 60)
    
    # 启动 MCP 服务器
    mcp.run(transport="streamable-http")