import pymongo

def connect_to_mongodb(database_name, collection_name):
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[database_name]
        collection = db[collection_name]
        return collection
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def fetch_data_from_mongodb(collection):
    try:
        # Fetch data from MongoDB
        data = list(collection.find())
        return data
    except Exception as e:
        print(f"Error fetching data from MongoDB: {e}")
        return None
