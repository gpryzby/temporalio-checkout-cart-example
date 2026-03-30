import random
from shared import OrderInfo
from datetime import timedelta
from temporalio import activity
from temporalio.exceptions import ActivityError, ApplicationError

@activity.defn(name="reserve_inventory")
async def reserve_inventory(order_info: OrderInfo) -> str:
    """Reserve inventory for the order."""
    print(f"reserve_inventory complete for order {order_info.order_id}")   
    return f"Inventory reserved for order {order_info.order_id}"


@activity.defn(name="charge_customer")
async def charge_customer(order_info: OrderInfo) -> str:
    """Charge the customer for the order."""
    
    # Simulate a random failure to demonstrate rollback
    result = random.choice([True, False])

    if not result:
        raise ApplicationError(
            "Charge denied. Order canceled.",
            type="ChargeDenied",
            non_retryable=True
            )
    print(f"charge_customer complete for order {order_info.order_id}")
    return f"Customer charged for order {order_info.order_id}"


@activity.defn(name="pack_and_ship_package")
async def pack_and_ship_package(order_info: OrderInfo) -> str:
    """Pack and ship the package."""
    print(f"pack_and_ship_package complete for order {order_info.order_id}")
    return f"Package packed and shipped for order {order_info.order_id}"


@activity.defn(name="notify_customer")
async def notify_customer(order_info: OrderInfo) -> str:
    """Notify the customer about the order."""
    print(f"notify_customer complete for order {order_info.order_id}")
    return f"Customer notified for order {order_info.order_id}"