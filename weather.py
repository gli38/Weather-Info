import schedule
import time

def get_weather(latitude, longitude):
    base_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,uv_index"
    response = requests.get(base_url)
    data = response.json()
    return data 
    
def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def send_text_message(body):
    account_sid = "twilio_sid"
    auth_token = "twilio_token"
    from_phone_number = "from_phone_number"
    to_phone_number = "to_phone_number"
    
    client = Client(account_sid, auth_token)
    
    message = client.message.create(
        body=body,
        from_=from_phone_number,
        to = to_phone_number
    )
    print("Text mesaage sent!")
        
def send_weather_update():
    # Hardcoded latitude and longitutde for Hayward
    latitude = 37.668819
    longitude = -122.080795
    
    weather_data = get_weather(latitude, longitude)
    temperature_celsius = weather_data["hourly"]["temperature_2m"]
    temperature_fahrenheit = celsius_to_fahrenheit(temperature_celsius)
    uv_index = weather_data["hourly"]["uv_index"]
    
    weather_info = (
        f"Good morning!\n"
        f"Current Weather in Hayward, CA:\n"
        f"Temperature: {temperature_fahrenheit:.2f}°F\n"
        f"UV Index: {uv_index}"
    )
    
    send_text_message(weather_info)

def main():
    schedule.every().day.at("08:00").do(send_weather_update)
    while True:
        schedule.run_pending()
        time.sleep(1)
        
if __name__ == "__main__":
    main()