# Glosario

Las palabras que usamos en este proyecto, explicadas de forma sencilla. Están agrupadas por tema y, dentro de cada tema, por orden alfabético.

> ¿Falta una palabra? Propónla en una Issue o añádela en tu pull request, con el mismo formato.

**Índice:** [Git y GitHub](#git-y-github) · [Proceso de desarrollo](#proceso-de-desarrollo-multiplataforma) · [IA y herramientas](#ia-y-herramientas) · [Documentación](#documentación)

## Git y GitHub

| Término | Qué significa |
|---|---|
| **Aprobar (approve)** | Dar el visto bueno a un pull request. Aquí solo lo hace el profesor. |
| **Clonar (clone)** | Descargar a tu ordenador una copia completa de un repositorio, con su historia. |
| **Code owner** | Persona responsable de revisar los cambios de ciertos ficheros. En este repo, el profesor. |
| **Commit** | Una "foto" de tus cambios con un mensaje que explica qué hiciste. |
| **Conflicto** | Situación en la que dos personas cambiaron las mismas líneas y Git no sabe cuál conservar. Se resuelve a mano. |
| **Conventional Commits** | Forma de escribir mensajes de commit: un tipo, dos puntos y una frase (`docs: añadir glosario`). |
| **Fork** | Copia de un repositorio ajeno en tu propia cuenta de GitHub. Aquí no se usa: trabajas con ramas del propio repo. |
| **Asignado (assignee)** | Persona que se ha encargado de una Issue o de un pull request. |
| **Etiqueta (label)** | Marca con nombre y color que clasifica una Issue o un pull request (por ejemplo `docs`). |
| **Fusionar (merge)** | Unir los cambios de una rama con otra. |
| **Git** | Programa que guarda la historia de los cambios de un proyecto. Funciona en tu ordenador. |
| **GitHub** | Web que aloja repositorios de Git y ayuda a colaborar (Issues, pull requests). |
| **HEAD** | La rama (o commit) en la que estás ahora mismo. En un conflicto, `HEAD` es **tu** versión. |
| **Issue** | Tarea o propuesta de trabajo, con su conversación. En este repo las propone el profesor. |
| **`main`** | Rama principal del repositorio: la versión buena. Está protegida y no se edita directamente. |
| **Origin** | Nombre con el que Git recuerda el repositorio de GitHub del que clonaste. |
| **Pull** | Traer a tu ordenador lo nuevo que hay en GitHub. |
| **Pull request (PR)** | Petición para unir tu rama con `main`. Es donde se revisa tu trabajo. |
| **Push** | Enviar tus commits a GitHub. |
| **Rama (branch)** | Línea de trabajo paralela. Trabajas en ella sin tocar `main`. |
| **Rama protegida** | Rama con reglas que impiden subir cambios directamente: todo entra por pull request. |
| **Remoto** | La copia del repositorio que está en GitHub (en contraste con la local, en tu ordenador). |
| **Reflog** | Registro local de los sitios donde ha estado tu `HEAD`. Sirve para recuperar commits que parecen perdidos. |
| **Repositorio** | La carpeta de un proyecto con toda su historia de cambios. |
| **Revert** | Crear un commit nuevo que deshace otro ya publicado, sin reescribir la historia. |
| **Revisión (review)** | Lectura de un pull request por otra persona, que comenta, pide cambios o aprueba. |
| **Stash** | Apartar temporalmente cambios sin terminar para dejar la carpeta limpia y recuperarlos después. |
| **Staging (preparado)** | Zona intermedia donde dejas los cambios que irán en el próximo commit (`git add`). |
| **Terminal** | Ventana donde se escriben comandos. En Windows, *Git Bash*. |
| **Token (de acceso)** | Clave que identifica tu cuenta ante GitHub cuando subes cambios. **No se comparte ni se sube nunca.** No es lo mismo que el token de un modelo de IA (ver más abajo). |

## Proceso de desarrollo multiplataforma

| Término | Qué significa |
|---|---|
| **ADR** | *Architecture Decision Record.* Documento corto que registra una decisión de arquitectura y por qué se tomó. |
| **Alcance** | Qué entra y qué no entra en el proyecto. |
| **Aplicación multiplataforma** | Aplicación que funciona en varios sistemas (por ejemplo Android, iOS, Windows, web) a partir de un código común o compartido. |
| **API** | Forma en que dos programas se comunican: define qué se puede pedir y qué se recibe. |
| **Arquitectura** | La organización general del código y sus partes. Por ejemplo, por capas: presentación, dominio y datos. |
| **Benchmark (análisis comparativo)** | Comparar alternativas con los mismos criterios para elegir con fundamento. |
| **CI/CD** | Integración y entrega continuas: automatizar las pruebas y la publicación cada vez que cambia el código. |
| **Criterio de aceptación** | Condición concreta que debe cumplirse para dar por terminada una tarea. |
| **Despliegue** | Poner la aplicación a disposición de los usuarios. |
| **Enfoque nativo** | Una aplicación escrita específicamente para una plataforma, con sus herramientas propias. |
| **Framework** | Conjunto de herramientas y reglas que facilita construir un tipo de aplicación. |
| **Go / no-go** | Decisión de seguir adelante con un proyecto o no, razonada con criterios (coste, plazo, riesgos, licencias). |
| **Historia de usuario** | Descripción breve de una necesidad desde el punto de vista de quien usa la aplicación. |
| **Licencia** | Condiciones con las que se permite usar, copiar y modificar un software o un contenido. Este repo usa MIT. |
| **MVC / MVVM** | Patrones para separar la interfaz, los datos y la lógica de una aplicación. |
| **Prueba (test)** | Comprobación de que una parte de la aplicación hace lo que debe. Pueden ser unitarias, de integración o de interfaz. |
| **PWA** | *Progressive Web App.* Web que se puede instalar y usar como una aplicación. |
| **Requisito** | Lo que la aplicación debe hacer (funcional) o cómo debe comportarse (no funcional: rendimiento, seguridad…). |
| **Riesgo** | Algo que puede salir mal, con su probabilidad y su impacto. |
| **SOTA (estado del arte)** | *State of the art.* Lo que ya existe y se sabe hoy sobre un problema: soluciones, tecnologías y sus límites. |
| **Supuesto** | Algo que damos por cierto sin haberlo comprobado. Conviene anotarlo, porque puede fallar. |
| **UML** | Lenguaje de diagramas para describir el diseño de un sistema. |
| **Viabilidad** | Si el proyecto se puede hacer en lo técnico, lo económico y lo legal. |

## IA y herramientas

| Término | Qué significa |
|---|---|
| **Agente** | Programa de IA que, además de responder, puede actuar: leer ficheros, ejecutar comandos y encadenar pasos hasta cumplir una tarea. |
| **Alucinación** | Cuando un modelo de IA inventa algo (un dato, una cita, un comando) y lo presenta como cierto. Por eso **todo se verifica**. |
| **Antigravity** | Entorno de desarrollo (IDE) con asistencia de IA, que se estudia en el tema de IDEs. *(Se ampliará en su tema.)* |
| **Contexto** | La información que el modelo tiene delante al responder: tu mensaje, los ficheros y la conversación. Es limitado. |
| **Cuota gratuita** | Límite de uso que un servicio permite sin pagar. Se agota y varía con el tiempo, así que hay que comprobarla. |
| **Harness** | Todo lo que rodea al modelo para que trabaje como agente: herramientas, reglas, memoria y el bucle que lo ejecuta. *(Se ampliará en su tema.)* |
| **IDE** | Entorno de desarrollo: el programa donde escribes, ejecutas y depuras código. |
| **LLM** | *Large Language Model.* Modelo de IA entrenado con mucho texto, capaz de escribir, resumir y generar código. |
| **MCP** | *Model Context Protocol.* Protocolo abierto para conectar a un modelo de IA con herramientas y fuentes de datos externas. |
| **OpenCode** | Agente de programación de código abierto, con interfaz de terminal, escritorio y web. Es la herramienta del taller. Ver [herramientas-ia/opencode](../herramientas-ia/opencode/). |
| **OpenRouter** | Servicio que da acceso a muchos modelos de IA con una sola cuenta, algunos gratuitos. *(Se ampliará en su tema.)* |
| **Plugin** | Extensión que añade funciones a una herramienta. |
| **Prompt** | El texto que le das a un modelo de IA para pedirle algo. Cuanto más claro y con más contexto, mejor respuesta. |
| **Proveedor** | Empresa o servicio que ofrece los modelos de IA (y su acceso). |
| **Reflection** | Técnica en la que el modelo revisa y critica su propia respuesta para mejorarla. *(Se ampliará en su tema.)* |
| **Skill** | Paquete de instrucciones reutilizables que un agente carga cuando las necesita para una tarea concreta. *(Se ampliará en su tema.)* |
| **Token (de un modelo)** | Trozo de texto (una palabra o parte de ella) que el modelo procesa. Los límites y los costes se miden en tokens. No es lo mismo que el token de acceso de GitHub. |

## Documentación

| Término | Qué significa |
|---|---|
| **README** | Fichero de presentación de un repositorio o de una carpeta: qué es y cómo orientarse. |
| **Markdown** | Lenguaje sencillo para escribir texto con formato (títulos, listas, enlaces) en ficheros `.md`. Ver el [curso de Markdown](../markdown/). |
| **Mermaid** | Forma de dibujar diagramas escribiendo texto, que GitHub muestra como imagen. |
| **Enlace relativo** | Enlace a otro fichero del repo por su ruta (`../glosario.md`), que sigue funcionando aunque el repo se mueva. |
| **Changelog** | Registro ordenado de los cambios de un proyecto entre versiones. |
| **Fuente primaria** | Origen original de una información: la documentación oficial, la norma o el autor, no un resumen de un tercero. |
