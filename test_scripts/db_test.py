import sys

sys.path.append('../src/api')
import database

iCanItems = database.ICanItems()
iCanItems.addRecord({'timestamp': 12345})
