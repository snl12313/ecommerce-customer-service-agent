import os
import json
from utils.logger_handler import logger
from datetime import datetime, timedelta
from utils.config_data import root_path
from langchain_core.tools import tool
from rag.rag_service import RagSummarizeService

rag = RagSummarizeService()


@tool(description="查询店铺的商品信息、退换货政策、物流说明和常见问题")
def rag_summarize(query: str) -> str:
    return rag.rag_summarize(query)

@tool(description="根据订单号查询订单状态、物流信息和金额")
def query_order(order_id: str) -> str:
    data_path = root_path("data", "external", "json", "orders.json")

    try:
        with open(data_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except FileNotFoundError:
        return "订单数据文件不存在，请联系客服。"

    results = [o for o in orders if o.get("order_id") == order_id]
    if not results:
        return f"未找到订单号为 {order_id} 的订单。"

    order = results[0]
    logistics = order.get("logistics")
    logistics_info = f"{logistics['company']} {logistics['tracking_no']}" if logistics else "暂无物流信息"

    return (
        f"订单号：{order['order_id']}\n"
        f"商品：{order['product']}\n"
        f"金额：{order['amount']}元\n"
        f"状态：{order['status']}\n"
        f"物流：{logistics_info}\n"
        f"下单时间：{order['create_time']}\n"
        f"支付时间：{order.get('pay_time') or '暂无'}\n"
        f"发货时间：{order.get('ship_time') or '暂无'}\n"
        f"送达时间：{order.get('deliver_time') or '暂无'}\n"
        f"签收时间：{order.get('sign_time') or '暂无'}"
    )

@tool(description="为已签收的订单提交退货申请。入参order_id为订单号，例如ORD20260825011")
def submit_return(order_id: str) -> str:
    data_path = root_path("data", "external", "json", "orders.json")
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except FileNotFoundError:
        return "订单数据文件不存在，请联系客服。"

    results = [o for o in orders if o.get("order_id") == order_id]
    if not results:
        return f"未找到订单号为 {order_id} 的订单。"

    order = results[0]

    if order.get("status") != "已签收":
        return f"订单 {order_id} 当前状态为「{order.get('status')}」，仅已签收的订单可申请退货。"

    sign_time_str = order.get("sign_time")
    if not sign_time_str:
        return "未找到签收时间，无法办理退货。"

    sign_time = datetime.strptime(sign_time_str, "%Y-%m-%d %H:%M:%S")
    if datetime.now() - sign_time > timedelta(days=7):
        return f"订单 {order_id} 签收已超过7天，不在退货期限内，无法办理退货。"

    return_id = f"RT{datetime.now().strftime('%Y%m%d%H%M%S')}"
    logger.info(f"退货申请已提交，订单号：{order_id}，售后单号：{return_id}")
    return f"退货申请已提交成功！售后单号：{return_id}，订单号：{order_id}，商品：{order.get('product')}，金额：{order.get('amount')}元。请在7天内寄回商品。"

