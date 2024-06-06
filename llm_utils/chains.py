from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers.openai_tools import (
    PydanticToolsParser,
)

from .schemas import PlaceAndFood
from .tools import crawl_restaurants, query_restaurants

# Extractor
parser_pydantic = PydanticToolsParser(tools=[PlaceAndFood])

llm = ChatOpenAI(model="gpt-4o")

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
            "다음 tool을 사용할 수 있습니다:"
            "crawl_restaurants - 검색어를 기반으로 음식점을 크롤링할 수 있습니다."
            "query_restaurants - 검색어를 기반으로 음식점을 DB에서 쿼리할 수 있습니다."
            "아래 툴을 사용해주세요",
        ),
        MessagesPlaceholder(variable_name="tool_choice"),
    ]
)

tools = [crawl_restaurants, query_restaurants]

search_chain = search_prompt | llm.bind_tools(tools)

# Recommender

recommend_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
                너는 검색결과를 바탕으로 사용자에게 식당을 추천하는 Assistance이다.
                적절한 식당을 추천하는 것이 당신의 필수적인 역할입니다.
                응답은 아래 형태를 유지해야 합니다.
                
                **음식점 이름**
                음식점의 주요 리뷰 카테고리: 리뷰 카테고리 정보
                음식점의 위치: 위치 정보
                음식점의 영업시간: 영업시간 정보
                음식점의 편의시설 및 서비스: 편의시설 및 서비스 정보
                음식점의 네이버 예약 가능 여부: 네이버 예약 가능 여부 정보
                음식점의 리뷰 내용 요약
                1. 리뷰 내용 요약 1
                2. 리뷰 내용 요약 2
                3. 리뷰 내용 요약 3
                
                아래 내용을 지켜 응답해주세요.
                1. 위에서 정의된 내용외에는 적지않아야합니다.
            """,
        ),
        MessagesPlaceholder(variable_name="user_input"),
        (
            "system",
            "위 유저의 요구사항을 만족하여, 아래 검색된 맛집 목록을 중에서 추천해주세요"
            "유저의 요구사항을 만족하는 맛집이 없다면 '해당하는 맛집이 없습니다'라고 응답해주세요.",
        ),
        MessagesPlaceholder(variable_name="restaurants_list"),
    ]
)

recommend_chain = recommend_prompt | llm
