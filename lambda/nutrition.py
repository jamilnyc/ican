import json

from botocore.vendored import requests


class NutritionService:
    def getHeaders(self):
        """
        Return the headers necessary to access the Nutritionix REST API.

        :return dictionary with key/value pairs as header names and header values
        """
        return {
            'Content-Type': 'application/json',
            'x-app-id': 'YOUR_APP_ID_HERE',
            'x-app-key': 'YOUR_APP_KEY_HERE',
        }

    def getUrl(self):
        """
        Return the URL of the Nutritionix REST API.

        :return string URL of the REST API
        """
        return 'https://trackapi.nutritionix.com/v2/natural/nutrients'

    def getPayload(self, foods):
        """
        Return the formatted POST payload for the natural language endpoint.

        :return JSON object that contains the payload for the API Request
        """
        query = []
        for food in foods:
            query.append(str(1) + ' ' + str(food))
        queryString = ', '.join(query)
        payload = {
            "query": queryString,
            "timezone": "US/Eastern"
        }
        return json.dumps(payload)

    def getNutritionByIdentifiers(self, identifiers):
        """
        Returns a list of food items with their basic nutritional information.

        Each element in the identifiers list is queried against the Nutritionix API
        and if any are recognized as food by the API, the most caloric item is returned
        with additional nutrition information.

        :param identifiers:
        :return:
        """
        # Data necessary to make an API call
        payload = self.getPayload(identifiers)
        headers = self.getHeaders()
        url = self.getUrl()

        # Make the HTTP request
        r = requests.post(url=url, data=payload, headers=headers)
        response = r.json()

        # Check if any element in the identifiers list is considered a food item
        if 'foods' not in response.keys():
            return None

        # Find the most caloric food item that was recognized
        targetFood = None
        for food in response['foods']:
            if targetFood is None:
                targetFood = food
            else:
                if food['nf_calories'] > targetFood['nf_calories']:
                    targetFood = food
                    
        # Variable targetFood now contains the most caloric food in the list
        # Translate field names from Nutritionix to more readable ones
        return {
            'name': targetFood['food_name'],
            'calories': targetFood['nf_calories'],
            'total_fat': targetFood['nf_total_fat'],
            'saturated_fat': targetFood['nf_saturated_fat'],
            'sugar': targetFood['nf_sugars']
        }
        
    def getMockNutritionData(self):
        """
        Return mock processed data that would normally be returned from getNutritionByIdentifiers().
        This method is useful for testing purposes as it bypasses the API calls and prevents hitting
        the rate limit on the Nutritionix API (100 calls a day for a free account).

        :return: JSON object
        """
        data = '''
        [
          {
            "saturated_fat": 0,
            "total_fat": 0,
            "calories": 0,
            "name": "water",
            "sugar": 0
          },
          {
            "saturated_fat": 0,
            "total_fat": 0,
            "calories": 0,
            "name": "water",
            "sugar": 0
          },
          {
            "saturated_fat": 2.59,
            "total_fat": 9.78,
            "calories": 211.8,
            "name": "biscuit",
            "sugar": 1.31
          },
          {
            "saturated_fat": 21.04,
            "total_fat": 39.18,
            "calories": 790.26,
            "name": "blizzard",
            "sugar": 77.5
          },
          {
            "saturated_fat": 0,
            "total_fat": 0,
            "calories": 0,
            "name": "water",
            "sugar": 0
          },
          {
            "saturated_fat": 0,
            "total_fat": 0.05,
            "calories": 2.37,
            "name": "coffee",
            "sugar": 0
          }
        ]
        '''
        return json.loads(data)