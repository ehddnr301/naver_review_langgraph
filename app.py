import time
import redis
import streamlit as st

r = redis.Redis(host="redis", port=6379, password="pseudolab", decode_responses=True)

st.title("레스토랑 검색 및 목록")
search_query = st.text_input("검색할 지역 또는 레스토랑을 입력하세요:", "강남역 맛집")

if st.button("검색"):

    from crawl_list import fetch_data

    initial_data = fetch_data(search_query, 1)
    print(initial_data)
    if initial_data:
        items = initial_data["data"]["restaurants"]["items"]
        id_n_name_list = [item["name"] for item in items]

        for item in id_n_name_list:
            r.lpush("restaurant_list", item)

col1, col2 = st.columns(2)

restaurant_list = r.lrange("restaurant_list", 0, -1)
with col1:
    col1.empty()
    if restaurant_list:
        st.write("현재 레스토랑 목록:")
        for restaurant in restaurant_list:
            st.text(restaurant)
    else:
        st.write("레스토랑 목록이 비어있습니다.")

poped_list = r.lrange("poped_list", 0, -1)
with col2:
    col2.empty()
    if poped_list:
        st.write("현재 처리된 레스토랑 목록:")
        for poped in poped_list:
            st.text(poped)
    else:
        st.write("처리목록이 비어있습니다.")

time.sleep(5)
st.rerun()
