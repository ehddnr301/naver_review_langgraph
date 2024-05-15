from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_tools import (
    PydanticToolsParser,
)

from .schemas import PlaceAndFood
from .tools import crawl_restaurants

# Extractor
parser_pydantic = PydanticToolsParser(tools=[PlaceAndFood])

llm = ChatOpenAI()

extract_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 사용자의 입력에 맞는 좋은 음식점을 찾을 수 있는 적절한 검색어를 생성하는 Assistance이다.
                사용자의 입력에 대해 음식점 관련 검색어를 생성하는 것이 당신의 필수적인 역할입니다.
            """,
        ),
        MessagesPlaceholder(variable_name="search_query"),
        (
            "system",
            "위 유저 Input에 맞는 적절한 지역명과 음식이름을 생성해줘",
        ),
    ]
)

initial_extractor = extract_prompt | llm.bind_tools(
    tools=[PlaceAndFood], tool_choice="PlaceAndFood"
)

extract_chain = initial_extractor | parser_pydantic

# Searcher
search_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 Extractor가 생성한 검색어를 기반으로 음식점을 검색하는 Assistance이다.
                주어진 검색어를 기반으로 음식점을 검색하는 것이 당신의 필수적인 역할입니다.
            """,
        ),
        MessagesPlaceholder(variable_name="search_term"),
        (
            "system",
            "위의 검색어를 기반으로 음식점을 검색해주세요."
            "다음 tool을 사용할 수 있습니다: crawl_restaurants - 검색어를 기반으로 음식점을 크롤링할 수 있습니다.",
        ),
    ]
)

tools = [crawl_restaurants]

search_chain = search_prompt | llm.bind_tools(tools)

# Recommender

recommend_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 검색결과를 바탕으로 사용자에게 식당을 추천하는 Assistance이다.
                적절한 식당을 추천하는 것이 당신의 필수적인 역할입니다.
            """,
        ),
        MessagesPlaceholder(variable_name="restaurants_list"),
        (
            "system",
            "위 맛집 목록을 바탕으로 맛집을 추천해주세요",
        ),
    ]
)

recommend_chain = recommend_prompt | llm
