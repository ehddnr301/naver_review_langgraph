import requests
from typing import Annotated
from langchain_core.tools import tool

from .schemas import PlaceAndFood

headers = {
    "referer": f"https://pcmap.place.naver.com/restaurant/list",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
}


def fetch_data(query: str, start: int):
    try:
        data = dict(
            operationName="getRestaurants",
            query="query getRestaurants($restaurantListInput: RestaurantListInput, $restaurantListFilterInput: RestaurantListFilterInput, $reverseGeocodingInput: ReverseGeocodingInput, $useReverseGeocode: Boolean = false, $isNmap: Boolean = false) {  restaurants: restaurantList(input: $restaurantListInput) {    items {      apolloCacheId      coupon {        ...CouponItems        __typename      }      ...CommonBusinessItems      ...RestaurantBusinessItems      __typename    }    ...RestaurantCommonFields    optionsForMap {      ...OptionsForMap      __typename    }    nlu {      ...NluFields      __typename    }    searchGuide {      ...SearchGuide      __typename    }    __typename  }  filters: restaurantListFilter(input: $restaurantListFilterInput) {    ...RestaurantFilter    __typename  }  reverseGeocodingAddr(input: $reverseGeocodingInput) @include(if: $useReverseGeocode) {    ...ReverseGeocodingAddr    __typename  }}fragment OptionsForMap on OptionsForMap {  maxZoom  minZoom  includeMyLocation  maxIncludePoiCount  center  spotId  keepMapBounds  __typename}fragment NluFields on Nlu {  queryType  user {    gender    __typename  }  queryResult {    ptn0    ptn1    region    spot    tradeName    service    selectedRegion {      name      index      x      y      __typename    }    selectedRegionIndex    otherRegions {      name      index      __typename    }    property    keyword    queryType    nluQuery    businessType    cid    branch    forYou    franchise    titleKeyword    location {      x      y      default      longitude      latitude      dong      si      __typename    }    noRegionQuery    priority    showLocationBarFlag    themeId    filterBooking    repRegion    repSpot    dbQuery {      isDefault      name      type      getType      useFilter      hasComponents      __typename    }    type    category    menu    context    __typename  }  __typename}fragment SearchGuide on SearchGuide {  queryResults {    regions {      displayTitle      query      region {        rcode        __typename      }      __typename    }    isBusinessName    __typename  }  queryIndex  types  __typename}fragment ReverseGeocodingAddr on ReverseGeocodingResult {  rcode  region  __typename}fragment CouponItems on Coupon {  total  promotions {    promotionSeq    couponSeq    conditionType    image {      url      __typename    }    title    description    type    couponUseType    __typename  }  __typename}fragment CommonBusinessItems on BusinessSummary {  id  dbType  name  businessCategory  category  description  hasBooking  hasNPay  x  y  distance  imageUrl  imageCount  phone  virtualPhone  routeUrl  streetPanorama {    id    pan    tilt    lat    lon    __typename  }  roadAddress  address  commonAddress  blogCafeReviewCount  bookingReviewCount  totalReviewCount  bookingUrl  bookingBusinessId  talktalkUrl  detailCid {    c0    c1    c2    c3    __typename  }  options  promotionTitle  agencyId  businessHours  newOpening  markerId @include(if: $isNmap)  markerLabel @include(if: $isNmap) {    text    style    __typename  }  imageMarker @include(if: $isNmap) {    marker    markerSelected    __typename  }  __typename}fragment RestaurantFilter on RestaurantListFilterResult {  filters {    index    name    value    multiSelectable    defaultParams {      age      gender      day      time      __typename    }    items {      index      name      value      selected      representative      displayName      clickCode      laimCode      type      icon      __typename    }    __typename  }  votingKeywordList {    items {      name      value      icon      clickCode      __typename    }    menuItems {      name      value      icon      clickCode      __typename    }    total    __typename  }  optionKeywordList {    items {      name      value      icon      clickCode      __typename    }    total    __typename  }  __typename}fragment RestaurantCommonFields on RestaurantListResult {  restaurantCategory  queryString  siteSort  selectedFilter {    order    rank    tvProgram    region    brand    menu    food    mood    purpose    sortingOrder    takeout    orderBenefit    cafeFood    day    time    age    gender    myPreference    hasMyPreference    cafeMenu    cafeTheme    theme    voting    filterOpening    keywordFilter    property    realTimeBooking    __typename  }  rcodes  location {    sasX    sasY    __typename  }  total  __typename}fragment RestaurantBusinessItems on RestaurantListSummary {  categoryCodeList  visitorReviewCount  visitorReviewScore  imageUrls  bookingHubUrl  bookingHubButtonName  visitorImages {    id    reviewId    imageUrl    profileImageUrl    nickname    __typename  }  visitorReviews {    id    review    reviewId    __typename  }  foryouLabel  foryouTasteType  microReview  tags  priceCategory  broadcastInfo {    program    date    menu    __typename  }  michelinGuide {    year    star    comment    url    hasGrade    isBib    alternateText    hasExtraNew    region    __typename  }  broadcasts {    program    menu    episode    broadcast_date    __typename  }  tvcastId  naverBookingCategory  saveCount  uniqueBroadcasts  isDelivery  deliveryArea  isCvsDelivery  isTableOrder  isPreOrder  isTakeOut  bookingDisplayName  bookingVisitId  bookingPickupId  popularMenuImages {    name    price    bookingCount    menuUrl    menuListUrl    imageUrl    isPopular    usePanoramaImage    __typename  }  newBusinessHours {    status    description    __typename  }  baemin {    businessHours {      deliveryTime {        start        end        __typename      }      closeDate {        start        end        __typename      }      temporaryCloseDate {        start        end        __typename      }      __typename    }    __typename  }  yogiyo {    businessHours {      actualDeliveryTime {        start        end        __typename      }      bizHours {        start        end        __typename      }      __typename    }    __typename  }  realTimeBookingInfo {    description    hasMultipleBookingItems    bookingBusinessId    bookingUrl    itemId    itemName    timeSlots {      date      time      timeRaw      available      __typename    }    __typename  }  __typename}",
            variables=dict(
                isNmap=False,
                restaurantListInput={
                    "deviceType": "pcmap",
                    "display": 50,
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

        return resp.json()
    except Exception as e:
        print(e)
        return []


@tool
def crawl_restaurants(search_term: Annotated[str, "search term"]):
    """
    Crawls restaurants based on the search term
    """
    start = 1
    res = fetch_data(search_term, start)

    return res
