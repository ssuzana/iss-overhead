import requests
from datetime import datetime
import smtplib
import time

MY_EMAIL = "smtppython1@gmail.com"
PASSWORD = "pyth0n2021"

MY_LAT = 36.974117
MY_LONG = -122.030792

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.

def iss_is_close(lat, long):
    return abs(lat - iss_latitude) <=5 and abs(long - iss_longitude)

def is_nightime():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    return sunset <= time_now.hour <= sunrise

def send_email(to_email, subject, message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=to_email, msg=f"{subject}\n\n{message}")

subject = "Look up!!"
message = "The ISS is close to your location."

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

while True:
    time.sleep(60)
    if iss_is_close(MY_LAT, MY_LONG) and is_nightime():
        send_email(MY_EMAIL, subject, message)


