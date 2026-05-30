import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 13.756331
MY_LONG = 100.501762
MY_EMAIL = "yogurtprovider67@gmail.com"
MY_PASSWORD = "quqa zann abbv zecl"
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")

    data = response.json()
    print(data)

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    iss_position = (iss_latitude, iss_longitude)
    print(iss_position)

    if MY_LAT-5 <= iss_latitude <= MY_LAT + 5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True
    else:
        return False

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    print(data)
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    print("sunrise:", sunrise)
    print("sunset:", sunset)

    time_now = datetime.now().hour
    print("now:", time_now)

    if time_now >= sunset or time_now <= sunrise:
        return True
    else:
        return False

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD),
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look up!!\n\nThe iss is above you in the sky! "
            )
            print("Mail sent!")
