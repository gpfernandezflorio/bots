Requerimientos:

(Saco icalevents por un bug en la comparación de fechas)

* pip install discord

* sudo apt install imagemagick

* pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

* pip install twx

* pip install opencv-python

Setup:

- Crear un archivo .env que incluya las siguientes claves:

DEBUG (YES|NO : hablar por la consola en lugar de conectarse a los bots)
TEST_MODE (YES|NO : usar los grupos y canales de prueba en lugar de los oficiales)
TG_TOKEN (el token del bot de Telgram)
TG_ADMIN (el user_id del administrador en Telegram)
TG_TEST_GROUP (el chat_id del grupo de prueba en Telegram)
TG_DC_GROUP (el chat_id del grupo principal en Telegram)
DISCORD_TOKEN (el token del bot de Discord)
DISCORD_ADMIN (el user_id del administrador en Discord)
DISCORD_ME (el user_id del bot en Discord)
DISCORD_GUILD_DC (el server_id del servidor principal en Discord)
DISCORD_GUILD_TEST (el server_id del servidor de prueba en Discord)
DISCORD_DC_MY_ROLE (el role_id del rol que tiene el bot en el servidor principal en Discord)
DISCORD_DC_CH_NORIEGA (el chat_id del canal de la Noriega en el servidor principal Discord)
DISCORD_DC_CH_GENERAL (el chat_id del canal general en el servidor principal Discord)
DISCORD_DC_CH_RECORDATORIOS (el chat_id del canal de recordatorios en el servidor principal Discord)
DISCORD_TEST_MY_ROLE (el role_id del rol que tiene el bot en el servidor principal en Discord)
DISCORD_TEST_CH_NORIEGA (el chat_id del canal de la Noriega en el servidor principal Discord)
DISCORD_TEST_CH_GENERAL (el chat_id del canal general en el servidor principal Discord)
DISCORD_TEST_CH_RECORDATORIOS (el chat_id del canal de recordatorios en el servidor principal Discord)

- Crear el archivo token.pickle para acceder a Google (hay que hacerlo desde una computadora con interfaz gráfica porque levanta el navegador web):
  - Abrir la cuenta de Google que se va a usar para acceder al calendario e ingresar a https://console.cloud.google.com/apis/credentials.
  - Buscar la aplicación BOT en la sección "ID de clientes OAuth 2.0" y descargar el archivo (última opción a la derecha).
  - Renombrar el archivo descargado a "credentials.json" y ubicarlo en la carpeta local del proyecto (no en el servidor).
  - Levantar el bot en modo DEBUG y mandarle el comando "cal".
  - Debería saltar una url. Abrirla y concederle permisos a la aplicación.
  - Al finalizar debería haberse creado el archivo token.pickle. Moverlo a la carpeta del proyecto en el servidor.

Acceso al servidor:

- Actualmente está corriendo en taller.ext.dc.uba.ar. Se puede acceder a través de ssh.

- Manejar los procesos con tmux
  - Iniciar nueva instancia: tmux
  - Conectarse a una instancia: tmux attach -t <SESION>
  - Renombrar una instancia: tmux rename -t <SESION> <NUEVO_NOMBRE>
  - Listar sesiones: tmux ls
  - Desconectarse de una sesión: tmux detach

- Lanzar el proceso main.py desde la carpeta del proyecto en una sesión de tmux.