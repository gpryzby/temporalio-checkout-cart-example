#!/usr/bin/env python3
"""Starter script for the Temporalio order processing workflow."""

import asyncio
import sys
from datetime import timedelta
from temporalio.client import Client

# Import our workflow and dataclass
from workflow import OrderProcessingWorkflow
from shared import OrderInfo

async def main():
    """Main function to start the workflow."""
    if len(sys.argv) != 2:
        print("Usage: python starter.py <order_id>")
        sys.exit(1)
    
    order_id = sys.argv[1]
    
    # Create order information
    # This is a simple example; in a real application, you would likely fetch this information from a database or another service.
    order_info = OrderInfo(
        order_id=order_id,
        name="Test Customer",
        notification_method="email",
        notification_value="test@example.com"
    )
    
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Start the workflow
    workflow_id = f"order-workflow-{order_id}"
    task_queue = "order-processing-task-queue"
    
    print(f"Starting workflow for order {order_id}")
    
    try:
        # Run the workflow
        result = await client.start_workflow(
            OrderProcessingWorkflow.run,
            order_info,
            id=workflow_id,
            task_queue=task_queue,
        )
        
        print(f"Workflow started successfully. Workflow ID: {workflow_id}")
        print("Waiting for workflow completion...")
        
        # Wait for workflow completion
        workflow_result = await client.get_workflow_handle(workflow_id).result()
        print(f"Workflow completed with result: {workflow_result}")
        
    except Exception as e:
        print(f"Error starting workflow: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())