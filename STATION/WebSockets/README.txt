==========================================================
INSTRUCCIONES DE EJECUCIÓN - PROYECTO WEBSOCKETS
==========================================================

PASO 1: PREPARACIÓN EN PC1 (SERVIDOR)
--------------------------------------
1. Conecta la cámara USB.
2. Abre una terminal y dale permisos al dispositivo:
   $ sudo chmod 666 /dev/video3

3. Entra en la carpeta del proyecto y lanza el contenedor:
   $ docker compose build --no-cache
   $ docker compose up

4. Obtén la IP de este PC para que el PC2 se conecte:
   $ hostname -I


PASO 2: EJECUCIÓN EN PC2 (CLIENTE)
--------------------------------------
1. Asegúrate de estar en la misma red local que el PC1.
2. Abre cualquier navegador web (Chrome, Firefox, etc.).
3. En la barra de direcciones, escribe la IP del PC1 seguida del puerto 8000:
   http://[IP_DEL_PC1]:8000

   (Ejemplo: http://192.168.1.50:8000)


VERIFICACIÓN DE DATOS
---------------------
- En la pantalla del PC2: Verás el video y los comandos enviados.
- En la terminal del PC1: Verás los logs de los comandos JSON recibidos
  (steering, brake, throttle) en tiempo real.

==========================================================