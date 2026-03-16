from pydantic import BaseModel


class UserCreate(BaseModel):
    file_id:int
    vendor_name: str
    

class UserResponse(BaseModel):
    file_id: int
    vendor_name:str
    

    class Config:
        orm_mode = True