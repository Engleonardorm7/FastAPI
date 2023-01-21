#Pytgon
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field


#FastAPI
from fastapi import FastAPI
from fastapi import Body
from fastapi import Query, Path

app = FastAPI()

#Models
class HairColor(Enum):
    white="white"
    brown="brown"
    blonde="blonde"
    red="red"

class Location(BaseModel):
    city: str
    state: str
    country: str

class Person(BaseModel):
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Leonardo"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Suarez"
    )
    age: int = Field(
        ...,
        gt=0,
        Le=115,
        example=21
    )
    hair_color:Optional[HairColor]=Field(default=None,example="blonde")
    is_married: Optional[bool]=Field(default=None, example=False)
    password: str=Field(...,min_length=8)#... significa obligatorio
    

    # class Config: 
    #     schema_extra={
    #         "example":{
    #             "first_name":"Leonardo",
    #             "last_name":"Rodriguez",
    #             "age":29,
    #             "hair_color":"brown",
    #             "is_married":False
    #         }
    #     }

@app.get("/") #path operation decorator
def home():
    return {"Hello": "World"}

    #request and response body

@app.post("/person/new")
def create_person(person:Person=Body(...)):
    return person

#Validaciones: Query Parameters
@app.get("/person/detail")
def show_person(
    name:Optional[str]=Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio"
        ),
    age:str=Query(
        ...,
        title="Person Age",
        description= "This is the person age. It's required",
        example=25
        
        )
):
    return {name:age}

#validaciones: Path Parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int=Path(
        ...,
        gt=0,
        example=7
        )
):
    return{person_id:"It exist!"}
#Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id:int=Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=77
    ),
    person:Person=Body(...),
    #location:Location=Body(...)
):
    #results=person.dict()
    #results.update(location.dict())
    #return results
    return person