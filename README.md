# Temporalio Order Processing Workflow

This project implements a SA technical interview use case of a Temporalio workflow for processing e-commerce orders with the following steps:
1. Reserve inventory
2. Charge customer
3. Pack and ship package
4. Notify customer

## Architecture Overview

The solution consists of the following components:

1. **OrderInfo Dataclass** (`shared.py`):
   - Defines the structure for order information
   - Uses dataclass for clean, readable code
   - Designed for backwards compatibility with future changes

2. **Activities** (`activities.py`):
   - Contains four activity functions: reserve_inventory, charge_customer, pack_and_ship_package, and notify_customer
   - Each activity is implemented as a separate function
   - Each activity is currently a stub that prints "<activity name> complete"

3. **Workflow Implementation** (`workflow.py`):
   - Defines the `OrderProcessingWorkflow` that orchestrates the order processing steps
   - Uses the `@workflow.run` decorator
   - Imports and uses the activities from activities.py

4. **Starter Script** (`starter.py`):
   - Accepts order_id as command line argument
   - Creates order information with default values (in production the `order_id` would be used to lookup the information about the customer and payment infomation if saved or query the customer for payment)
   - Connects to Temporal server and starts the workflow

## How to Run

1. Ensure Temporal server is running on port 7233 
2. Create your virtual environment:
   ```bash
   python3 -m venv .venv
   ```
3. Activate your virtual environment:
   ```bash
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt (prepend uv if Debian based distros)
   ```
5. Start docker instance:
   ``` bash
   docker run --rm -p 7233:7233 -p 8233:8233 temporalio/temporal:latest server start-dev --ip 0.0.0.0
   ```
6. Start worker:
   ``` bash
   python3 worker.py
   ```
7. Start the workflow:
   ```bash
   python starter.py <order_id>
   ```

## Key Features

- **Non-deterministic Activities**: Each activity is designed to handle external dependencies
- **Backwards Compatibility**: The dataclass approach allows for easy extension
- **Timeouts**: Proper timeouts configured for each activity to prevent hanging
- **Error Handling**: Basic error handling in the starter script
- **Modular Design**: Clear separation of concerns between data, workflow, and execution

## File Structure

- `shared.py`: Contains the OrderInfo dataclass
- `activities.py`: Contains all activity implementations
- `workflow.py`: Contains the workflow definition
- `starter.py`: Script to start workflow execution
- `worker.py`: Script to run the Temporalio worker
- `requirements.txt`: Project dependencies
- `test_workflow.py`: Test script to verify functionality

## Workflow Steps

1. **reserve_inventory**: Prints "reserve_inventory complete"
2. **charge_customer**: Prints "charge_customer complete"
3. **pack_and_ship_package**: Prints "pack_and_ship_package complete"
4. **notify_customer**: Prints "notify_customer complete"

Each activity prints its completion message as specified in the requirements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
