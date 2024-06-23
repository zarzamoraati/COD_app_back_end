def serialize_documents(document):
    if "_id" in document:
        document["_id"]=str(document["_id"])

    return document
    