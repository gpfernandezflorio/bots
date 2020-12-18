import os
from dotenv import load_dotenv

load_dotenv()
modo_testing = os.getenv('TEST_MODE')=="YES"
servidor = "TEST" if modo_testing else "DC"
id_admin = int(os.getenv('DISCORD_ADMIN'))
print("ID ADMIN: " + str(id_admin))
id_me = int(os.getenv('DISCORD_ME'))
print("ID ME: " + str(id_me))
id_servidor = int(os.getenv('DISCORD_GUILD_'+servidor))
print("ID SERVIDOR: " + str(id_servidor))
id_rol = int(os.getenv('DISCORD_'+servidor+'_MY_ROLE'))
print("ID ROL: " + str(id_rol))
id_canal_noriega = int(os.getenv('DISCORD_'+servidor+'_CH_NORIEGA'))
print("ID CANAL NORIEGA: " + str(id_canal_noriega))
id_canal_general = int(os.getenv('DISCORD_'+servidor+'_CH_GENERAL'))
print("ID CANAL GENERAL: " + str(id_canal_general))
id_canal_recordatorios = int(os.getenv('DISCORD_'+servidor+'_CH_RECORDATORIOS'))
print("ID CANAL RECORDATORIOS: " + str(id_canal_recordatorios))
