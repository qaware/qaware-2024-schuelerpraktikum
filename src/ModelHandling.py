from bson import ObjectId
from pydantic import BaseModel, Field


class SensorDataModel(BaseModel):
    name: str = Field(...),
    type: str = Field(...),
    pressure: float = Field(...)
    temperature: float = Field(...)
    timestamp: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "thruster.01b",
                "type": "thruster",
                "temperature": 1.23,
                "pressure": 5.78,
                "timestamp": 12328
            }
        }


class ModelMapper():
    def model_to_dict(self, model):
        return model.dict()

    def dict_to_model(self, dict):
        return SensorDataModel.parse_obj(dict)
