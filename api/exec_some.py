from dotenv import dotenv_values

config = dotenv_values('.env')
print(config)
print(config.get('POSTGRES_USER', 'postgres'))