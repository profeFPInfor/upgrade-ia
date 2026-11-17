<div align="center">

# LLM'S

## OpenRouter

### Trabajo de investigación

<br><br><br>

**Autor:** Iván Álvarez Hernández

**Ciclo formativo:** 2º DAM

**Curso:** 2026-2027

</div>

---


### ¿Qué es OpenRouter?

OpenRouter es una plataforma que permite acceder a diferentes modelos de inteligencia artificial (LLM, *Large Language Models*) desde un mismo lugar y mediante una única API.

Un LLM es un modelo de inteligencia artificial entrenado para comprender y generar lenguaje natural. Estos modelos pueden responder preguntas, resumir textos, analizar documentos, generar código y realizar muchas otras tareas.

Existen distintos proveedores que desarrollan sus propios modelos, como OpenAI, Anthropic, Google o Meta. Cada uno ofrece modelos con características diferentes: algunos destacan por su capacidad de razonamiento, otros por su velocidad y otros por su coste.

El problema es que, si queremos utilizar modelos de varios proveedores en una misma aplicación, normalmente tenemos que adaptar nuestra programación a las características de cada servicio. OpenRouter simplifica este proceso, ya que permite acceder a numerosos modelos mediante una interfaz de API común.

Por tanto, OpenRouter no es un modelo de inteligencia artificial en sí mismo, sino una plataforma que actúa como intermediaria entre una aplicación y los modelos de IA disponibles. Permite seleccionar qué modelo utilizar sin tener que integrar individualmente la API de cada proveedor.

### ¿Cómo funciona?

El funcionamiento de OpenRouter se basa en la comunicación entre una aplicación, la plataforma y el modelo de inteligencia artificial seleccionado.

El proceso se desarrolla de la siguiente manera:

1. La aplicación necesita realizar una tarea. Por ejemplo, un programa puede necesitar resumir un documento, responder una pregunta o generar código.
2. La aplicación envía una petición a OpenRouter. Mediante una solicitud a su API, el programa envía las instrucciones, los datos necesarios y el modelo que desea utilizar.
3. OpenRouter procesa la petición. La plataforma identifica el modelo seleccionado y dirige la solicitud al proveedor correspondiente. Según la configuración, también puede utilizar mecanismos de selección de proveedores o alternativas si se producen determinados fallos.
4. El modelo genera una respuesta. El modelo recibe la información, la procesa y genera un resultado de acuerdo con las instrucciones proporcionadas.
5. OpenRouter devuelve el resultado. La respuesta llega a la aplicación, que puede mostrarla al usuario, almacenarla o utilizarla como parte de otro proceso.

Por ejemplo, si desarrollamos una aplicación de gestión de documentos, esta podría enviar un archivo de texto a OpenRouter para que un modelo de IA lo resumiese, extrajese los datos más importantes y organizase la información en apartados. Posteriormente, la aplicación podría mostrar el resultado al usuario o guardarlo en una base de datos.

Es importante tener en cuenta que OpenRouter facilita la comunicación con los modelos, pero no garantiza que las respuestas sean correctas. La calidad del resultado depende, entre otros factores, del modelo elegido y de la información proporcionada.

### ¿Para qué sirve?

OpenRouter sirve principalmente para facilitar el acceso y la integración de distintos modelos de inteligencia artificial en una misma aplicación. Sus principales utilidades son las siguientes:

- **Acceder a diferentes modelos:** permite utilizar modelos de distintos proveedores a través de una misma API, sin tener que desarrollar una integración independiente para cada uno.
- **Comparar resultados:** facilita probar varios modelos para comprobar cuál ofrece mejores respuestas para una tarea concreta. Por ejemplo, podemos comparar cómo explican un error de programación o cómo resumen un documento.
- **Controlar los costes:** los modelos tienen precios y capacidades diferentes. OpenRouter permite elegir el modelo que mejor se adapte al presupuesto y a las necesidades del proyecto. Algunos modelos pueden ofrecer opciones gratuitas con limitaciones.
- **Cambiar de modelo fácilmente:** si un modelo deja de ser adecuado, resulta demasiado caro o queremos probar uno más avanzado, podemos cambiar la configuración de la aplicación sin rehacer toda la comunicación con el servicio.
- **Configurar alternativas:** permite configurar opciones de respaldo para determinados casos en los que un proveedor o modelo no esté disponible. Esto puede ayudar a mantener el funcionamiento de una aplicación.
- **Integrar inteligencia artificial en otros programas:** permite que aplicaciones web, programas de escritorio, chatbots y sistemas automatizados utilicen modelos de IA para procesar información y generar respuestas.

