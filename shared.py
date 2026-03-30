from dataclasses import dataclass
from typing import Optional

@dataclass
class OrderInfo:
    """Dataclass for order information to ensure backwards compatibility."""
    order_id: str
    name: str
    notification_method: str
    notification_value: str