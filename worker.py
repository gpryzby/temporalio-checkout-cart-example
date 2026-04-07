#!/usr/bin/env python3
"""Worker script to run the Temporalio workflow worker."""

import asyncio
import logging
from temporalio.worker import Worker
from temporalio.client import Client
from workflow import OrderProcessingWorkflow
from activities import reserve_inventory, release_inventory, charge_customer, pack_and_ship_package, notify_customer

async def main():
    """Main function to start the Temporalio worker."""
    
    logging.basicConfig(level=logging.INFO)
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Create worker that listens on the default "order-processing-task-queue"
    worker = Worker(
        client=client,
        task_queue="order-processing-task-queue",
        workflows=[OrderProcessingWorkflow],
        activities=[
            reserve_inventory,
            release_inventory,
            charge_customer,
            pack_and_ship_package,
            notify_customer,
        ],
    )
    
    print("Worker started successfully")
    print("Worker is ready to process workflows...")
    
    # The worker will run indefinitely
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())