from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from shared import OrderInfo
from activities import reserve_inventory, charge_customer, pack_and_ship_package, notify_customer

@workflow.defn
class OrderProcessingWorkflow:
    """Workflow for processing an order through inventory reservation, payment, shipping, and notification."""
    
    @workflow.run
    async def run(self, order_info: OrderInfo) -> str:
        """Main workflow method that orchestrates the order processing steps."""
        
        # Step 1: Reserve inventory
        await workflow.execute_activity(
            reserve_inventory,
            order_info,
            start_to_close_timeout=timedelta(seconds=3)
        )

        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        print(f"Sleep to allow canceling workflow to test durability before charging customer")
        await workflow.sleep(timedelta(seconds=3))

        # Step 2: Charge customer
        try:
            await workflow.execute_activity(
                charge_customer,
                order_info,
                start_to_close_timeout=timedelta(seconds=10),
                # ApplicationError should cause workflow to fail immediately
                # Configure no retries for this activity
                retry_policy=RetryPolicy(
                    maximum_attempts=1,
                    )
                )
        except Exception as e:
            # If charge fails, the workflow should exit
            print(f"Workflow failed due to charge error: {e}")
            # Re-raise the exception to fail the workflow
            raise

        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        print(f"Sleep to allow canceling workflow to test durability before packing and shipping package")
        await workflow.sleep(timedelta(seconds=3))
        
        # Step 3: Pack and ship package
        await workflow.execute_activity(
            pack_and_ship_package,
            order_info,
            start_to_close_timeout=timedelta(hours=4)
        )
        
        # Sleep for testing purposes to simulate a long-running workflow and demonstrate Temporal's durability
        print(f"Sleep to allow canceling workflow to test durability before notifying customer")
        await workflow.sleep(timedelta(seconds=3))

        # Step 4: Notify customer
        await workflow.execute_activity(
            notify_customer,
            order_info,
            start_to_close_timeout=timedelta(minutes=5)
        )
        
        return f"Order {order_info.order_id} processed successfully"