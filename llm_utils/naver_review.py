import time
import random
import requests
from datetime import datetime

import numpy as np
import pandas as pd

from google.cloud import bigquery


def fetch_restaurants(query: str, start: int) -> pd.DataFrame:
    headers = {
        "referer": f"https://pcmap.place.naver.com/restaurant/list",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    }

    try:
        data = dict(
            operationName="getRestaurants",
            query="query getRestaurants($restaurantListInput: RestaurantListInput, $restaurantListFilterInput: RestaurantListFilterInput, $reverseGeocodingInput: ReverseGeocodingInput, $useReverseGeocode: Boolean = false, $isNmap: Boolean = false) {  restaurants: restaurantList(input: $restaurantListInput) {    items {      apolloCacheId      coupon {        ...CouponItems        __typename      }      ...CommonBusinessItems      ...RestaurantBusinessItems      __typename    }    ...RestaurantCommonFields    optionsForMap {      ...OptionsForMap      __typename    }    nlu {      ...NluFields      __typename    }    searchGuide {      ...SearchGuide      __typename    }    __typename  }  filters: restaurantListFilter(input: $restaurantListFilterInput) {    ...RestaurantFilter    __typename  }  reverseGeocodingAddr(input: $reverseGeocodingInput) @include(if: $useReverseGeocode) {    ...ReverseGeocodingAddr    __typename  }}fragment OptionsForMap on OptionsForMap {  maxZoom  minZoom  includeMyLocation  maxIncludePoiCount  center  spotId  keepMapBounds  __typename}fragment NluFields on Nlu {  queryType  user {    gender    __typename  }  queryResult {    ptn0    ptn1    region    spot    tradeName    service    selectedRegion {      name      index      x      y      __typename    }    selectedRegionIndex    otherRegions {      name      index      __typename    }    property    keyword    queryType    nluQuery    businessType    cid    branch    forYou    franchise    titleKeyword    location {      x      y      default      longitude      latitude      dong      si      __typename    }    noRegionQuery    priority    showLocationBarFlag    themeId    filterBooking    repRegion    repSpot    dbQuery {      isDefault      name      type      getType      useFilter      hasComponents      __typename    }    type    category    menu    context    __typename  }  __typename}fragment SearchGuide on SearchGuide {  queryResults {    regions {      displayTitle      query      region {        rcode        __typename      }      __typename    }    isBusinessName    __typename  }  queryIndex  types  __typename}fragment ReverseGeocodingAddr on ReverseGeocodingResult {  rcode  region  __typename}fragment CouponItems on Coupon {  total  promotions {    promotionSeq    couponSeq    conditionType    image {      url      __typename    }    title    description    type    couponUseType    __typename  }  __typename}fragment CommonBusinessItems on BusinessSummary {  id  dbType  name  businessCategory  category  description  hasBooking  hasNPay  x  y  distance  imageUrl  imageCount  phone  virtualPhone  routeUrl  streetPanorama {    id    pan    tilt    lat    lon    __typename  }  roadAddress  address  commonAddress  blogCafeReviewCount  bookingReviewCount  totalReviewCount  bookingUrl  bookingBusinessId  talktalkUrl  detailCid {    c0    c1    c2    c3    __typename  }  options  promotionTitle  agencyId  businessHours  newOpening  markerId @include(if: $isNmap)  markerLabel @include(if: $isNmap) {    text    style    __typename  }  imageMarker @include(if: $isNmap) {    marker    markerSelected    __typename  }  __typename}fragment RestaurantFilter on RestaurantListFilterResult {  filters {    index    name    value    multiSelectable    defaultParams {      age      gender      day      time      __typename    }    items {      index      name      value      selected      representative      displayName      clickCode      laimCode      type      icon      __typename    }    __typename  }  votingKeywordList {    items {      name      value      icon      clickCode      __typename    }    menuItems {      name      value      icon      clickCode      __typename    }    total    __typename  }  optionKeywordList {    items {      name      value      icon      clickCode      __typename    }    total    __typename  }  __typename}fragment RestaurantCommonFields on RestaurantListResult {  restaurantCategory  queryString  siteSort  selectedFilter {    order    rank    tvProgram    region    brand    menu    food    mood    purpose    sortingOrder    takeout    orderBenefit    cafeFood    day    time    age    gender    myPreference    hasMyPreference    cafeMenu    cafeTheme    theme    voting    filterOpening    keywordFilter    property    realTimeBooking    __typename  }  rcodes  location {    sasX    sasY    __typename  }  total  __typename}fragment RestaurantBusinessItems on RestaurantListSummary {  categoryCodeList  visitorReviewCount  visitorReviewScore  imageUrls  bookingHubUrl  bookingHubButtonName  visitorImages {    id    reviewId    imageUrl    profileImageUrl    nickname    __typename  }  visitorReviews {    id    review    reviewId    __typename  }  foryouLabel  foryouTasteType  microReview  tags  priceCategory  broadcastInfo {    program    date    menu    __typename  }  michelinGuide {    year    star    comment    url    hasGrade    isBib    alternateText    hasExtraNew    region    __typename  }  broadcasts {    program    menu    episode    broadcast_date    __typename  }  tvcastId  naverBookingCategory  saveCount  uniqueBroadcasts  isDelivery  deliveryArea  isCvsDelivery  isTableOrder  isPreOrder  isTakeOut  bookingDisplayName  bookingVisitId  bookingPickupId  popularMenuImages {    name    price    bookingCount    menuUrl    menuListUrl    imageUrl    isPopular    usePanoramaImage    __typename  }  newBusinessHours {    status    description    __typename  }  baemin {    businessHours {      deliveryTime {        start        end        __typename      }      closeDate {        start        end        __typename      }      temporaryCloseDate {        start        end        __typename      }      __typename    }    __typename  }  yogiyo {    businessHours {      actualDeliveryTime {        start        end        __typename      }      bizHours {        start        end        __typename      }      __typename    }    __typename  }  realTimeBookingInfo {    description    hasMultipleBookingItems    bookingBusinessId    bookingUrl    itemId    itemName    timeSlots {      date      time      timeRaw      available      __typename    }    __typename  }  __typename}",
            variables=dict(
                isNmap=False,
                restaurantListInput={
                    "deviceType": "pcmap",
                    "display": 5,
                    "filterOpening": None,
                    "isCurrentLocationSearch": None,
                    "isPcmap": True,
                    "orderBenefit": None,
                    "query": query,
                    "rank": "저장많은",
                    "start": start,
                    "takeout": None,
                    "x": "127.019508",
                    "y": "37.490119",
                },
            ),
        )
        resp = requests.post(
            "https://pcmap-api.place.naver.com/place/graphql",
            headers=headers,
            json=data,
        )

        resp_data = resp.json()

        restaurant_items = resp_data["data"]["restaurants"]["items"]

        restaurant_data = pd.DataFrame(
            data=[],
            columns=[
                "restaurant_id",
                "restaurant_name",
                "category",
                "commonAddress",
                "options",
                "businessHours",
                "naverBookingCategory",
            ],
        )

        for item in restaurant_items:
            tmp = []
            tmp.append(item["id"])
            tmp.append(item["name"])
            tmp.append(item["category"])
            tmp.append(item["commonAddress"])
            tmp.append(item["options"])
            tmp.append(item["businessHours"])
            tmp.append(item["naverBookingCategory"])

            tmp = pd.DataFrame(data=[tmp], columns=restaurant_data.columns)
            restaurant_data = pd.concat([restaurant_data, tmp])

        restaurant_data["naverBookingCategory"] = restaurant_data[
            "naverBookingCategory"
        ].fillna("예약불가")
        return restaurant_data

    except Exception as e:
        return []


