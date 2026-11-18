# Herdr: documentación y guía de uso

> **Fecha de consulta:** 17 de noviembre de 2026  
> **Web oficial:** <https://herdr.dev/>  
> **Estado de esta documentación:** guía explicativa elaborada a partir de la web, la documentación oficial y los repositorios públicos de Herdr. Los comandos y las opciones pueden cambiar entre versiones.

## Índice

1. [Qué es Herdr](#1-qué-es-herdr)
2. [Para qué sirve](#2-para-qué-sirve)
3. [Conceptos principales](#3-conceptos-principales)
4. [Cómo funciona internamente](#4-cómo-funciona-internamente)
5. [Gestión y coordinación de agentes](#5-gestión-y-coordinación-de-agentes)
6. [Trabajo con varios equipos](#6-trabajo-con-varios-equipos)
7. [Personalización y extensibilidad](#7-personalización-y-extensibilidad)
8. [Aplicación móvil](#8-aplicación-móvil)
9. [Instalación](#9-instalación)
10. [Primeros pasos](#10-primeros-pasos)
11. [Comandos útiles de `herdr-core`](#11-comandos-útiles-de-herdr-core)
12. [Privacidad y seguridad](#12-privacidad-y-seguridad)
13. [Limitaciones y aspectos que conviene conocer](#13-limitaciones-y-aspectos-que-conviene-conocer)
14. [Herdr frente a Herdr TUI](#14-herdr-frente-a-herdr-tui)
15. [Ventajas, inconvenientes y casos recomendados](#15-ventajas-inconvenientes-y-casos-recomendados)
16. [Recursos oficiales](#16-recursos-oficiales)

---

## 1. Qué es Herdr

**Herdr es una aplicación de escritorio de código abierto para organizar terminales y agentes de programación**, especialmente herramientas de desarrollo basadas en inteligencia artificial, como Claude Code o Codex.

Su objetivo principal es permitir que una persona gestione varios procesos y agentes de programación desde una única interfaz. En lugar de abrir una ventana de terminal independiente para cada tarea, Herdr agrupa el trabajo en espacios, pestañas y paneles, y ofrece una vista general del estado de los agentes.

Una característica importante es que los procesos no dependen de que la ventana gráfica permanezca abierta. La aplicación separa la interfaz del entorno que mantiene vivos los terminales: **Herdr muestra y organiza el trabajo, mientras que `herdr-core` ejecuta y mantiene los procesos**.

Herdr no es, por sí mismo, un modelo de inteligencia artificial ni un IDE que sustituya al editor de código. Tampoco obliga a utilizar un agente concreto. Proporciona el entorno en el que se pueden ejecutar herramientas de terminal, agentes de programación, servidores de desarrollo, pruebas y otros comandos.

La aplicación se distribuye gratuitamente y su código está publicado bajo la licencia Apache 2.0.

## 2. Para qué sirve

Herdr resulta especialmente útil cuando se trabaja con varias tareas de desarrollo al mismo tiempo o se delegan partes de un proyecto en distintos agentes.

### 2.1. Administrar varios agentes desde un único lugar

Permite mantener varios agentes trabajando en diferentes repositorios, ramas o tareas. Desde la barra lateral se puede consultar qué agentes están ocupados, cuáles han terminado y cuáles necesitan una respuesta.

Por ejemplo, se podría tener simultáneamente:

- Un agente modificando una funcionalidad de una aplicación.
- Otro ejecutando pruebas automatizadas.
- Un tercero revisando los cambios de una rama.
- Un terminal ejecutando el servidor local del proyecto.

### 2.2. Mantener procesos en ejecución

Los programas se ejecutan dentro de `herdr-core`, no dentro de la ventana visual. Por eso, cerrar la ventana de Herdr no termina automáticamente los procesos de los paneles que siguen abiertos.

Esto es útil para dejar ejecutándose compilaciones, pruebas largas, servidores de desarrollo o agentes que tardan bastante en completar una tarea.

### 2.3. Delegar trabajo entre agentes

Un agente puede iniciar otros agentes auxiliares, asignarles tareas y recibir sus resultados. Así, un agente principal puede continuar trabajando mientras otro analiza una parte del proyecto.

Un ejemplo sería pedir a un agente principal que implemente una función y, al mismo tiempo, iniciar otro agente para revisar los cambios o ejecutar una batería de pruebas.

### 2.4. Trabajar en equipos o máquinas remotas

Herdr puede conectarse mediante SSH a servidores, máquinas virtuales y otros equipos. Los terminales se ejecutan en la máquina remota, pero pueden consultarse desde la misma interfaz que los terminales locales.

Esto permite, por ejemplo, trabajar desde el ordenador personal con agentes que se ejecutan en un servidor o en una máquina virtual.

### 2.5. Consultar el trabajo desde el móvil

La aplicación móvil permite localizar agentes, abrir sus terminales y responder a sus preguntas desde un teléfono o una tableta, siempre que las máquinas estén configuradas para permitir la conexión.

## 3. Conceptos principales

La aplicación organiza el trabajo mediante varios elementos jerárquicos:

| Elemento | Función |
|---|---|
| **Machine (máquina)** | Equipo local o remoto donde se ejecuta `herdr-core` y viven los terminales. |
| **Space (espacio)** | Agrupación de trabajo asociada normalmente a un repositorio, proyecto o tarea. |
| **Tab (pestaña)** | Vista dentro de un espacio. Puede separar, por ejemplo, el agente, los registros y el servidor de desarrollo. |
| **Pane (panel)** | Terminal real que muestra la salida de un programa. Una pestaña puede dividirse en varios paneles. |
| **Agent (agente)** | Proceso de programación que Herdr puede identificar y cuyo estado puede mostrar. |
| **Layout (disposición)** | Organización visual de la ventana, sus paneles y sus elementos de interfaz. |
| **Mod** | Extensión escrita en JavaScript que añade o modifica elementos y comportamientos de la interfaz. |

### Ejemplo de organización

Una forma razonable de estructurar un proyecto sería:

```text
Máquina local
└── Space: Proyecto web
    ├── Tab: Desarrollo
    │   ├── Pane: Claude Code
    │   └── Pane: Servidor local
    ├── Tab: Pruebas
    │   ├── Pane: Ejecución de tests
    │   └── Pane: Codex - revisión
    └── Tab: Git
        └── Pane: Terminal Git
```

La idea es mantener las tareas relacionadas dentro del mismo espacio y separarlas en pestañas o paneles cuando sea conveniente.

## 4. Cómo funciona internamente

### 4.1. Separación entre interfaz y procesos

La arquitectura de Herdr se apoya en dos componentes principales:

- **Herdr (aplicación de escritorio):** proporciona la interfaz gráfica. Permite abrir espacios, cambiar de pestaña, dividir terminales, consultar agentes y personalizar la presentación.
- **`herdr-core`:** es el componente de ejecución. Mantiene los terminales y los programas que se ejecutan en ellos, y proporciona una interfaz de control para la aplicación, scripts y agentes.

De forma simplificada:

```text
┌──────────────────────────────────────────────┐
│          Aplicación Herdr (interfaz)         │
│                                              │
│  Espacios · Pestañas · Paneles · Agentes     │
└──────────────────────┬───────────────────────┘
                       │ Control y visualización
                       ▼
┌──────────────────────────────────────────────┐
│                 herdr-core                   │
│                                              │
│  Terminales · Procesos · Estado · API        │
└──────────────────────┬───────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Agente       Pruebas      Servidor
      de IA         del código   de desarrollo
```

Esta separación explica por qué la ventana puede cerrarse sin finalizar los terminales. La interfaz se puede volver a conectar al núcleo y mostrar los procesos que siguen activos.

### 4.2. Persistencia de terminales

Mientras `herdr-core` continúe funcionando, los terminales pueden permanecer activos aunque:

- Se cierre la ventana de Herdr.
- Se cierre el terminal desde el que se abrió la aplicación.
- Se actualice la aplicación de escritorio.
- Se pierda temporalmente la conexión SSH desde el equipo cliente.

Hay una distinción importante: **cerrar la ventana no es lo mismo que cerrar un panel o una pestaña**. Según la documentación de la aplicación, cerrar un panel o una pestaña termina sus terminales.

Tampoco debe confundirse la persistencia con la reanudación automática de cualquier tarea. Si el equipo se reinicia o `herdr-core` deja de funcionar inesperadamente, los paneles conservados pueden volver a aparecer con una nueva shell en la última carpeta utilizada, pero el programa anterior no se vuelve a ejecutar automáticamente.

### 4.3. Identificación del estado de los agentes

Herdr utiliza el protocolo abierto **OSC 7501**, denominado *Program Status Protocol*, para recibir información de estado desde los programas que lo implementan.

Entre los estados que puede mostrar se encuentran:

| Estado | Significado |
|---|---|
| `Working` | El agente está trabajando. |
| `Blocked` | El agente está esperando una respuesta o intervención. |
| `Done` | El agente ha terminado. |
| `Idle` | El agente está inactivo o su trabajo ya se ha revisado. |

El núcleo no necesita interpretar el texto que aparece en pantalla ni deducir el estado leyendo la conversación. El propio programa comunica su estado mediante el protocolo.

Un ejemplo de señal de estado bloqueado documentada por Herdr es:

```sh
printf '\e]7501;state=blocked:app=my-agent\e\\'
```

Esto tiene una consecuencia: **un programa puede ejecutarse en Herdr aunque no aparezca como agente reconocido en la lista de estados**. Si no implementa OSC 7501, seguirá funcionando en el terminal, pero no proporcionará necesariamente esa información visual.

## 5. Gestión y coordinación de agentes

### 5.1. Supervisión centralizada

La barra lateral agrupa los agentes de los distintos espacios y máquinas. De esta manera, no es necesario cambiar continuamente entre terminales para comprobar cuál necesita atención.

Al seleccionar un agente se puede abrir su terminal. Los agentes auxiliares que no tengan un panel visible pueden consultarse mediante una vista previa (*peek*) y, si interesa, mantenerse después como una pestaña.

### 5.2. Agentes auxiliares

`herdr-core` permite crear relaciones entre un agente principal y otros agentes secundarios. El principal puede:

1. Iniciar un agente auxiliar.
2. Enviarle una instrucción concreta.
3. Continuar con su propia tarea.
4. Esperar a que el auxiliar termine.
5. Leer el resultado que devuelve.
6. Enviar nuevas indicaciones si necesita ampliar o corregir el trabajo.

La comunicación se puede realizar mediante comandos de `hc`, como `hc send`, y los agentes pueden informar al proceso que los inició.

### 5.3. Ejemplo práctico

Imaginemos que se está desarrollando una aplicación Java. Se podría organizar el trabajo de esta forma:

- **Agente principal:** implementa una nueva funcionalidad.
- **Agente revisor:** examina los cambios y busca errores potenciales.
- **Agente de pruebas:** ejecuta pruebas y devuelve los resultados.
- **Terminal adicional:** mantiene en ejecución la aplicación para probarla manualmente.

El agente principal puede recibir los informes de los auxiliares sin que el usuario tenga que copiar manualmente información entre distintas ventanas.

## 6. Trabajo con varios equipos

Herdr admite máquinas remotas accesibles por **SSH**. La máquina remota necesita tener disponible `herdr-core`; la aplicación permite añadirla desde la configuración o desde la barra lateral.

Una vez conectada:

- Los espacios y terminales remotos aparecen integrados en la interfaz.
- Los programas se ejecutan en el equipo remoto, no en el ordenador que muestra la ventana.
- Los archivos permanecen en la máquina donde se ejecutan los procesos.
- El trabajo puede continuar aunque se cierre la aplicación local o el portátil entre en suspensión, siempre que la máquina remota y su núcleo sigan funcionando.

Herdr también puede utilizarse junto con **Tailscale** u otra VPN para facilitar el acceso a equipos que no están en la misma red local.

El acceso remoto no significa que Herdr aloje los proyectos en sus propios servidores. La comunicación entre la aplicación móvil o de escritorio y las máquinas configuradas se realiza directamente mediante SSH; la empresa indica que los terminales no pasan por un servidor intermediario suyo.

## 7. Personalización y extensibilidad

Una de las características distintivas de Herdr es que gran parte de su interfaz se puede adaptar mediante archivos.

### 7.1. Configuración local

La carpeta de configuración predeterminada de la aplicación es:

```text
~/.config/herdr-app/
```

Entre los elementos que puede contener se encuentran:

```text
herdr-app/
├── AGENTS.md
├── settings.json
├── keys.json
├── layouts/
├── mods/
└── themes/
```

- `AGENTS.md`: guía que explica a los agentes cómo pueden inspeccionar y modificar la configuración de Herdr.
- `settings.json`: preferencias generales, como fuentes, tema y sonidos.
- `keys.json`: asignaciones de teclas y atajos.
- `layouts/`: disposiciones de la ventana.
- `mods/`: extensiones y modificaciones de la interfaz.
- `themes/`: temas visuales.

La ruta puede variar si se configura `XDG_CONFIG_HOME` o `HERDR_APP_HOME`.

### 7.2. Personalización mediante lenguaje natural

Herdr está diseñado para que un agente de programación pueda modificar su propia interfaz. La aplicación incluye una guía local en `AGENTS.md` para explicar qué puede cambiarse y cómo hacerlo.

Por ejemplo, se puede pedir a un agente:

```text
Crea una disposición que muestre mis agentes como tarjetas
organizadas en tres columnas: necesitan atención, trabajando y terminados.
```

El agente puede crear una disposición nueva sin necesidad de reemplazar la original.

Otros ejemplos posibles:

- Añadir un contador de tiempo a cada pestaña.
- Mostrar un panel con información de un servidor.
- Cambiar fuentes, colores y sonidos.
- Crear un panel de seguimiento de tareas.
- Añadir notificaciones externas cuando un agente necesite atención.

### 7.3. Layouts y mods

Un *layout* define cómo se organiza la ventana. Un *mod* es un pequeño programa JavaScript que puede dibujar paneles, menús y diálogos o añadir comportamientos.

Es recomendable duplicar una disposición o extensión incluida de serie antes de modificarla. De este modo se conserva la versión original y se puede experimentar con una copia propia.

Las modificaciones guardadas se vuelven a cargar en la interfaz. La aplicación también indica que, si una edición falla, conserva la última versión funcional.

## 8. Aplicación móvil

Herdr dispone de aplicaciones para iPhone, iPad y Android. No son simplemente una captura o réplica visual del escritorio: permiten conectarse a los terminales reales de las máquinas configuradas.

Sus funciones principales incluyen:

- Consultar una bandeja de agentes ordenada por necesidad de atención, finalizados, trabajando e inactivos.
- Abrir un agente y escribir directamente en su terminal.
- Enviar texto, capturas o imágenes y utilizar dictado.
- Buscar agentes de distintas máquinas.
- Consultar los espacios y pestañas disponibles.
- Recibir avisos mientras la aplicación móvil está abierta cuando un agente necesita atención o termina.

La conexión se realiza por SSH con `herdr-core`. La aplicación móvil **no es compatible con Herdr TUI**, porque esa versión utiliza un servidor diferente.

La aplicación móvil se ofrece gratuitamente, según la información publicada por el proyecto.

## 9. Instalación

La web oficial ofrece instaladores para Windows, macOS y Linux. Los comandos siguientes corresponden a la **aplicación de escritorio Herdr**, no a Herdr TUI.

### 9.1. Windows

La documentación del repositorio indica soporte para Windows x64 y Windows 10 versión 1803 o posterior, con `curl` y `tar` disponibles para el instalador.

Abrir PowerShell y ejecutar:

```powershell
irm https://releases.herdr.dev/app/install.ps1 | iex
```

El instalador añade Herdr al menú Inicio y configura la ruta del ejecutable para el usuario. Es posible que haya que abrir una nueva terminal para que se actualice la variable `PATH`.

### 9.2. Linux

En una terminal, ejecutar:

```sh
curl -fsSL https://releases.herdr.dev/app/install.sh | sh
```

La aplicación está disponible para Linux x86-64 y ARM64. El sistema necesita una sesión gráfica y un controlador Vulkan funcional.

### 9.3. macOS

En macOS con Apple Silicon se puede instalar mediante:

```sh
curl -fsSL https://releases.herdr.dev/app/install.sh | sh
```

También está disponible mediante Homebrew:

```sh
brew install --cask herdr-app
```

La web ofrece además una imagen DMG para instalar la aplicación arrastrándola a la carpeta de aplicaciones. El repositorio indica que las compilaciones precompiladas para macOS están disponibles para Apple Silicon; en equipos Intel se puede compilar desde el código fuente.

### 9.4. Instalación del núcleo

El instalador de la aplicación configura `herdr-core` si todavía no está disponible. Por tanto, para el uso habitual de la aplicación de escritorio no es necesario instalar el núcleo por separado.

También se puede instalar `herdr-core` de forma independiente si solo se necesita el entorno de terminales o se quiere desarrollar un cliente propio. La web oficial contiene los instaladores y las instrucciones específicas.

### 9.5. Actualizaciones

Las versiones instaladas mediante los instaladores propios de Herdr comprueban si hay actualizaciones y pueden descargarlas en segundo plano. La nueva versión pasa a utilizarse al reiniciar la aplicación o al ejecutar la acción de actualización.

Las instalaciones gestionadas por Homebrew, Nix o `mise` deben actualizarse mediante el gestor de paquetes correspondiente.

## 10. Primeros pasos

Una vez instalada la aplicación, el proceso básico recomendado es:

1. **Abrir Herdr.** Se mostrará la interfaz con sus espacios, pestañas y terminales.
2. **Crear o seleccionar un espacio.** Lo habitual es utilizar un espacio por repositorio, proyecto o investigación.
3. **Abrir una pestaña o terminal.** Se puede iniciar desde el botón `+` de la barra de pestañas.
4. **Iniciar un agente o programa.** Por ejemplo, Claude Code, Codex u otra herramienta que funcione en terminal.
5. **Dar contexto al agente.** Se puede pedir que lea `~/.config/herdr-app/AGENTS.md` para conocer las posibilidades de personalización.
6. **Separar tareas.** Crear otras pestañas o paneles para pruebas, servidores, registros o agentes auxiliares.
7. **Supervisar el estado.** Utilizar la barra lateral para detectar los agentes que han terminado o necesitan una respuesta.

La propia guía de Herdr propone empezar pidiendo al agente que lea el archivo `AGENTS.md` y después solicitarle modificaciones concretas de la interfaz.

## 11. Comandos útiles de `herdr-core`

El ejecutable de línea de comandos de `herdr-core` se llama **`hc`**. Permite controlar terminales y procesos desde scripts o desde los propios agentes.

| Comando | Utilidad |
|---|---|
| `hc run cargo test` | Ejecuta un programa y muestra su salida mientras espera a que termine. |
| `hc run --bg --name web bun dev` | Inicia un proceso en segundo plano con el nombre `web`. |
| `hc ls` | Lista los terminales activos. |
| `hc attach web` | Se conecta a un terminal para interactuar con él. |
| `hc read web --lines 100` | Lee las últimas líneas de salida sin tomar el control del terminal. |
| `hc send review "Revisa también las pruebas"` | Envía texto a un terminal o agente. |
| `hc wait review` | Espera a que termine el proceso indicado. |
| `hc machine add my-ssh-host --name box` | Añade una máquina remota mediante SSH. |

### Ejemplo de coordinación

```sh
# Iniciar un agente auxiliar en segundo plano
hc run --bg --name review codex "Revisa src/x.rs. Solo lectura."

# Enviar una indicación adicional
hc send review "Presta especial atención al tratamiento de errores."

# Esperar a que termine
hc wait review

# Consultar su informe
hc read review --lines 100
```

Los nombres y direcciones de terminal de estos ejemplos son ilustrativos. En el uso real se debe utilizar el identificador que devuelva Herdr.

Para consultar la sintaxis disponible en la versión instalada:

```sh
hc --help
hc run --help
hc --skill
```

`hc --skill` muestra la guía de uso de `herdr-core` destinada a los agentes.

## 12. Privacidad y seguridad

Herdr ejecuta el trabajo en las máquinas del usuario y utiliza SSH para las conexiones remotas. Aun así, es importante distinguir entre el tráfico de los terminales, la telemetría de la aplicación y las extensiones instaladas.

### 12.1. Telemetría de escritorio

Según la política de privacidad y la documentación técnica consultadas, la telemetría de uso está **activada por defecto en las versiones de escritorio distribuidas**.

La aplicación envía un informe de uso anónimo diario asociado a un identificador aleatorio de instalación. Puede incluir versiones de la aplicación y del núcleo, sistema operativo y arquitectura, tiempos de uso agrupados, recuentos y determinados nombres de agentes, disposiciones y comandos.

La documentación afirma que estos informes **no incluyen el texto de los terminales, las instrucciones enviadas a los agentes, el contenido de los archivos ni las rutas de las carpetas**.

Se puede desactivar desde:

```text
Settings → Privacy
```

También se puede configurar `"telemetry": false` en `settings.json`.

### 12.2. Comunicación remota

La conexión desde el móvil o desde otro equipo se realiza directamente con las máquinas configuradas mediante SSH. Herdr indica que el contenido de los terminales no pasa por un servidor intermediario suyo.

La seguridad del acceso remoto depende también de la configuración SSH, las claves, los permisos y la seguridad de las máquinas conectadas.

### 12.3. Riesgos de los mods

Este es uno de los puntos más importantes que hay que tener en cuenta.

Los mods son código JavaScript de confianza que se ejecuta dentro de Herdr. Según la documentación de seguridad, pueden ejecutar programas con el entorno del usuario, leer archivos, realizar peticiones de red e incluso ejecutar programas en máquinas conectadas.

No existe una solicitud de permiso independiente para cada operación. Por tanto:

- No se deben instalar mods desconocidos sin revisar su código.
- Hay que comprobar también los mods que carga un layout descargado.
- Conviene tratar cada mod como si fuera un script de shell que se va a ejecutar con los permisos del usuario.
- No se debe asumir que los mods están aislados en un entorno seguro (*sandbox*).

### 12.4. Archivos de configuración

La carpeta de configuración contiene preferencias, claves de acceso de la interfaz, datos de mods y otros elementos locales. La documentación indica que esta carpeta no está cifrada por Herdr.

Conviene proteger el acceso al usuario del sistema y evitar guardar secretos innecesarios en archivos de configuración o extensiones de terceros.

## 13. Limitaciones y aspectos que conviene conocer

1. **No todos los agentes muestran estado.** Para aparecer correctamente clasificados en la lista, el programa debe comunicar su estado mediante OSC 7501. Sin ello, puede seguir funcionando como proceso de terminal.
2. **Cerrar la ventana no detiene los procesos, pero cerrar un panel o pestaña sí puede hacerlo.** Es importante conocer esta diferencia antes de limpiar espacios de trabajo.
3. **No hay reanudación automática general tras un reinicio.** Si se apaga el equipo o se detiene el núcleo, los paneles pueden recuperarse con shells nuevas, pero el agente o programa anterior no se relanza por sí solo.
4. **La máquina remota debe permanecer activa.** Si el servidor se apaga o `herdr-core` deja de funcionar, los procesos alojados allí no pueden seguir ejecutándose.
5. **Los mods requieren confianza.** Tienen acceso amplio al entorno del usuario y no están aislados mediante permisos por operación.
6. **La disponibilidad varía por plataforma.** La documentación consultada señala binarios Linux x86-64/ARM64, Windows x64 y macOS Apple Silicon. Para macOS Intel se plantea compilar desde el código fuente.
7. **Herdr no sustituye al agente.** Se necesita instalar y configurar aparte la herramienta de programación que se quiera ejecutar, así como sus cuentas, modelos o credenciales cuando correspondan.

## 14. Herdr frente a Herdr TUI

La web mantiene dos productos relacionados, pero diferentes. Es importante no confundir sus instaladores, comandos y mecanismos internos.

| Característica | Herdr (aplicación de escritorio) | Herdr TUI |
|---|---|---|
| Interfaz | Aplicación gráfica de escritorio. | Interfaz de terminal (TUI). |
| Orientación | Gestión visual de espacios, agentes y terminales. | Multiplexor de terminal con sesiones, pestañas y paneles. |
| Núcleo | Utiliza `herdr-core`. | Utiliza su propio servidor/runtime. |
| Aplicación móvil | Compatible mediante `herdr-core`. | No compatible con la aplicación móvil actual. |
| Configuración y comandos | Repositorio `herdr-app`; núcleo controlado con `hc`. | Documentación y CLI propias de Herdr TUI, como `herdr`. |

La aplicación actual de escritorio y Herdr TUI no comparten sus agentes en ejecución: lo iniciado en uno no aparece automáticamente en el otro. Pueden coexistir en una misma máquina, pero deben tratarse como programas separados.

Para quien llega desde la web principal y quiere una interfaz gráfica, la descarga adecuada es la de **Herdr (desktop app)** en <https://herdr.dev/download/>. La sección de Herdr TUI está en <https://herdr.dev/tui/>.

## 15. Ventajas, inconvenientes y casos recomendados

### Ventajas

- Centraliza varios terminales y agentes en una sola interfaz.
- Mantiene procesos activos aunque se cierre la ventana gráfica.
- Permite delegar tareas entre agentes y recibir sus informes.
- Integra máquinas locales y remotas mediante SSH.
- Permite personalizar la interfaz mediante layouts y mods.
- Ofrece una aplicación móvil para supervisar y responder a agentes.
- Es gratuito y el código de la aplicación y del núcleo está disponible bajo Apache 2.0.

### Inconvenientes o precauciones

- Para aprovechar la clasificación de agentes, las herramientas deben comunicar su estado mediante OSC 7501.
- La persistencia de los terminales depende de que `herdr-core` y la máquina sigan funcionando.
- La personalización avanzada puede implicar modificar archivos o ejecutar JavaScript.
- Los mods tienen permisos amplios y hay que revisar su procedencia.
- Es necesario configurar las herramientas de IA por separado.

### ¿Para quién puede resultar útil?

Herdr encaja especialmente bien con:

- Desarrolladores que utilizan varios agentes de programación a la vez.
- Personas que realizan revisiones de código y pruebas en paralelo.
- Usuarios que ejecutan trabajos largos en terminales.
- Equipos que desarrollan en servidores o máquinas virtuales por SSH.
- Usuarios que quieren supervisar agentes desde un dispositivo móvil.

Puede resultar excesivo para quien solo utiliza una terminal y un único agente de forma ocasional. Su valor aumenta cuando hay varios procesos, proyectos o máquinas que coordinar.

## 16. Recursos oficiales

- **Web principal:** <https://herdr.dev/>
- **Descarga de la aplicación de escritorio:** <https://herdr.dev/download/>
- **Guía de uso y personalización:** <https://herdr.dev/guide/>
- **Página de `herdr-core`:** <https://herdr.dev/core/>
- **Aplicación móvil:** <https://herdr.dev/mobile/>
- **Política de privacidad:** <https://herdr.dev/privacy/>
- **Repositorio de la aplicación:** <https://github.com/herdrdev/herdr-app>
- **Repositorio de `herdr-core`:** <https://github.com/herdrdev/herdr-core>
- **Herdr TUI:** <https://herdr.dev/tui/>
- **Documentación de Herdr TUI:** <https://herdr.dev/tui/docs/>

---

*Documento elaborado consultando los recursos oficiales disponibles el 17 de noviembre de 2026. Para instrucciones de instalación, comandos y detalles que dependan de la versión, debe prevalecer siempre la documentación oficial y la ayuda incluida en la instalación utilizada.*