### ¿En qué ámbitos se utiliza?

OpenRouter puede utilizarse en diferentes sectores y proyectos que necesiten incorporar modelos de inteligencia artificial.

- **Desarrollo de software:** ayuda a integrar funciones que generan código, explican errores, proponen soluciones y crean documentación técnica.
- **Automatización de tareas:** permite desarrollar sistemas que clasifican información, procesan solicitudes, redactan informes o realizan tareas repetitivas a partir de instrucciones.
- **Atención al cliente:** puede utilizarse para crear chatbots y asistentes virtuales capaces de responder preguntas frecuentes y orientar a los usuarios.
- **Análisis de datos y documentos:** permite resumir textos extensos, extraer información relevante, clasificar documentos y organizar grandes cantidades de información.
- **Ciberseguridad:** puede ayudar a interpretar registros, resumir alertas, analizar informes técnicos y documentar incidentes. Sin embargo, sus resultados deben verificarse y no debería utilizarse como única herramienta para tomar decisiones de seguridad.
- **Educación:** puede utilizarse para desarrollar asistentes educativos, explicar conceptos, generar ejercicios y adaptar las explicaciones al nivel del estudiante.
- **Gestión empresarial:** permite automatizar tareas administrativas, clasificar correos electrónicos, resumir reuniones y ayudar a organizar información de una empresa.

### ¿Cómo se utiliza?

OpenRouter se puede utilizar principalmente de dos formas: desde su página web o mediante una API integrada en un programa.

#### 1. Desde su página web

