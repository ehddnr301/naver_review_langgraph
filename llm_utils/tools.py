import requests
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
    {restaurant_name} 음식점의 영업시간 정보:{businessHours}
    {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
    {restaurant_name} 음식점의 예약가능 여부:{reservation_available} [예약/예약불가]

    And Each restaurant's information is separated by double newline character
    """
    try:
        restaurants = fetch_restaurants(search_term, 0)

        results = ""

        for _, row in restaurants.iterrows():
            restaurant_id = row["restaurant_id"]
            restaurant_name = row["restaurant_name"]
            businessHours = row["businessHours"]
            restaurant_options = row["options"]
            reservation_available = row["naverBookingCategory"]

            reviews = fetch_reviews(restaurant_id)

            review_contents = reviews["content"].tolist()

            result_line = f"""
                {restaurant_name} 음식점의 리뷰:{','.join(review_contents)}
                {restaurant_name} 음식점의 영업시간 정보:{businessHours}
                {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
                {restaurant_name} 음식점의 예약가능 여부:{reservation_available}
            """

            results += result_line + "\n\n"

        return results

    except:
        return ""


@tool
def query_restaurants(search_term: Annotated[str, "search term"]):
    """
    Query restaurants based on the search term Each restaurant's information is returned in the following format:
    {restaurant_name} 음식점의 리뷰:{reviews}
    {restaurant_name} 음식점의 영업시간 정보:{businessHours}
    {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
    {restaurant_name} 음식점의 예약가능 여부:{reservation_available} [예약/예약불가]

    And Each restaurant's information is separated by double newline character
    """
    try:
        df = query_search_term(search_term)
        results = ""

        for _, row in df.iterrows():

            restaurant_name = row["restaurant_name"]
            businessHours = row["business_hours"]
            restaurant_options = row["options"]
            reservation_available = row["naver_booking_category"]
            reviews = row["content"]

            result_line = f"""
                {restaurant_name} 음식점의 리뷰:{reviews}
                {restaurant_name} 음식점의 영업시간 정보:{businessHours}
                {restaurant_name} 음식점의 편의시설 및 서비스:{restaurant_options}
                {restaurant_name} 음식점의 예약가능 여부:{reservation_available}
            """

            results += result_line + "\n\n"

        return results

    except Exception as e:
        return ""