def fetch_reviews(restaurant_id: int) -> pd.DataFrame:
    now = datetime.now()
    formatted_time = now.strftime("%Y%m%d%H%M")

    headers = {
        "referer": f"https://pcmap.place.naver.com/place/{restaurant_id}?from=map&timestamp={formatted_time}",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    }

    data = dict(
        operationName="getVisitorReviews",
        query="query getVisitorReviews($input: VisitorReviewsInput) { visitorReviews(input: $input) { items { id rating author { id nickname from imageUrl borderImageUrl objectId url review { totalCount imageCount avgRating __typename } theme { totalCount __typename } isFollowing followerCount followRequested __typename } body thumbnail media { type thumbnail thumbnailRatio class videoId videoOriginSource trailerUrl __typename } tags status visitCount viewCount visited created reply { editUrl body editedBy created date replyTitle isReported isSuspended __typename } originType item { name code options __typename } language highlightOffsets apolloCacheId translatedText businessName showBookingItemName bookingItemName votedKeywords { code iconUrl iconCode displayName __typename } userIdno loginIdno receiptInfoUrl reactionStat { id typeCount { name count __typename } totalCount __typename } hasViewerReacted { id reacted __typename } nickname showPaymentInfo visitKeywords { category keywords __typename } __typename } starDistribution { score count __typename } hideProductSelectBox total showRecommendationSort itemReviewStats { score count itemId starDistribution { score count __typename } __typename } __typename } }",
        variables=dict(
            id=f"{restaurant_id}",
            input={
                "businessId": f"{restaurant_id}",
                "businessType": "restaurant",
                "item": "0",
                "bookingBusinessId": "null",
                "page": 1,
                "size": 1,
                "isPhotoUsed": False,
                "includeContent": True,
                "getUserStats": True,
                "includeReceiptPhotos": True,
                "cidList": ["220036", "220037", "220053"],
                "getReactions": True,
                "getTrailer": True,
            },
        ),
    )

    review_data = pd.DataFrame(
        data=[],
        columns=[
            "review_id",
            "content",
        ],
    )

    resp = requests.post(
        "https://pcmap-api.place.naver.com/place/graphql", headers=headers, json=data
    )
    data = resp.json()

    items = data["data"]["visitorReviews"]["items"]

    for item in items:
        tmp = []
        """sample
        tmp.append(str(item['rating']) + " " + str(item['created']))
        """
        tmp.append(item["id"])  # review_id
        tmp.append(item["body"])  # content

        tmp = pd.DataFrame(data=[tmp], columns=review_data.columns)
        review_data = pd.concat([review_data, tmp])

    return review_data


