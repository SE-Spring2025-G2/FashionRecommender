import json

from . import models
from . import utils

default_preferences = {
    "male": ["blue shirt", "black pant"],
    "female": ["blue shirt", "black pant"],
}


class PreferencesHelper:
    def givePreferences(self, userid, occasion):
        try:
            preferenceObj = models.Preference.query.filter_by(userid=userid).first()
            preferences = json.loads(str(preferenceObj.preferences))
            if occasion in preferences:
                return preferences[occasion]
        except:
            return None


class RecommendationHelper:
    def __init__(self) -> None:
        self.searchAPIObj = utils.SearchImages()
    
    def giveRecommendationsBasedOnGemini(self, query):
        return self.searchAPIObj.image_search(query)

