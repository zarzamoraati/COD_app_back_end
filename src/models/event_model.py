from datetime import date
from pydantic import BaseModel, Field
from typing import List,Optional, Union
import uuid
from typing import TypedDict
from datetime import datetime

class Event(BaseModel):
    id:Optional[str]=Field(default_factory=lambda : str(uuid.uuid4()))
    date:Optional[datetime]=Field(default_factory=lambda :datetime.today())
    time: Union[float,int]=Field(default=0)
    
    

class RecordEvents(BaseModel):
    name:str= Field(description="The name of the event",default="")
    goal_time:Union[float,int]=Field(description="The desire time you want to spend on that situation (in min)",default=0)
    record:Optional[List[Event]]=Field(default=[])


class EventResponse(TypedDict):
    id_event:str