Podemos acceder a [openrouter.ai](https://openrouter.ai/) para consultar el catálogo de modelos disponibles, revisar sus características y probarlos directamente.

Esta opción resulta útil para conocer la plataforma, comparar modelos y comprobar qué resultados ofrecen sin necesidad de desarrollar una aplicación.

Al elegir un modelo, conviene revisar sus capacidades, sus límites de uso y su precio. No todos los modelos ofrecen las mismas prestaciones ni están disponibles en las mismas condiciones.

#### 2. Mediante una API

La API permite conectar OpenRouter con un programa para que este pueda enviar instrucciones a un modelo de inteligencia artificial y recibir sus respuestas automáticamente.

A diferencia del uso desde la página web, esta opción permite incorporar la IA como una funcionalidad más de una aplicación, sin que el usuario tenga que acceder manualmente a OpenRouter.

Para utilizarla, hay que seguir estos pasos:

1. **Crear una cuenta y obtener una clave API.** Desde la página de OpenRouter podemos generar una clave que permita a nuestro programa identificarse al realizar peticiones.
2. **Seleccionar un modelo.** Debemos elegir el modelo que mejor se adapte a la tarea, teniendo en cuenta su calidad, velocidad, precio y límites de uso.
3. **Preparar la petición.** El programa debe indicar el modelo que quiere utilizar y enviar las instrucciones y los datos que necesita procesar. Esta información se transmite mediante una solicitud HTTP.
4. **Enviar la petición a OpenRouter.** La aplicación se comunica con la dirección de la API, incluyendo la clave de autenticación y los datos preparados.
5. **Recibir y procesar la respuesta.** OpenRouter devuelve el resultado generado por el modelo. Nuestro programa puede extraer el texto y mostrarlo en pantalla, guardarlo en una base de datos o utilizarlo para continuar ejecutando otras tareas.

Por ejemplo, una aplicación desarrollada en Python podría enviar un texto a un modelo para que lo resumiese y mostrar el resumen al usuario. El mismo procedimiento se puede adaptar a otros lenguajes de programación.

### Ventajas y desventajas de OpenRouter

OpenRouter ofrece varias ventajas a la hora de desarrollar aplicaciones que utilizan inteligencia artificial, aunque también presenta algunas limitaciones que conviene conocer.

#### Ventajas

- **Centralización:** permite acceder a modelos de distintos proveedores desde una misma API.
- **Flexibilidad:** facilita cambiar de modelo según las necesidades del proyecto.
- **Facilidad de integración:** utiliza una API común, compatible con formatos de peticiones empleados por otros servicios de IA.
- **Variedad de modelos:** permite elegir entre diferentes alternativas según sus capacidades, velocidad y precio.
- **Disponibilidad:** la configuración de proveedores alternativos puede ayudar a mantener el servicio cuando una opción falla.

#### Desventajas

- **Dependencia de un intermediario:** las peticiones pasan por OpenRouter antes de llegar al proveedor del modelo.
- **Costes variables:** el precio depende del modelo y de la cantidad de información procesada. Además, pueden aplicarse tarifas de la plataforma según el plan.
- **Diferencias entre modelos:** no todos los modelos admiten las mismas funciones ni producen resultados de la misma calidad.
- **Necesidad de conexión:** para utilizar la API se necesita acceso a Internet y que los servicios correspondientes estén disponibles.
- **Privacidad:** la información enviada puede pasar por OpenRouter y por el proveedor que ejecuta el modelo. Por ello, es importante revisar las políticas de tratamiento de datos y evitar enviar información confidencial innecesaria.

### Costes y modelos gratuitos

OpenRouter dispone de modelos gratuitos y de pago, por lo que el coste depende de la alternativa elegida y del uso que se haga de ella.

Los modelos gratuitos pueden ser útiles para realizar pruebas, aprender a utilizar la API o desarrollar pequeños prototipos. Sin embargo, pueden tener límites de solicitudes, menor disponibilidad o capacidades diferentes a las de los modelos de pago.

En los modelos de pago, el precio suele calcularse según los *tokens* procesados. Un token es una unidad de texto que utiliza el modelo para interpretar las entradas y generar respuestas. No equivale necesariamente a una palabra: puede representar una palabra completa, una parte de ella o determinados caracteres.

Por ejemplo, si una aplicación envía un documento extenso y solicita un análisis detallado, normalmente consumirá más tokens que si envía una pregunta breve. Por tanto, el coste dependerá tanto del modelo como de la cantidad de información enviada y de la respuesta generada.

Antes de integrar un modelo, conviene consultar su precio y sus límites en la página oficial de [precios de OpenRouter](https://openrouter.ai/pricing). También es recomendable controlar el consumo para evitar gastos inesperados.

### Seguridad y privacidad

La seguridad es un aspecto importante cuando se utiliza OpenRouter dentro de una aplicación, especialmente si se trabaja con documentos, información de usuarios o datos de una empresa.

Hay tres aspectos principales que deben tenerse en cuenta:

- **Protección de la clave API:** debe guardarse de forma segura y no publicarse en repositorios públicos. Si alguien consigue una clave válida, podría utilizarla y generar consumo asociado a la cuenta.
- **Protección de los datos enviados:** antes de enviar información a un modelo, hay que comprobar si contiene datos personales, contraseñas u otra información confidencial. Siempre que sea posible, se deben eliminar los datos que no sean necesarios.
- **Revisión de las políticas de privacidad:** es importante comprobar cómo se gestionan las solicitudes y qué condiciones aplica el proveedor del modelo elegido. Las opciones de privacidad y retención pueden variar según la configuración y el proveedor.

Además, las respuestas generadas por la IA deben revisarse antes de utilizarlas en procesos importantes. Aunque un modelo pueda proporcionar información útil, también puede cometer errores, interpretar mal una instrucción o generar recomendaciones incorrectas.

### ¿Cómo elegir el modelo adecuado?

OpenRouter permite seleccionar entre numerosos modelos, pero no siempre es necesario utilizar el más avanzado. La elección depende de la tarea que se quiera resolver.

Los principales criterios que conviene valorar son:

- **Calidad:** capacidad del modelo para comprender las instrucciones y generar respuestas correctas.
- **Precio:** coste de procesar las entradas y generar las respuestas.
- **Velocidad:** tiempo que tarda en responder, especialmente importante en aplicaciones interactivas.
- **Contexto:** cantidad de información que puede procesar en una petición. Es relevante cuando se analizan documentos extensos.
- **Funciones disponibles:** compatibilidad con las necesidades del proyecto, como trabajar con imágenes, utilizar herramientas externas o generar respuestas estructuradas.
- **Privacidad:** condiciones de tratamiento de los datos por parte del proveedor seleccionado.

Por ejemplo, para clasificar textos sencillos puede ser suficiente un modelo económico. En cambio, para analizar documentación técnica compleja puede interesar un modelo con mayor capacidad de razonamiento.

Lo recomendable es probar varias alternativas con ejemplos reales del proyecto y comparar sus resultados, su velocidad y su coste antes de decidir cuál utilizar.

## Cómo combinar modelos gratuitos de OpenRouter sin gastar dinero

El objetivo es crear un sistema que utilice varios modelos de inteligencia artificial a través de OpenRouter sin generar costes por el uso de la API. Para conseguirlo, se pueden utilizar modelos alternativos, encadenar varios modelos para realizar tareas diferentes o seleccionar el más adecuado según la petición.

Es importante tener en cuenta que los modelos gratuitos tienen límites de uso y disponibilidad. Por tanto, combinar varios modelos no garantiza un funcionamiento ilimitado, pero sí permite aprovechar mejor las opciones gratuitas disponibles.

### 1. Utilizar `openrouter/free`

Una de las formas más sencillas de utilizar modelos gratuitos es mediante el enrutador `openrouter/free`. En lugar de seleccionar manualmente un modelo concreto, la aplicación envía la petición a este enrutador y OpenRouter selecciona un modelo gratuito compatible con ella.

El funcionamiento sería el siguiente:

1. El usuario introduce una petición en la aplicación.
2. La aplicación envía la petición a OpenRouter.
3. OpenRouter selecciona un modelo gratuito compatible.
4. El modelo procesa la información y genera una respuesta.
5. La aplicación recibe el resultado y se lo muestra al usuario.

Por ejemplo, si desarrollamos una aplicación que resume documentos, el usuario podría introducir un texto y la aplicación utilizaría el enrutador para obtener un resumen sin tener que elegir manualmente el modelo.

Sus principales ventajas son la sencillez de integración, la posibilidad de probar diferentes modelos gratuitos y la reducción de la complejidad del código.

Sin embargo, el modelo seleccionado puede variar entre peticiones, la calidad de las respuestas puede ser diferente y existen límites de uso y disponibilidad.

Esta opción resulta especialmente útil para realizar pruebas, desarrollar prototipos y añadir funciones de inteligencia artificial a una aplicación de forma sencilla.

Más información: [Documentación del enrutador de modelos gratuitos](https://openrouter.ai/docs/guides/routing/routers/free-models-router).

### 2. Alternar modelos gratuitos cuando uno falla (fallback)

El *fallback* consiste en preparar una lista de modelos alternativos para que la aplicación pueda probar otro cuando el primero no esté disponible o no pueda completar una petición.

Por ejemplo, podemos establecer tres modelos gratuitos:

- Modelo A: primera opción.
- Modelo B: segunda opción.
- Modelo C: tercera opción.

Cuando el usuario realiza una petición, la aplicación intenta utilizar primero el modelo A. Si este responde correctamente, el proceso termina. Si falla por un problema de disponibilidad o un límite temporal, la aplicación puede intentar utilizar el modelo B. Si tampoco funciona, puede probar el modelo C.

Para implementar esta lógica, el programa debe:

1. Mantener una lista de modelos gratuitos compatibles.
2. Enviar la petición al primer modelo.
3. Comprobar si se ha recibido una respuesta válida.
4. Si se produce un error que permite reintentar, probar el siguiente modelo.
5. Si todos fallan, informar al usuario y detener los intentos.

No conviene cambiar de modelo ante cualquier error. Por ejemplo, si la petición contiene datos incorrectos, utilizar otro modelo probablemente no solucionará el problema.

También es importante distinguir entre el cambio de proveedor para un mismo modelo y el cambio a un modelo diferente. OpenRouter puede gestionar alternativas de proveedores y permite configurar modelos alternativos, pero el comportamiento depende de la configuración utilizada.

Para evitar gastos, todos los modelos de la lista deben tener un precio de entrada y salida de cero. Además, conviene limitar el número de intentos, ya que las peticiones pueden consumir los límites gratuitos disponibles.

Esta estrategia es especialmente útil para aplicaciones que necesitan seguir funcionando cuando un modelo gratuito está saturado o no responde.

### 3. Encadenar modelos para realizar tareas diferentes

Encadenar modelos consiste en utilizar la respuesta de un modelo como entrada del siguiente. En lugar de pedir a todos que realicen exactamente la misma tarea, cada uno se encarga de una fase concreta del proceso.

Por ejemplo, una aplicación de gestión documental podría organizar el trabajo en tres fases:

1. **Extracción de información:** el primer modelo identifica las ideas principales, fechas, nombres y datos relevantes del documento.
2. **Redacción del resumen:** el segundo modelo recibe la información extraída y la transforma en un texto ordenado y comprensible.
3. **Revisión del resultado:** el tercer modelo comprueba la coherencia del resumen y señala posibles omisiones o contradicciones.

De esta manera, una tarea compleja se divide en pasos más sencillos y cada modelo tiene una función específica.

Para mantener el coste de la API en cero, es necesario utilizar modelos gratuitos en todas las fases y comprobar sus precios antes de integrarlos. También conviene limitar la cantidad de información enviada, evitar repetir fases innecesarias y detener el proceso si no quedan alternativas gratuitas disponibles.

Cada fase suele implicar una llamada independiente a la API. Por tanto, utilizar tres modelos normalmente supone realizar tres llamadas, lo que consume más solicitudes gratuitas y puede aumentar el tiempo necesario para obtener el resultado.

Además, encadenar modelos no garantiza una mayor calidad. Un modelo puede introducir errores que el siguiente no detecte, por lo que es recomendable revisar los resultados cuando se utilicen en procesos importantes.

Esta estrategia resulta útil cuando una tarea puede dividirse en fases diferenciadas, como extraer información, resumir documentos, clasificar textos o revisar resultados.

### 4. Seleccionar el modelo según la tarea

Otra posibilidad consiste en elegir el modelo en función del tipo de trabajo que deba realizar la aplicación. Esta técnica se conoce como selección o enrutamiento de modelos.

No todas las tareas necesitan las mismas capacidades. Para resumir un texto breve puede ser suficiente un modelo rápido y ligero, mientras que para explicar código o analizar documentación técnica puede interesar otro con mejores capacidades para esas tareas.

Algunos ejemplos de selección son:

- **Resumir textos breves:** utilizar un modelo rápido que siga correctamente las instrucciones.
- **Clasificar documentos:** elegir un modelo capaz de asignar categorías de forma consistente.
- **Explicar código Java:** utilizar un modelo con buenas capacidades de programación.
- **Analizar documentación extensa:** buscar un modelo con una ventana de contexto amplia.
- **Revisar textos:** seleccionar un modelo capaz de comparar información y detectar posibles inconsistencias.

La aplicación puede identificar la tarea mediante reglas programadas. Por ejemplo, si el usuario solicita un resumen, se selecciona una ruta; si pide una explicación de código, se utiliza otra.

También es posible utilizar un modelo gratuito para clasificar la petición y decidir qué modelo debe responder. Sin embargo, esto añade una llamada adicional a la API, por lo que en aplicaciones sencillas puede ser preferible empezar con reglas básicas.

Esta estrategia se puede combinar con el *fallback*. Primero se selecciona el modelo más adecuado para la tarea y, si no está disponible, se prueba una alternativa gratuita compatible.

Su principal ventaja es que permite adaptar el uso de los modelos a las necesidades de cada operación, evitando llamadas innecesarias y aprovechando mejor los recursos gratuitos.

### 5. Cómo mantener el coste en cero

Para conseguir que el uso de la API tenga un coste de cero euros, no basta con elegir modelos gratuitos. También es necesario controlar los precios, los límites de uso y las llamadas realizadas por la aplicación.

#### 5.1. Utilizar exclusivamente modelos gratuitos

OpenRouter ofrece modelos con identificadores terminados en `:free`, además del enrutador `openrouter/free`. Estas opciones permiten utilizar modelos gratuitos, aunque sus condiciones y límites pueden variar.

Antes de integrar un modelo, conviene comprobar su precio de entrada y salida, sus restricciones y su disponibilidad.

Se pueden consultar los modelos disponibles en las siguientes páginas:

- [Catálogo de modelos gratuitos](https://openrouter.ai/collections/free-models)
- [Precios de OpenRouter](https://openrouter.ai/pricing)

#### 5.2. Evitar los modelos de pago como alternativa

Es importante comprobar que todos los modelos configurados como alternativas sean gratuitos.

Por ejemplo, si el modelo A es gratuito, pero el modelo B tiene un coste, una configuración de *fallback* podría terminar utilizando el modelo B cuando el primero falle.

Para evitarlo, hay que configurar únicamente modelos gratuitos y no permitir que el sistema recurra automáticamente a opciones de pago. El enrutador gratuito también debe utilizarse conforme a sus condiciones vigentes.

#### 5.3. Controlar los límites de uso

Los modelos gratuitos suelen tener límites de solicitudes y disponibilidad. Estos límites pueden variar según el proveedor, el modelo y las condiciones de la cuenta.

Además, cada llamada realizada durante una cadena de modelos o un proceso de *fallback* puede consumir parte del cupo disponible.

Por ello, conviene consultar las restricciones actuales de OpenRouter, controlar el número de solicitudes y evitar realizar llamadas que no sean necesarias.

#### 5.4. Evitar reintentos ilimitados

Si una petición falla, la aplicación no debería intentarlo indefinidamente. Una solución consiste en establecer un número máximo de intentos y detener el proceso cuando se hayan agotado las alternativas.

Por ejemplo, se puede intentar utilizar el modelo A, después el B y finalmente el C. Si ninguno responde correctamente, la aplicación informa del error y permite intentarlo de nuevo más adelante.

Esto evita consumir solicitudes innecesariamente y reduce el riesgo de alcanzar rápidamente los límites gratuitos.

#### 5.5. Reducir las llamadas innecesarias

No todas las tareas requieren varios modelos. Si una petición se resuelve correctamente con un único modelo, no es necesario enviar el resultado a otros modelos para repetir el trabajo.

Reducir las llamadas permite aprovechar mejor los límites gratuitos, disminuir el tiempo de respuesta y reducir la posibilidad de que aparezcan errores durante el proceso.

En definitiva, mantener el coste de la API en cero requiere utilizar modelos con precios gratuitos, controlar las alternativas y limitar las llamadas realizadas.

### 6. Sistema recomendado para una aplicación

Para una primera aplicación, una buena opción consiste en combinar la selección de modelos según la tarea con un sistema de *fallback*. El encadenamiento se puede reservar para aquellas operaciones que realmente necesiten varias fases.

El funcionamiento general sería el siguiente:

1. El usuario envía una petición a la aplicación.
2. El programa identifica el tipo de tarea que debe realizar.
3. Selecciona un modelo gratuito compatible.
4. Envía la petición a OpenRouter.
5. Si el modelo falla por una causa que permite reintentar, prueba otro modelo gratuito.
6. Si la tarea necesita varias fases, utiliza modelos adicionales únicamente cuando sea necesario.
7. Si se agotan las alternativas, muestra un mensaje de error sin recurrir a modelos de pago.

Esta arquitectura combina flexibilidad y control del consumo. Permite aprovechar distintos modelos gratuitos sin depender de uno solo y evita añadir pasos innecesarios a cada petición.

En conclusión, existen dos estrategias principales que pueden combinarse: utilizar modelos alternativos para mejorar la disponibilidad y encadenar modelos para dividir tareas complejas. La selección del modelo según la tarea permite completar el sistema y aprovechar mejor los recursos disponibles.

No obstante, un coste de API de cero euros no implica disponer de capacidad ilimitada ni garantiza que los modelos estén siempre disponibles. Para mantener el sistema gratuito, es necesario respetar los límites de uso y comprobar periódicamente las condiciones de OpenRouter.