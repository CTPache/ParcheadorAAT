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
Lo más habitual es que suceda al principio, cuando falta un único fichero por parchear (el Assembly-CSharp.dll). Esto es a causa de estar utilizando una versión de este binario diferente a la versión vanilla de Steam. En caso de haber aplicado otro parche anteriormente, se debe restaurar este fichero para aplicar el parche nuevo. Esto se hace fácilmente desde la interfaz de steam:
- En la página del juego, se abre la rueda dentada, y se pulsa en "Propiedades...".
- En el menú que aparece, se navega hasta "Archivos locales"
- A continuación, pulsar el botón de "Verificar integridad de los archivos de juego..."
 
Tardará un rato en verificar y descargar los ficheros originales. Una vez estén, se podrá aplicar el parche de forma normal.

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
