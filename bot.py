import telebot
import requests
from dotenv import dotenv_values
import json


env_vars = dotenv_values()
weather_api_key = env_vars['WEATHER_API_KEY']
bot_token = env_vars['BOT_TOKEN']

lat = 9.0192
lon = 38.7525


# maps weather icon to telegram emoji
emoji_code = {
    "01d": "\U00002600", "01n": "\U0001F319",
    "02d": "\U0001F324", "02n": "\U00002601",
    "03d": "\U00002601", "03n": "\U00002601",
    "04d": "\U0001F325", "04n": "\U0001F325",
    "09d": "\U0001F327", "09n": "\U0001F327",
    "10d": "\U0001F326", "10n": "\U0001F327",
    "11d": "\U000026C8", "11n": "\U000026C8",
    "13d": "\U00002744", "13n": "\U00002744",
    "50d": "\U0001F32B", "50n": "\U0001F32B",
}




def fetch_weather_data(latitude, longitude):
    
    try:
        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api_key}")
        data = json.loads(response.text)

        weather_condition = data['weather'][0]['main']
        description = data['weather'][0]['description']
        feels_like = str(int(data['main']['feels_like']) - 273.15)[:5]
        icon = emoji_code[data['weather'][0]['icon']]
        
        
        reply = f"""
        {icon}{icon}{icon}\n
<b>{weather_condition}</b>\n
Description: <i>{description}</i>
Temperature: <i>{feels_like}°C</i>
        """
        return True, reply

    except:
        return False, '\U0001F641'

        
memo = defaultdict(lambda :None)
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):

    chat_id = message.chat.id
    # first_name = message.from_user.first_name
    
    ok_status, response = fetch_weather_data(lat, lon)
    if ok_status:
        bot.send_message(chat_id, response, parse_mode="HTML")
    
    else:
        bot.send_message(chat_id, response, parse_mode="HTML")
        bot.send_message(chat_id, "Oops, something went wrong.", parse_mode="HTML")




def validate(coordinates):
    coordinates = coordinates.replace(" ", "")
    lat, lon = map(float, coordinates.split(":"))
    assert (-180 <= lon <= 180) 
    assert (-90 <= lat <= 90) 
    return (lat, lon)

@bot.message_handler(func=lambda msg: True)
def chat(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    

bot.infinity_polling()

