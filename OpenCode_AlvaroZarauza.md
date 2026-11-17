# OpenCode: análisis de una herramienta de programación basada en inteligencia artificial

**Trabajo de investigación**

**Ciclo formativo:** Desarrollo de Aplicaciones Multiplataforma (2º DAM)

**Módulo:** Digitalizacón 

**Autor:** Álvaro Zarauza Galindo

**Centro educativo:** CIFP La Laboral

**Curso académico:** 2026–2027

**Fecha de entrega:** 28/10/2026

# Índice
- [OpenCode: análisis de una herramienta de programación basada en inteligencia artificial](#opencode-análisis-de-una-herramienta-de-programación-basada-en-inteligencia-artificial)
- [Índice](#índice)
- [Introducción y objetivos](#introducción-y-objetivos)
- [Origen, desarrollo y licencia](#origen-desarrollo-y-licencia)
- [Arquitectura y funcionamiento técnico](#arquitectura-y-funcionamiento-técnico)
- [Ejecución local](#ejecución-local)
- [Seguridad, permisos y privacidad](#seguridad-permisos-y-privacidad)
- [Modelos de inteligencia compatibles](#modelos-de-inteligencia-compatibles)
- [Instalación y configuración](#instalación-y-configuración)
- [Aplicaciones prácticas](#aplicaciones-prácticas)
- [Comparación con otras herramientas](#comparación-con-otras-herramientas)
- [Ventajas y limitaciones](#ventajas-y-limitaciones)
- [Conclusiones](#conclusiones)

# Introducción y objetivos

Introducción

La inteligencia artificial está adquiriendo una gran importancia en el desarrollo de software, ya que permite automatizar tareas, generar código y facilitar la detección de errores. En este contexto, han surgido herramientas como OpenCode, un agente de programación de código abierto que utiliza modelos de lenguaje grandes (LLM) para ayudar a los desarrolladores a trabajar con sus proyectos.

OpenCode permite analizar archivos, generar y modificar código y ejecutar distintas tareas de programación mediante instrucciones en lenguaje natural. Además, admite diferentes proveedores de inteligencia artificial, lo que ofrece flexibilidad a la hora de seleccionar los modelos y adaptar la herramienta a las necesidades de cada proyecto.

# Origen, desarrollo y licencia

Desarrollo de OpenCode

El desarrollo de OpenCode comenzó en abril de 2025 bajo la organización SST, con el objetivo de crear una herramienta de programación de código abierto basada en inteligencia artificial. El proyecto permite utilizar modelos de lenguaje para ayudar a escribir, analizar y modificar código. Posteriormente, su repositorio pasó a estar asociado a AnomalyCo, organización bajo la que continúa su desarrollo.

Desde sus inicios, OpenCode ha evolucionado para ofrecer distintas interfaces, como el terminal, la aplicación de escritorio y las extensiones para editores de código, además de admitir diferentes proveedores de modelos de inteligencia artificial.

Licencia de OpenCode

OpenCode utiliza la licencia MIT, una licencia de software libre y de código abierto de carácter permisivo. Esta permite utilizar, copiar, modificar y distribuir el programa, incluso con fines comerciales, siempre que se mantengan los avisos de copyright y el texto de la licencia. La licencia también establece que el software se proporciona sin garantías. Es importante tener en cuenta que se aplica al código de OpenCode, mientras que los modelos de inteligencia artificial y los proveedores externos utilizados pueden tener sus propias licencias y condiciones de uso.

# Arquitectura y funcionamiento técnico

OpenCode es un agente de programación de código abierto que conecta un modelo de inteligencia artificial con el entorno de desarrollo. Está disponible mediante terminal, aplicación de escritorio y extensiones para editores de código.

Su funcionamiento se puede resumir en cuatro partes:

1. Interfaz de usuario: permite al programador escribir instrucciones y consultar las respuestas de la IA.
2. Agente de programación: interpreta las instrucciones y coordina las tareas necesarias para resolverlas.
3. Modelo de inteligencia artificial: genera respuestas y propuestas de código. Puede conectarse a distintos proveedores o utilizar modelos locales compatibles.
4. Herramientas de desarrollo: permiten al agente consultar archivos, buscar información y, según sus permisos, modificar código o ejecutar comandos.

Por ejemplo, si un desarrollador solicita crear una clase en Java, OpenCode transmite la petición al modelo configurado, recibe una propuesta y puede utilizar sus herramientas para incorporar los cambios al proyecto, según los permisos establecidos. El desarrollador puede revisar el resultado y comprobar que funciona correctamente.

# Ejecución local

OpenCode se ejecuta localmente en el ordenador del desarrollador, desde donde puede acceder a los archivos del proyecto y utilizar herramientas para analizar o modificar código. Para generar respuestas, se conecta al proveedor de inteligencia artificial y al modelo seleccionado, por lo que ejecutar OpenCode localmente no significa necesariamente que el modelo también funcione en el propio ordenador.

También es posible utilizar modelos locales compatibles, dependiendo de la configuración. El usuario puede revisar los cambios realizados y configurar los permisos de las herramientas antes de permitir determinadas acciones. Esta arquitectura permite integrar la inteligencia artificial en el flujo de trabajo habitual sin necesidad de trasladar todo el proyecto a una plataforma de desarrollo en la nube.

# Seguridad, permisos y privacidad

Seguridad y permisos

OpenCode incorpora un sistema de permisos que permite controlar las acciones que puede realizar la inteligencia artificial, como leer archivos, modificar código, ejecutar comandos en el terminal o acceder a recursos web. Según la configuración, estas acciones pueden permitirse automáticamente, requerir la aprobación del usuario o bloquearse. También es posible establecer restricciones específicas para proteger archivos sensibles, como los que contienen variables de entorno y claves de acceso.

Privacidad

En cuanto a la privacidad, OpenCode se ejecuta en el ordenador del usuario, pero los datos enviados al modelo de inteligencia artificial pueden ser procesados por el proveedor seleccionado, de acuerdo con sus propias políticas. Por tanto, ejecutar la herramienta localmente no garantiza que toda la información permanezca en el equipo. Además, OpenCode no incorpora un aislamiento de seguridad completo por defecto, por lo que es recomendable revisar los permisos, evitar compartir credenciales y utilizar entornos aislados, como contenedores, cuando se trabaje con proyectos sensibles.

# Modelos de inteligencia compatibles

OpenCode no depende de un único modelo de inteligencia artificial, sino que permite conectarse a diferentes proveedores. Esto posibilita elegir modelos en función de su calidad de generación de código, velocidad, coste y capacidad para manejar proyectos complejos.

Existen proveedores que ofrecen modelos gratuitos con límites de uso, servicios de pago por consumo y alternativas que permiten ejecutar modelos localmente. Por tanto, que OpenCode sea gratuito y de código abierto no significa que todos los modelos compatibles sean gratuitos. Antes de elegir uno, conviene comprobar sus condiciones, requisitos de hardware y política de privacidad.

# Instalación y configuración

OpenCode dispone de documentación oficial con instrucciones de instalación y configuración. El procedimiento depende del sistema operativo y del método elegido. Una vez instalado, es necesario abrirlo en el directorio del proyecto, configurar el proveedor de inteligencia artificial y seleccionar el modelo que se va a utilizar.

La configuración debe incluir también la revisión de los permisos de las herramientas, para evitar que el agente realice modificaciones o ejecute comandos sin el control adecuado. Para documentar este apartado, conviene registrar los pasos realizados, los requisitos y cualquier problema encontrado durante la instalación.

# Aplicaciones prácticas

OpenCode puede utilizarse para distintas tareas dentro del desarrollo de software, entre ellas:

- Generar clases, métodos y funciones a partir de instrucciones.
- Explicar código existente y ayudar a comprender proyectos desconocidos.
- Detectar posibles errores y proponer correcciones.
- Crear pruebas unitarias y ayudar a documentar el código.
- Modificar proyectos existentes y colaborar en tareas de refactorización.
- Ayudar a desarrollar API REST y aplicaciones con tecnologías como Java y Spring Boot.

# Comparación con otras herramientas

OpenCode compite con otras herramientas de programación basadas en inteligencia artificial, como GitHub Copilot y Claude Code. Aunque todas ayudan a desarrollar software, se diferencian en su licencia, las posibilidades de configuración y la forma de integrarse en el entorno de trabajo.

La principal ventaja de OpenCode es su flexibilidad: permite elegir entre distintos proveedores de inteligencia artificial y utilizar modelos locales compatibles. Además, su código abierto facilita examinar y adaptar el funcionamiento de la herramienta. Sin embargo, configurarlo puede requerir más conocimientos técnicos y el uso de determinados modelos puede generar costes.

# Ventajas y limitaciones

Entre las principales ventajas de OpenCode destacan su código abierto, la flexibilidad para seleccionar modelos, la integración con proyectos existentes y la posibilidad de automatizar tareas de programación. Además, permite adaptar su configuración a diferentes necesidades de desarrollo.

Sus limitaciones incluyen la posibilidad de que genere código incorrecto, la necesidad de revisar los cambios, los costes que pueden derivarse del uso de modelos externos y los requisitos de hardware cuando se utilizan modelos locales. También requiere prestar atención a los permisos y a la información que se envía a los proveedores.

Por ello, OpenCode debe entenderse como una herramienta de apoyo al programador, no como un sustituto de las pruebas, la revisión del código y el criterio técnico.

# Conclusiones

OpenCode es una herramienta de programación asistida por inteligencia artificial que destaca por su carácter abierto y por la flexibilidad para utilizar distintos modelos y proveedores. Puede facilitar tareas como la generación de código, la comprensión de proyectos y la detección de errores, por lo que resulta una opción interesante en el desarrollo de aplicaciones informáticas.

Sin embargo, su utilidad depende del modelo seleccionado, de la configuración y de la complejidad de la tarea. La revisión del código, la ejecución de pruebas y la gestión de los permisos siguen siendo esenciales. La prueba práctica permitirá valorar con mayor precisión sus ventajas y limitaciones en un contexto de desarrollo real.