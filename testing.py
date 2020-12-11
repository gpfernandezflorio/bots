import os
from dotenv import load_dotenv

load_dotenv()
modo_testing = os.getenv('TEST_MODE')=="YES"
servidor = "TEST" if modo_testing else "DC"
id_servidor = int(os.getenv('DISCORD_GUILD_'+servidor))
id_canal_noriega = int(os.getenv('DISCORD_CH_'+servidor+'_NORIEGA'))
id_canal_general = int(os.getenv('DISCORD_CH_'+servidor+'_GENERAL'))
