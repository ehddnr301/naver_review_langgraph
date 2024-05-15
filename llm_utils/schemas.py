from langchain_core.pydantic_v1 import BaseModel, Field


class PlaceAndFood(BaseModel):
    """Place And Food."""

    place: str = Field(
        description="대화에서 나온 확실한 지역명 필드. 대화에서 지역명이 확실히 지정되지 않은 경우, '강남역'을 사용한다."
    )
    food: str = Field(
        description="""
            대화에서 나온 확실한 음식명 필드. 대화에서 음식명이 확실히 지정되지 않은 경우, 음식카테고리중 하나를 골라 사용한다: '패스트 푸드', '한식', '일식', '중식', '베트남식', '맛집'
        """
    )