def query_search_term(search_term: str):
    client = bigquery.Client()
    place, keyword = search_term.split(" ")
    place = place.replace("역", "")
    query = f"""
        WITH searched_restaurants_id AS (
        SELECT DISTINCT place_id
        FROM `pseudocon-24-summer.place_id.search_query`
        WHERE search_query LIKE '%{search_term}%'
        ), recent_review AS (
            SELECT place_id AS restaurant_id
            , body
            , review_category.element.displayName
            , DENSE_RANK() OVER (PARTITION BY place_id ORDER BY viewCount DESC) AS row_num
            FROM `pseudocon-24-summer.review.naver`
            , unnest(votedKeywords.list) AS review_category
            WHERE body <> '' AND place_id IN (
                SELECT place_id
                FROM searched_restaurants_id
        )
        ), TOP10_recent_review AS (
        SELECT restaurant_id
        , body
        , STRING_AGG(distinct displayName, ', ') AS displayName
        FROM recent_review
        WHERE row_num <= 10
        GROUP BY restaurant_id, body
        ), restaurants_list AS (
        SELECT id
        , name
        , commonAddress
        , businessHours
        , options
        , naverBookingCategory
        FROM `pseudocon-24-summer.gangnam.pasta`
        WHERE id IN (
            SELECT place_id
            FROM searched_restaurants_id
        )
        )

        SELECT
            A.name AS restaurant_name,
            A.commonAddress,
            A.businessHours AS business_hours,
            A.options,
            STRING_AGG(B.body, '\\n') AS review_content,
            String_AGG(distinct B.displayName, ', ') AS review_category,
            CASE 
                WHEN A.naverBookingCategory IS NULL 
                    THEN '네이버 예약 불가' 
                ELSE '네이버 예약 가능'
            END AS naverBookingCategory
        FROM restaurants_list AS A
        INNER JOIN TOP10_recent_review AS B
        ON A.id = B.restaurant_id
        GROUP BY
            A.name,
            A.commonAddress,
            A.businessHours,
            A.options,
            A.naverBookingCategory
        LIMIT 10
    """

    query_job = client.query_and_wait(query)

    df = query_job.to_dataframe()
    return df
