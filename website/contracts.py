class ErrorCodes:
    USER_NOT_LOGGED_IN = 1
    OBJECT_NOT_SAVED = 2
    SERVER_ERROR = 3


class SessionParameters:
    USERID = "userid"


class RecommendationContractRequest:
    # RECOMMENDATION PAYLOAD FIELDS
    OCCASION_KEY = "occasion"
    GENDER_KEY = "gender"
    AGE_GROUP_KEY = "ageGroup"
    CULTURE_KEY = "culture"
    CITY_KEY = "city"
    SEASONAL_TRENDS_KEY = "seasonalTrends"
    PERSONAL_STYLE_KEY = "personalStyle"
    BODY_TYPE_KEY = "bodyType"
    FIT_TYPE_KEY = "fitType"
    FABRICE_PREFERENCE_KEY = "fabricPreference"
    COLOR_PREFERENCE_KEY = "colorPreference"
    CLOTHING_TYPE_KEY = "clothingType"
    ACTIVITY_TYPE_KEY = "activityType"
    DATE_TIME_KEY = "dateTime"
    TIME_KEY = "time"
    LOWER_BUDGET_KEY = "lowerBudget"
    UPPER_BUDGET_KEY = "upperBudget"
    


class RecommendationContractResponse:
    LINKS = "links"


class PreferenceContractRequest:
    PREFERENCES = "preferences"


class FavouritesContrastRequest:
    FAVOURITE_URL_KEY = "favouriteUrl"
    SEARCH_OCCASION_KEY = "occasion"
    SEARCH_WEATHER_KEY = "city"
