from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError
from shared import OrderInfo
from activities import reserve_inventory, release_inventory, charge_customer, pack_and_ship_package, notify_customer
import logging

@workflow.defn
class OrderProcessingWorkflow:
    """Workflow for processing an order through inventory reservation, payment, shipping, and notification."""
    
    @workflow.run
    async def run(self, order_info: OrderInfo) -> str:
        """Main workflow method that orchestrates the order processing steps."""
        workflow.logger.info(f"OrderProcessing workflow invoked")
        
        # Step 1: Reserve inventory
        await workflow.execute_activity(
            reserve_inventory,
            order_info,
            start_to_close_timeout=timedelta(seconds=10)
        )

        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        await workflow.sleep(timedelta(seconds=3))

        # Step 2: Charge customer
        try:
            await workflow.execute_activity(
                charge_customer,
                order_info,
                start_to_close_timeout=timedelta(seconds=10),
                # Configure no retries for this activity ONLY for the similation. This can be updated to try multiple times in a real application.
                retry_policy=RetryPolicy(
                    maximum_attempts=1,
                    )
                )

        except ActivityError as e:
            # If charge fails, the workflow releases inventory and handles the error gracefully
            await workflow.execute_activity(
                release_inventory,
                order_info,
                start_to_close_timeout=timedelta(seconds=10)
            )
            # Re-raise the original error to fail the workflow
            raise e.cause

        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        await workflow.sleep(timedelta(seconds=3))
        
        # Step 3: Pack and ship package
        await workflow.execute_activity(
            pack_and_ship_package,
            order_info,
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        await workflow.sleep(timedelta(seconds=3))

        # Step 4: Notify customer
        await workflow.execute_activity(
            notify_customer,
            order_info,
            start_to_close_timeout=timedelta(seconds=10)
        )
        
        return f"Order {order_info.order_id} processed successfully"
