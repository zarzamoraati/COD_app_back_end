from fastapi import FastAPI , HTTPException
from db.pymongodb import  client, close_connection
from fastapi import FastAPI
from models.event_model import Event,RecordEvents,EventResponse
from typing import TypedDict
from typing import Union
from bson import ObjectId
from utils.serialize_docs import serialize_documents

db = client["DB2"]
collection = db["db2_collection"]

app = FastAPI()

@app.get("/")
def home_page():
    return "home page"

## TODO add event endpoint

@app.post("/add-event")
def add_event(message:RecordEvents)->Union[str, EventResponse]:
    consult = collection.find_one({"name":message.name})
    if consult is not None:
        return "Event already exists in DB"
    
    response=collection.insert_one({"name":message.name,"goal_time":message.goal_time,"record":[]})
    print(response)
    return {"id_event":str(response.inserted_id)}


## TODO add a new record 

@app.post("/new-record/{id}")
def add_record(id:str,new_record:Event):
    ## Convert id to ObjectId
    try:
        obj_id=ObjectId(id)
    except:
        return HTTPException(status_code=400,detail="Invalid Format")
    ## search in the collection
    document = collection.find_one({"_id":obj_id})
    ## asses if document exist
    if document is None:

        return HTTPException(status_code=404,detail="Document with id : {id} down't exist in collection")
    ## add new record to the collection
    document["record"].append(new_record.dict())

    ## update document 
    result=collection.update_one({"_id":obj_id},{"$set":{"record":document["record"]}})

    ## assess update

    if result.matched_count == 0:
        raise HTTPException(status_code=404,detail=f"Failed to update the document with id :{id}")
    return "Record added succesfully"


##TODO consult all events
@app.get("/event")
def consult_events():
    cursor=collection.find({})
    ## convert cursor to list 
    events=list(cursor)
    ## serialize events
    serialized_events=[serialize_documents(event) for event in events]
    return {"events":serialized_events}

##TODO consult one event

@app.get("/event/{id}")
def consult_event(id:str):
    try:
        object_id=ObjectId(id)
    except:
        return HTTPException(status_code=400, detail="Invalid id format")
    
    event=collection.find_one({"_id":object_id})
    if event is None:
        return HTTPException(status_code=400, detail="The event with id {id} is not in collection")
    
    return {"event":str(event)}





##TODO delete event endpoint

    
     
    
    
    
    





