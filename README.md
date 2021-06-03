# Parcheador Ace Attorney Trilogy

## Uso
- Descargar la última release compilada.
- Presionar el botón de parchear.
- Esperar a que se descargue y aplique el parche.
- Una vez aplicado, abrir el juego normalmente en Steam. Si el juego aparece en otro idioma, cambiar a español en el menú de opciones.

## Compilación
- Para compilar el ejecutable es necesario el uso de pyinstaller, y es necesaria la librería pyQt5:
  
`` pip install pyinstaller pyQt5``
  
- Una vez se cumplan las dependencias, se ejecuta buid.bat, y el ejecutable se compilará como "PatcherNew.exe".

## Troubleshooting

### Es posible que el parcheador no encuentre el directorio del juego.
Eso puede deberse a 2 motivos:
  - El juego instalado no es una copia original de Steam, por lo que la variable de registro no existe.
  - El juego no está instalado.

En cualquiera de los dos casos, la solución es instalar el juego desde Steam.

### Es posible que el parcheador falle.
Lo más habitual es que suceda al final, cuando falta un único fichero por parchear (el Assembly-CSharp.dll). Esto es a causa de estar utilizando una versión de este binario diferente a la versión vanilla de Steam. En caso de haber aplicado otro parche anteriormente, se debe restaurar este fichero para aplicar el parche nuevo. Esto se hace fácilmente desde la interfaz de steam:
- En la página del juego, se abre la rueda dentada, y se pulsa en "Propiedades...".
- En el menú que aparece, se navega hasta "Archivos locales"
- A continuación, pulsar el botón de "Verificar integridad de los archivos de juego..."

Tardará un rato en verificar y descargar los ficheros originales. Una vez estén, se podrá aplicar el parche de forma normal.

## Créditos
- Parcheador escrito por [CTPache](https://github.com/CTPache)

- Interfaz escrita por [CTPache](https://github.com/CTPache) y [legendaryX77](https://github.com/legendaryX77).

- Agradecimientos a [Darkmet98](https://github.com/Darkmet98) por el [parcheador de Disgaea](https://github.com/Darkmet98/DisgaeaPatcher)

## Créditos del parche
- Edición gráfica, revisión y coordinación: [JauCR](https://github.com/JauCR/)
- Romhacking: [CTPache](https://github.com/CTPache) y [WorstAquaPlayer](https://github.com/WorstAquaPlayer)
- Agradecimientos a CAPCOM por la traducción original de DS.
