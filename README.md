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

5. **Worker Script** (`worker.py`):
   - Script to run the Temporalio worker
   - Connects to Temporal server and registers the workflow and activities

## How to Run with Docker

1. Ensure Docker and Docker Compose are installed
2. Start the Temporal server and worker:
   ```bash
   docker-compose up -d
   ```
3. Start a workflow:
   ```bash
   docker-compose run --rm starter
   ```
4. To run with a specific order ID:
   ```bash
   docker-compose run --rm starter python starter.py your-order-id-here
   ```
5. To stop all services:
   ```bash
   docker-compose down
   ```

## Key Features

- **Non-deterministic Activities**: Each activity is designed to handle external dependencies
- **Backwards Compatibility**: The dataclass approach allows for easy extension
- **Timeouts**: Proper timeouts configured for each activity to prevent hanging
- **Error Handling**: Basic error handling in the starter script
- **Modular Design**: Clear separation of concerns between data, workflow, and execution
- **Docker Support**: Complete Docker setup for easy deployment

## File Structure

- `shared.py`: Contains the OrderInfo dataclass
- `activities.py`: Contains all activity implementations
- `workflow.py`: Contains the workflow definition
- `starter.py`: Script to start workflow execution
- `worker.py`: Script to run the Temporalio worker
- `requirements.txt`: Project dependencies
- `Dockerfile`: Docker configuration for the application
- `docker-compose.yml`: Docker Compose configuration for running Temporal server, worker, and starter

## Workflow Steps

1. **reserve_inventory**: Prints "reserve_inventory complete"
2. **charge_customer**: Prints "charge_customer complete"
3. **pack_and_ship_package**: Prints "pack_and_ship_package complete"
4. **notify_customer**: Prints "notify_customer complete"

Each activity prints its completion message as specified in the requirements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
