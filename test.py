from dotenv import load_dotenv

from typing import Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode

load_dotenv()

from llm_utils.chains import extract_chain, search_chain, recommend_chain
from llm_utils.tools import crawl_restaurants, query_restaurants

EXTRACT = "extract"
SEARCH = "search"
GET_RESTAURANTS = "get_restaurants"
RECOMMEND = "recommend"

tool_node = ToolNode([crawl_restaurants, query_restaurants])


def extract_node(state: Sequence[BaseMessage]):
    res = extract_chain.invoke(input={"search_query": [state[-1].content]})
    search_query = " ".join(list(res[0].dict().values()))
    return search_query


def search_node(state: Sequence[BaseMessage]):
    if len(state) > 10:
        raise ValueError("Too many iterations")
    search_term = state[-1].content if len(state) < 3 else state[1].content
    tool_choice = "query_restaurants" if len(state) < 3 else "crawl_restaurants"
    res = search_chain.invoke(
        input={"search_term": [search_term], "tool_choice": [tool_choice]}
    )
    return res


def recommend_node(state: Sequence[BaseMessage]):
    return recommend_chain.invoke(
        input={
            "user_input": [state[0].content],
            "restaurants_list": [state[-1].content],
        }
    )


def decide_node(state: Sequence[BaseMessage]):
    content = state[-1].content
    if content == "":
        return SEARCH
    else:
        return RECOMMEND


from langgraph.graph import END, MessageGraph

builder = MessageGraph()
builder.add_node(EXTRACT, extract_node)
builder.add_node(SEARCH, search_node)
builder.add_node(RECOMMEND, recommend_node)
builder.add_node(GET_RESTAURANTS, tool_node)

builder.set_entry_point(EXTRACT)

builder.add_edge(EXTRACT, SEARCH)
builder.add_edge(SEARCH, GET_RESTAURANTS)
builder.add_conditional_edges(
    GET_RESTAURANTS,
    decide_node,
    {
        RECOMMEND: RECOMMEND,
        SEARCH: SEARCH,
    },
)
builder.add_edge(RECOMMEND, END)

graph = builder.compile()

if __name__ == "__main__":
    human_message = HumanMessage(
        content="강남역 파스타 추천해줘 예약가능한 가게여야만 해"
    )

    res = graph.invoke(input=human_message)
    # print(graph.get_graph().draw_mermaid())
