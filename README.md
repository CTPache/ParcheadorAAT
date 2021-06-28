# Parcheador Ace Attorney Trilogy
## Introducción
Parcheador de Ace Attorney Trilogy al español. El idioma se inserta como uno más del juego, permitiendo conservar las partidas guardadas de los otros idiomas.

*SI  ESTÁS AQUÍ Y SOLO QUIERES PARCHEAR EL JUEGO, VETE A LA [PESTAÑA DE RELEASES](https://github.com/CTPache/ParcheadorAAT/releases), AUNQUE SE RECOMIENDA LA LECTURA DEL SIGUIENTE DOCUMENTO, SOBRE TODO LA PARTE MARCADA COMO IMPORTANTE.*

![imagen](https://user-images.githubusercontent.com/33907485/121191910-b4c89700-c86c-11eb-9dbd-e0e08f99710c.png)

### IMPORTANTE
- Es posible que el parcheador sea detectado como malware por Windows Defender. [Esto es un problema conocido de PyInstaller, que no tiene nada que ver con nuestro código y que no podemos solucionar](https://github.com/pyinstaller/pyinstaller/issues/5854). 
(En caso de paranoia extrema, siempre puedes revisar el código fuente y compilarlo o ejecutarlo tu mismo.)
- Una vez el parche esté aplicado, tienes que ir a los ajustes y cambiar el idioma desde ahí (Será el último de la lista).
- El parcheador solamente funciona en Windows 10, ya que usa el registro de Windows para buscar el juego. Si usas otra versión de Windows tendrás que modificar el script. Lo mismo para usuarios de Linux. Se admiten pull requests de soporte para otros sistemas operativos.
- En el caso de querer mover la instalación del juego, se recomienda primero moverla con la herramienta de steam, y a continuación comprobar que no haya quedado nada en la ubicación anterior. Si queda algo, se puede cortar y pegar.
- Se recomienda hacer lo mismo si se quiere desinstalar el juego, primero desinstalarlo desde steam y a continuación eliminar el directorio del juego de forma manual.
- A partir de la 1.0.2, el juego descargará el último parcheador por su cuenta si detecta una actualización. Esto implica que el juego puede parcer que se ha colgado al abrirlo, cuando lo que realmente pasa es que está descargando el parcheador para iniciar la actualización. Por eso, recomendamos que si el juego parece que tarda en arrancar no lo cerréis, y simplemente dejéis que acabe de hacer lo suyo.

## Uso
- Descargar la última release compilada.
- Presionar el botón de parchear.
- Esperar a que se descargue y aplique el parche.
- Una vez aplicado, abrir el juego normalmente en Steam. Si el juego aparece en otro idioma, cambiar a español en el menú de opciones.

## Compilación
- Para compilar el ejecutable es necesario el uso de pyinstaller, y es necesaria la librería pyQt5:
  
``pip install pyinstaller pyQt5``
  
- Una vez se cumplan las dependencias, se ejecuta buid.bat, y el ejecutable se compilará como "PatcherNew.exe".

## Troubleshooting

### Es posible que el parcheador no encuentre el directorio del juego.
Eso puede deberse a estos motivos:
  - El juego instalado no es una copia original de Steam, por lo que la variable de registro no existe.
  - El juego no está instalado.
  - El juego se instaló y se movió de forma manual (Cortar y pegar).

En cualquiera de los tres casos, la solución mas sencilla es instalar el juego desde Steam.

### Es posible que el parcheador falle.
 
Desde la versión 1.1.0, el parcheador verifica los contenidos del juego de Steam. Tardará un rato en verificar y descargar los ficheros originales. Una vez estén, se podrá aplicar el parche de forma normal. Si el usuario cierra por su cuenta la ventana de verificación, el parcheador se quedará atascado en un bucle infinito, y habrá que volver a empezar el proceso.

También puede suceder que el parcheador no sea capaz de escribir en el directorio donde se encuentra. Esto puede ser porque no se ha descomprimido, entonces se descomprime a un directorio temporal en el que no puede escribir, o porque no tiene permisos de escritura en el directorio. Esto se puede solcionar de dos maneras:

- Moviendo el ejecutable a un directorio donde tenga permisos, como puede ser el escritorio o la carpeta de Documentos.
- Ejecutándolo como administrador (No recomendado, hacer eso solo si lo anterior no funcionó).


Si necesitas soporte más allá de lo que hay aquí escrito, escribe ene el canal de ``#soporte-parches`` de nuestro [servidor de discord](https://discord.gg/8UgvVG92Hd).

## Créditos del parcheador
- Parcheador escrito por [CTPache](https://github.com/CTPache)

- Interfaz escrita por [CTPache](https://github.com/CTPache) y [legendaryX77](https://github.com/legendaryX77).

- Agradecimientos a [Darkmet98](https://github.com/Darkmet98) por el [parcheador de Disgaea](https://github.com/Darkmet98/DisgaeaPatcher)

## Créditos del parche
- Edición gráfica, revisión y coordinación: [JauCR](https://github.com/JauCR/)

- Romhacking: [CTPache](https://github.com/CTPache) y [WorstAquaPlayer](https://github.com/WorstAquaPlayer)

- Agradecimientos a CAPCOM por la traducción original de DS.
