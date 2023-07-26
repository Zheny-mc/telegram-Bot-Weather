def token(file_name:str):
    with open(file_name) as f:
        return f.readline().rstrip()

bot_token = lambda: token('tokens/token.txt')
weather_token = lambda: token('tokens/WEATHER_API_KEY.txt')