import random
from shared import OrderInfo
from datetime import timedelta
from temporalio import activity
from temporalio.exceptions import ActivityError, ApplicationError

@activity.defn
async def reserve_inventory(order_info: OrderInfo) -> str:
    """Reserve inventory for the order."""
    activity.logger.info(f"reserve_inventory complete for order {order_info.order_id}")   
    return f"Inventory reserved for order {order_info.order_id}"


@activity.defn
async def release_inventory(order_info: OrderInfo) -> str:
    """Release inventory for the order."""
    activity.logger.info(f"release_inventory complete for order {order_info.order_id}")   
    return f"Inventory released for order {order_info.order_id}"


@activity.defn
async def charge_customer(order_info: OrderInfo) -> str:
    """Charge the customer for the order."""
    
    # Simulate a random failure to demonstrate rollback
    result = random.choice([True, False])

    if not result:
        # Log a clean message for the activity failure
        activity.logger.info("Charge denied for order %s", order_info.order_id)
        raise ApplicationError(
            "Order canceled.",
            type="ChargeDenied",
            non_retryable=True
        )
    activity.logger.info(f"charge_customer complete for order {order_info.order_id}")
    return f"Customer charged for order {order_info.order_id}"


@activity.defn
async def pack_and_ship_package(order_info: OrderInfo) -> str:
    """Pack and ship the package."""
    activity.logger.info(f"pack_and_ship_package complete for order {order_info.order_id}")
    return f"Package packed and shipped for order {order_info.order_id}"


@activity.defn
async def notify_customer(order_info: OrderInfo) -> str:
    """Notify the customer about the order."""
    activity.logger.info(f"notify_customer complete for order {order_info.order_id}")
    return f"Customer notified for order {order_info.order_id}"
