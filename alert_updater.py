from models.alert import Alert
from dotenv import load_dotenv

load_dotenv()

alerts = Alert.all()

for alert in alerts:
    alert.load_item_price()
    alert.notify_if_price_reached()

if not alerts:
    print("There has no alert been created yet")
