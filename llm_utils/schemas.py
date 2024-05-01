from langchain_core.pydantic_v1 import BaseModel, Field


class PlaceAndFood(BaseModel):
    """Place And Food."""

    place: str = Field(description="The name of the area from the conversation")
    food: str = Field(description="The name of the food from the conversation")
