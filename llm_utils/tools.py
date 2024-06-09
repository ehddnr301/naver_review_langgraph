import requests
import random
from collections import Counter
from typing import Annotated
from langchain_core.tools import tool

from .naver_review import fetch_restaurants, fetch_reviews, query_search_term


@tool
def crawl_restaurants(
    search_term: Annotated[str, "search term"],
):
    """
    Crawls restaurants And Review based on the search term Each restaurant's information is returned in the following format:
    {restaurant_name} 음식점의 리뷰:{review_contents}
    {restaurant_name} 음식점의 위치:{common_address}
    {restaurant_name} 음식점의 영업시간 정보:{businessHours}
    {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
    {restaurant_name} 음식점의 네이버 예약가능 여부:{reservation_available} [예약/예약불가]

    And Each restaurant's information is separated by double newline character
    """
    try:
        restaurants = fetch_restaurants(search_term, random.randint(0, 3))
        results = ""

        for _, row in restaurants.iterrows():
            restaurant_id = row["restaurant_id"]
            restaurant_name = row["restaurant_name"]
            common_address = row["commonAddress"]
            businessHours = row["businessHours"]
            restaurant_options = row["options"]
            reservation_available = row["naverBookingCategory"]

            reviews = fetch_reviews(restaurant_id)

            review_contents = reviews["content"].tolist()

            result_line = f"""
                {restaurant_name} 음식점의 리뷰:{','.join(review_contents)}
                {restaurant_name} 음식점의 위치 정보:{common_address}
                {restaurant_name} 음식점의 영업시간 정보:{businessHours}
                {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
                {restaurant_name} 음식점의 네이버 예약가능 여부:{reservation_available}
            """

            results += result_line + "\n\n"
        return results

    except Exception as e:
        print(e)
        return ""


@tool
def query_restaurants(search_term: Annotated[str, "search term"]):
    """
    Query restaurants based on the search term Each restaurant's information is returned in the following format:
    {restaurant_name} 음식점의 리뷰:{reviews}
    {restaurant_name} 음식점의 위치:{common_address}
    {restaurant_name} 음식점의 리뷰 카테고리 정보:{businessHours}
    {restaurant_name} 음식점의 영업시간 정보:{businessHours}
    {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
    {restaurant_name} 음식점의 네이버 예약가능 여부:{reservation_available} [예약/예약불가]

    And Each restaurant's information is separated by double newline character
    """
    try:
        df = query_search_term(search_term)
        results = ""

        for _, row in df.iterrows():

            restaurant_name = row["restaurant_name"]
            commonAddress = row["commonAddress"]
            businessHours = row["business_hours"]
            restaurant_options = row["options"]
            reservation_available = row["naverBookingCategory"]
            reviews = row["review_content"]
            review_category = row["review_category"]

            most_reviewed_category = (
                Counter(review_category.split(", ")).most_common(1)[0][0]
                if "," in review_category
                else "없음"
            )

            result_line = f"""
                {restaurant_name} 음식점의 리뷰: ```{reviews}```
                {restaurant_name} 음식점의 주요 리뷰 카테고리:{most_reviewed_category}
                {restaurant_name} 음식점의 위치 정보:{commonAddress}
                {restaurant_name} 음식점의 영업시간 정보:{businessHours}
                {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
                {restaurant_name} 음식점의 네이버 예약가능 여부:{reservation_available}
            """

            results += result_line + "\n\n"

        return results

    except Exception as e:
        print(e)
        return ""
