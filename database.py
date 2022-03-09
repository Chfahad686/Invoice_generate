from pymongo import MongoClient

mdb_client = MongoClient(host="mongodb+srv://safiulm123:G6seconds!@cluster0.mnzwa.mongodb.net/symmi?retryWrites=true&w=majority", connect=False)
dbName = 'Invoice_Generate'
db = mdb_client["Invoice_Generate"]