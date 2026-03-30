#!/usr/bin/env python3
"""Test script to verify workflow behavior with ApplicationError."""

import asyncio
import sys
from datetime import timedelta
from temporalio.client import Client
from temporalio.exceptions import ApplicationError

# Import our workflow and dataclass
from workflow import OrderProcessingWorkflow
from shared import OrderInfo

async def test_workflow_with_application_error():
    """Test that workflow exits when ApplicationError is raised."""
    
    # Create order information
    order_info = OrderInfo(
        order_id="test-123",
        name="Test Customer",
        notification_method="email",
        notification_value="test@example.com"
    )
    
    # Connect to Temporal server
    client = await Client.connect("localhost:7233")
    
    # Start the workflow
    workflow_id = f"order-workflow-test-123"
    task_queue = "order-processing-task-queue"
    
    print("Starting workflow test with ApplicationError...")
    
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
        print(f"Workflow failed as expected: {e}")
        # This is what we want to see - the workflow should fail when ApplicationError is raised
        return True
    
    return False

if __name__ == "__main__":
    asyncio.run(test_workflow_with_application_error())