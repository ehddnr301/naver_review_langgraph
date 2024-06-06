from langchain_core.pydantic_v1 import BaseModel, Field


class PlaceAndFood(BaseModel):
    """Place And Food."""

    place: str = Field(
        description="대화에서 나온 확실한 지역명 필드. 대화에서 지역명이 확실히 지정되지 않은 경우, '분류불가' 를 사용한다."
    )

    food: str = Field(
        description="""
            대화에서 나온 확실한 음식명 필드. 대화에서 음식명이 확실히 지정되지 않은 경우, 다음 음식 카테고리 키워드를 사용한다. : '한식', '일식', '중식', '양식', '분식', '맛집', '분류불가'
        """
    )
