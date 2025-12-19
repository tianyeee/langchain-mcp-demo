#!/usr/bin/env python3
"""
MCP (Model Context Protocol) 框架演示 - 使用 Qwen 模型

按照 https://docs.langchain.org.cn/oss/python/langchain/mcp 文档实现
展示如何使用 MCP 协议将工具提供给 LLM，特别是与 Qwen 模型的集成
"""

import asyncio
import logging
from fastmcp import Client

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# 安装必要的依赖：
# uv pip install langchain-mcp-adapters langchain-openai langchain fastmcp

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent


async def main():
    """主函数 - 演示 MCP 客户端与工具服务器的集成"""
    logger.info("=" * 60)
    logger.info("🎯 MCP 客户端工具演示")
    logger.info("=" * 60)
    logger.info("")

    # 步骤1: 创建 MCP 客户端，同时连接本地和远程MCP服务
    logger.info("🔌 创建 MCP 客户端...")
    try:
        # 配置同时连接本地和远程MCP服务
        client = MultiServerMCPClient(
            {
                "local_tools": {
                    "transport": "streamable_http",
                    "url": "http://localhost:8000/mcp",
                },
                "cloud_tools": {
                    "transport": "streamable_http",
                    "url": "https://previous-beige-opossum.fastmcp.app/mcp",
                    "headers": {
                        "Authorization": "Bearer fmcp_dNJmpUPbLwXcMLbb4eOIX2ByCdMjGWSklIaBOA3PBws"
                    }
                },
                "weather_mcp": {
                    "transport": "streamable_http",
                    "url": "https://dashscope.aliyuncs.com/api/v1/mcps/market-cmapi033617/mcp",
                    "headers": {
                        "Authorization": "Bearer sk-df156b2ab7ed4ea5a1d7ff550277f0c9"
                    }
                }
            }
        )
        logger.info("✅ MCP 客户端创建成功")
        logger.info("")
    except Exception as e:
        logger.error(f"❌ MCP 客户端创建失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return

    # 步骤2: 获取可用工具列表
    logger.info("📋 获取 MCP 工具列表...")
    try:
        tools = await client.get_tools()
        
        logger.info(f"✅ 成功获取 {len(tools)} 个工具:")
        for tool in tools:
            logger.info(f"   - {tool.name}: {tool.description}")
        logger.info("")
    except Exception as e:
        logger.error(f"❌ 获取工具列表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return

    # 步骤3: 配置 Qwen 模型并创建代理
    logger.info("🤖 配置 Qwen 模型并创建代理...")
    try:
        #配置 Qwen 模型
        llm = ChatOpenAI(
            model="qwen-plus",
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key="sk-df156b2ab7ed4ea5a1d7ff550277f0c9"
        )
        #llm = ChatOpenAI(model="qwen3-32b",base_url="http://139.210.101.45:12455/v1",api_key="your_api_key",)
        logger.info("✅ Qwen 模型配置成功")
        logger.info("")

        # 创建代理
        agent = create_agent(
            llm,
            tools,
            system_prompt="""你是一个智能助手，能够使用各种工具来帮助用户完成任务。

工作流程：
1. 分析用户的问题
2. 选择合适的工具来解决问题
3. 使用工具获取结果
4. 总结结果并回答用户

注意事项：
- 只使用提供的工具
- 如果工具调用失败，分析错误并重新尝试
- 用中文总结工具调用结果
""",
        )
        logger.info("✅ 代理创建成功")
        logger.info("")

        # 步骤4: 使用代理测试工具功能
        logger.info("🧪 使用代理测试工具功能...")
        
        # 测试1: 使用计算器工具
        logger.info("\n测试1: 使用计算器工具")
        try:
            response1 = await agent.ainvoke({"messages": [{"role": "user", "content": "计算 25 * 4 + 100 的结果，直接返回计算结果"}]})
            final_message1 = response1["messages"][-1]
            logger.info(f"查询: 计算 25 * 4 + 100 的结果")
            logger.info(f"回答: {final_message1.content}")
        except Exception as e:
            logger.info(f"查询: 计算 25 * 4 + 100 的结果")
            logger.error(f"错误: {str(e)}")

        # 测试2: 使用天气工具
        logger.info("\n测试2: 使用天气工具")
        try:
            response2 = await agent.ainvoke({"messages": [{"role": "user", "content": "查询北京的天气，详细说明天气状况"}]})
            final_message2 = response2["messages"][-1]
            logger.info(f"查询: 查询北京的天气")
            logger.info(f"回答: {final_message2.content}")
        except Exception as e:
            logger.info(f"查询: 查询北京的天气")
            logger.error(f"错误: {str(e)}")

        # 测试3: 使用当前时间工具
        logger.info("\n测试3: 使用当前时间工具")
        try:
            response3 = await agent.ainvoke({"messages": [{"role": "user", "content": "现在几点了？请以YYYY-MM-DD HH:MM:SS格式显示当前时间"}]})
            final_message3 = response3["messages"][-1]
            logger.info(f"查询: 现在几点了？")
            logger.info(f"回答: {final_message3.content}")
        except Exception as e:
            logger.info(f"查询: 现在几点了？")
            logger.error(f"错误: {str(e)}")

        # 测试4: 使用心愿列表查询工具
        logger.info("\n测试4: 使用心愿列表查询工具")
        try:
            response4 = await agent.ainvoke({"messages": [{"role": "user", "content": "查询所有心愿列表"}]})
            final_message4 = response4["messages"][-1]
            logger.info(f"查询: 查询所有心愿列表")
            logger.info(f"回答: {final_message4.content}")
        except Exception as e:
            logger.info(f"查询: 查询所有心愿列表")
            logger.error(f"错误: {str(e)}")

        # 测试5: 综合旅游规划
        logger.info("\n测试5: 综合旅游规划")
        try:
            #response5 = await agent.ainvoke({"messages": [{"role": "user", "content": "基于我的心愿列表，给我一个三天长春旅游的规划。要求：1.首先查询长春的当前气温和未来几天的天气预报；2.然后查询有什么心愿项目；3.根据气温判断哪些心愿可以实现；4.基于可实现的心愿制定行程计划，每天的规划中包含当天的天气和心愿项目；5.只使用数据库中存在的心愿项目，不要添加任何数据库中没有的项目。"}]})
            response5 = await agent.ainvoke({"messages": [{"role": "user", "content": "基于长春市未来三天的天气和我的心愿列表，根据气温判断哪些心愿可以实现，给我一个三天长春旅游的规划，每天的规划中包含当天的天气和心愿项目。"}]})
            final_message5 = response5["messages"][-1]
            logger.info(f"查询: 基于我的心愿列表，给我一个为期三天的长春市旅游的规划,每天的规划中包含当天的天气和心愿项目")
            logger.info(f"回答: {final_message5.content}")
        except Exception as e:
            logger.info(f"查询: 基于我的心愿列表，给我一个为期三天的长春市旅游的规划,每天的规划中包含当天的天气和心愿项目")
            logger.error(f"错误: {str(e)}")

        logger.info("")
        logger.info("✅ 所有测试完成！")
    except Exception as e:
        logger.error(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
    # 不需要显式关闭 MultiServerMCPClient


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main())