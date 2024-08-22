import pymongo # type: ignore[import-not-found]

MONGODB_URI = "mongodb+srv://darshanvkalola:dIsy3F4z0CgYGqFh@cluster0.7ouqu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongodb_client = pymongo.MongoClient(MONGODB_URI)
