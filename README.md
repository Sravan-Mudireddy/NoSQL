# Multi-Database Integration for an E-commerce Use Case

---

## Introduction
This project demonstrates the integration of MongoDB (Document Model), Redis (Key-Value Store), and Neo4j (Graph Database) in an e-commerce application. The aim is to show how these databases can work together for efficient data handling.

---

## Use Case
The project simulates an e-commerce application where:
1. **MongoDB** stores user and product data.
2. **Redis** caches user data for quick access.
3. **Neo4j** tracks user-product interactions.

---

## Project Workflow
1. Data is inserted into each database using initialization queries.
2. The main script retrieves user data from MongoDB, caches it in Redis, and tracks interactions in Neo4j.
3. Outputs are displayed, showing data fetched from all three databases.

---

## Setup and Installation
1. Clone the repository:  
2. Install Dependencies
   ```bash
   pip install -r requirements.txt

4. Database Configurations

    1. **MongoDB**: Configure your connection string in the script. Use the cluster URI provided.
    2. **Redis**: Set up the Redis host, port, and password.
    3. **Neo4j**: Provide your instance URI, username, and password in the script.


5. Insert Initial Data
Insert data into MongoDB, Redis, and Neo4j using the provided queries in the queries/ directory.

6. Run the Main Script
Execute the main script to see the data flow between databases:
