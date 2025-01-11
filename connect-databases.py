import pymongo
import redis
from neo4j import GraphDatabase
import json

# MongoDB connection
def connect_mongo():
    mongo_uri = "mongodb+srv://followalong:Password123@cluster0.8z7h2.mongodb.net/"
    client = pymongo.MongoClient(mongo_uri)
    db = client['project_ecommerce']
    return db

# Redis connection
def connect_redis():
    redis_host = "redis-17105.c267.us-east-1-4.ec2.redns.redis-cloud.com"
    redis_port = 17105
    redis_password = "I4Ftkmbo1mIuIIzAgBdnH8V43RpCNXiY"
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    return redis_client

# Neo4j connection
def connect_neo4j():
    uri = "neo4j+s://bf068998.databases.neo4j.io"
    username = "neo4j"
    password = "f6qT-r10Q-X_XmPoMoDfuvEyYiFSyFSiz5BrmCMHgOQ"
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver

# Fetch data from MongoDB
def fetch_user_data_from_mongo(db, user_id):
    return db.users.find_one({"_id": user_id})

def fetch_product_data_from_mongo(db):
    return list(db.products.find())

# Fetch data from Redis
def fetch_user_data_from_redis(redis_client, user_id):
    user_data = redis_client.get(f"user:{user_id}:data")
    return json.loads(user_data) if user_data else None

# Fetch data from Neo4j
def fetch_user_data_from_neo4j(driver, user_id):
    with driver.session() as session:
        result = session.run("MATCH (u:User {id: $user_id}) RETURN u", user_id=user_id)
        return result.single()

# Insert User and Product Data into Neo4j
def insert_user_data_neo4j(driver, user_data):
    with driver.session() as session:
        session.run(
            "CREATE (u:User {id: $id, name: $name, email: $email, address: $address})",
            id=user_data["_id"],
            name=user_data["name"],
            email=user_data["email"],
            address=user_data["address"]
        )

def insert_product_data_neo4j(driver, product_data):
    with driver.session() as session:
        for product in product_data:
            session.run(
                "CREATE (p:Product {id: $id, name: $name, price: $price, category: $category, description: $description})",
                id=product["_id"],
                name=product["name"],
                price=product["price"],
                category=product["category"],
                description=product["description"]
            )

# Create relationships between User and Products in Neo4j
def create_user_product_relationship(driver, user_id, product_ids):
    with driver.session() as session:
        for product_id in product_ids:
            session.run(
                "MATCH (u:User {id: $user_id}), (p:Product {id: $product_id}) "
                "CREATE (u)-[:VIEWED]->(p)",
                user_id=user_id,
                product_id=product_id
            )

# Main function
def main():
    # Connect to MongoDB
    mongo_db = connect_mongo()

    # Connect to Redis
    redis_client = connect_redis()

    # Connect to Neo4j
    neo4j_driver = connect_neo4j()

    # Fetch user data from MongoDB
    user_data = fetch_user_data_from_mongo(mongo_db, "u1")
    print(f"User Data from MongoDB: {user_data}")

    # Fetch product data from MongoDB
    product_data = fetch_product_data_from_mongo(mongo_db)
    print(f"Product Data from MongoDB: {product_data}")

    # Fetch user data from Redis
    user_data_from_redis = fetch_user_data_from_redis(redis_client, "u1")
    print(f"User Data cached in Redis: {user_data_from_redis}")

    # Insert data into Neo4j
    insert_user_data_neo4j(neo4j_driver, user_data)
    insert_product_data_neo4j(neo4j_driver, product_data)
    print("User and Product data created in Neo4j.")

    # Create relationships in Neo4j
    create_user_product_relationship(neo4j_driver, "u1", ["1", "2"])
    print("Relationships created between user and products in Neo4j.")

if __name__ == "__main__":
    main()
