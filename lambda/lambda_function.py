from __future__ import print_function

import time

# Custom modules
import database
from notification import Notification
from nutrition import NutritionService
from report import NutrtritionReport


def lambda_handler(event, context):
    # This is the function that is called by Lambda (like a Main function)

    # Fetch all records from the last week
    dynamoService = database.DynamoService()
    now = int(time.time())
    oneWeekAgo = now - (7 * 24 * 60 * 60)
    print ("Getting items")
    identifierList = dynamoService.getItemIdentifiersAfterTimestamp(oneWeekAgo)

    # Get nutrition data on all food
    nutritionService = NutritionService()   
    nutrition = nutritionService.getMockNutritionData()
    print ("Querying for nutrition")
    for identifiers in identifierList:
        n = nutritionService.getNutritionByIdentifiers(identifiers)
        if n is not None:
            nutrition.append(n)

    # Generate HTML report
    nutritionReport = NutrtritionReport()
    url = nutritionReport.getHTML(nutrition)

    # Send user notification
    notificationService = Notification()
    message = "Your weekly Nutrition Report is ready. Download here: " + str(url);
    notificationService.sendNotification(message)
    return message
