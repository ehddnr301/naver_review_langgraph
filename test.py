from dotenv import load_dotenv

from typing import Sequence
from langchain_core.messages import HumanMessage, BaseMessage
from langgraph.prebuilt import ToolNode

load_dotenv()

from llm_utils.chains import extract_chain, search_chain, recommend_chain
from llm_utils.tools import crawl_restaurants

EXTRACT = "extract"
SEARCH = "search"
CRAWL_RESTAURANTS = "crawl_restaurants"
RECOMMEND = "recommend"

tool_node = ToolNode([crawl_restaurants])


def extract_node(state: Sequence[BaseMessage]):
    res = extract_chain.invoke(input={"search_query": state})
    search_query = " ".join(list(res[0].dict().values()))
    return search_query


def search_node(state: Sequence[BaseMessage]):
    res = search_chain.invoke(input={"search_term": state})
    return res


def recommend_node(state: Sequence[BaseMessage]):
    print(state)
    return recommend_chain.invoke(input={"restaurants_list": state})


from langgraph.graph import END, MessageGraph

builder = MessageGraph()
builder.add_node(EXTRACT, extract_node)
builder.add_node(SEARCH, search_node)
builder.add_node(RECOMMEND, recommend_node)
builder.add_node(CRAWL_RESTAURANTS, tool_node)

builder.set_entry_point(EXTRACT)

builder.add_edge(EXTRACT, SEARCH)
builder.add_edge(SEARCH, CRAWL_RESTAURANTS)
builder.add_edge(CRAWL_RESTAURANTS, RECOMMEND)
builder.add_edge(RECOMMEND, END)

graph = builder.compile()

if __name__ == "__main__":
    human_message = HumanMessage(
        content="강남역 돈까스 추천해줘 예약가능한 가게여야만 해"
    )

    res = graph.invoke(input=human_message)
    for r in res:
        print(r)
        print("-" * 60)
    # print(graph.get_graph().draw_mermaid())
