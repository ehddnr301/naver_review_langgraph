from dotenv import load_dotenv

from typing import Sequence
from langchain_core.messages import HumanMessage, BaseMessage

load_dotenv()

from llm_utils.chains import extract_chain, search_chain, recommend_chain

EXTRACT = "extract"
SEARCH = "search"
RECOMMEND = "recommend"


def extract_node(state: Sequence[BaseMessage]):
    res = extract_chain.invoke(input={"search_query": state})
    search_query = list(res[0].dict().values())
    return search_query


def search_node(state: Sequence[BaseMessage]):
    res = search_chain.invoke(input={"search_term": state})
    print(res)
    return res


def recommend_node(state: Sequence[BaseMessage]):
    return recommend_chain.invoke(input={"restaurants_list": state})


from langgraph.graph import END, MessageGraph

builder = MessageGraph()
builder.add_node(EXTRACT, extract_node)
builder.add_node(SEARCH, search_node)
builder.add_node(RECOMMEND, recommend_node)
builder.set_entry_point(EXTRACT)

builder.add_edge(EXTRACT, SEARCH)
builder.add_edge(SEARCH, RECOMMEND)
builder.add_edge(RECOMMEND, END)

graph = builder.compile()

if __name__ == "__main__":
    human_message = HumanMessage(
        content="강남역 근처에서 회식할껀데 8-10명 정도 모임이 가능한 모두들 느끼한 음식을 좋아해요"
    )

    res = graph.invoke(input=[human_message])
    print(res[0])
    for r in res:
        print(r)
