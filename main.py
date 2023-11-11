from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind='bulldog'),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return "Hello, wrld!"

@app.post('/post')
def post():
    last_post = post_db[len(post_db) - 1].copy()
    last_post.id += 1
    last_post.timestamp += 1
    post_db.append(last_post)
    return post_db

@app.post('/dog')
def post_dog(dog: Dog):
    dogs_db[dog.pk] = dog
    return dog

@app.get('/dog/{id}')
def get_dog_by_id(id: int):
    if id not in dogs_db:
        raise HTTPException(status_code=422, detail="Dog not found")
    return dogs_db[id]

@app.get('/dog', summary='Get Dogs')
def get_dog_by_kind(kind: DogType = None):
    if kind is None:
        return list(dogs_db.values())
    return list(filter(lambda dog: dog.kind == kind, dogs_db.values()))

@app.patch('/dog/{id}')
def update_dog(id: int, dog: Dog):
    dogs_db[dog.pk] = dog
    return dog
