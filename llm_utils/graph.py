from dotenv import load_dotenv

from typing import Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode

import redis

load_dotenv()

from llm_utils.chains import extract_chain, search_chain, recommend_chain
from llm_utils.tools import crawl_restaurants, query_restaurants

my_redis = redis.Redis(
    host="redis", password="pseudolab", port=6379, decode_responses=True
)

EXTRACT = "extract"
SEARCH = "search"
GET_RESTAURANTS = "get_restaurants"
RECOMMEND = "recommend"

tool_node = ToolNode([crawl_restaurants, query_restaurants])


def extract_node(state: Sequence[BaseMessage]):
    res = extract_chain.invoke(input={"search_query": [state[-1].content]})
    search_query = " ".join(list(res[0].dict().values()))
    if "분류불가" in search_query:
        return "잘 이해하지 못했어요. 다시 말씀해주세요."
    else:
        my_redis.lpush("search_term", search_query)
        return search_query


def search_node(state: Sequence[BaseMessage]):
    if len(state) > 10:
        raise ValueError("Too many iterations")
    search_term = state[-1].content if len(state) < 4 else state[1].content
    tool_choice = "query_restaurants" if len(state) < 4 else "crawl_restaurants"
    res = search_chain.invoke(
        input={"search_term": [search_term], "tool_choice": [tool_choice]}
    )

    return res


def recommend_node(state: Sequence[BaseMessage]):

    res = recommend_chain.invoke(
        input={
            "user_input": [state[0].content],
            "restaurants_list": [state[-1].content],
        }
    )

    return res


def decide_node(state: Sequence[BaseMessage]):
    content = state[-1].content
    if content == "":
        return SEARCH
    else:
        return RECOMMEND


def decide_node_extract(state: Sequence[BaseMessage]):
    content = state[-1].content

    if content == "잘 이해하지 못했어요. 다시 말씀해주세요.":
        return END
    else:
        return SEARCH


def decide_node_recommend(state: Sequence[BaseMessage]):
    content = state[-1].content

    if "맛집이 없습니다" in content:
        return SEARCH
    else:
        return END


from langgraph.graph import END, MessageGraph

builder = MessageGraph()
builder.add_node(EXTRACT, extract_node)
builder.add_node(SEARCH, search_node)
builder.add_node(RECOMMEND, recommend_node)
builder.add_node(GET_RESTAURANTS, tool_node)

builder.set_entry_point(EXTRACT)

builder.add_conditional_edges(
    EXTRACT,
    decide_node_extract,
    {
        SEARCH: SEARCH,
        END: END,
    },
)
builder.add_edge(SEARCH, GET_RESTAURANTS)
builder.add_conditional_edges(
    GET_RESTAURANTS,
    decide_node,
    {
        RECOMMEND: RECOMMEND,
        SEARCH: SEARCH,
    },
)
builder.add_conditional_edges(
    RECOMMEND,
    decide_node_recommend,
    {
        SEARCH: SEARCH,
        END: END,
    },
)

graph = builder.compile()

__all__ = ["graph"]
