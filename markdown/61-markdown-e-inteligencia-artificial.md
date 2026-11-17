# 61. Markdown e inteligencia artificial

> [← Índice general](README.md) · Capítulo 61 de 63

Los modelos de lenguaje trabajan con texto y Markdown es texto estructurado. Esa afinidad explica por qué tantas herramientas de generación, revisión y búsqueda lo usan como formato de entrada y de salida. También explica sus límites: un modelo puede escribir Markdown impecable y, aun así, inventar un dato, citar una fuente inexistente o romper una tabla al editarla.

Este capítulo trata a la IA como una herramienta editorial más: útil para producir borradores y detectar problemas, insuficiente para decidir qué es verdad.

## 61.1 Dónde encaja la IA en un flujo Markdown

| Tarea | Uso razonable | Supervisión necesaria |
|---|---|---|
| Generar | Esquema, borrador, ejemplos, variantes de redacción | Verificar datos, ejemplos y licencias |
| Reescribir | Claridad, tono, longitud, lenguaje inclusivo | Revisar intención y terminología |
| Resumir | Notas de reunión, cambios de una versión | Comprobar que no se omite lo esencial |
| Traducir | Primera pasada de un documento | Revisión humana y glosario |
| Revisar | Estilo, enlaces, consistencia, accesibilidad | Decidir qué sugerencias se aceptan |
| Clasificar | Etiquetas, categorías, extracción de metadatos | Validar el esquema y los valores |
| Buscar | Preguntas sobre un corpus propio | Citar la fuente y comprobar el fragmento |

La regla práctica: **la IA acelera la primera versión y la revisión mecánica, no la aprobación final**. Todo lo que se publique debe tener una persona responsable identificable (véase el capítulo [62](62-gobierno-frescura-y-metricas.md)).

## 61.2 Por qué el texto plano es buen sustrato

- **Diferencias legibles.** Un cambio generado se revisa con `git diff`, no con un editor binario.
- **Estructura explícita.** Títulos, listas y tablas separan ideas que luego se pueden fragmentar.
- **Metadatos separables.** El Front Matter describe título, fecha, autor o etiquetas sin contaminar el cuerpo.
- **Portabilidad.** El mismo archivo alimenta un sitio, un PDF o un corpus de recuperación.
- **Trazabilidad.** Cada modificación queda asociada a un commit y a una revisión.

Markdown no garantiza que el contenido sea correcto, pero hace visible **qué cambió y quién lo cambió**, que es la base de cualquier control editorial.

## 61.3 Generación asistida

Un buen encargo no pide «escribe sobre X»: fija el contrato del documento. Conviene indicar:

1. **Audiencia y objetivo.** Quién lo va a leer y qué debe poder hacer después.
2. **Esquema.** Títulos previstos y extensión aproximada por sección.
3. **Fuentes.** Documentación oficial, especificaciones o textos internos que el modelo debe usar.
4. **Restricciones.** Qué no debe afirmar, qué terminología evitar y qué formato devolver.
5. **Criterio de aceptación.** Enlaces verificables, ejemplos ejecutables, tabla de compatibilidad.

```text
Redacta la sección «Instalación» de una guía para desarrolladores.
Audiencia: personas con experiencia en línea de comandos y sin conocimiento del producto.
Esquema: requisitos, instalación, verificación, errores frecuentes.
Fuentes: solo los documentos adjuntos. Si un dato no está en ellos, escribe «pendiente de verificar».
Formato: Markdown con un solo H2, bloques de código con el lenguaje y una tabla de errores.
Extensión: 350-450 palabras.
```

Dos precauciones:

- **No delegues la estructura completa.** Un esquema revisado por una persona evita secciones redundantes y detecta omisiones antes de generar texto.
- **Pide marcas de incertidumbre.** Frases como «pendiente de verificar» o «según la fuente X» son más útiles que una seguridad injustificada.

## 61.4 Revisión asistida

La IA detecta bien problemas locales: frases largas, repeticiones, enlaces con texto genérico, listas con formato inconsistente, títulos que no siguen la jerarquía. También puede proponer texto alternativo para una imagen, aunque la descripción final debe comprobarse mirando la imagen.

| Se puede automatizar | No conviene delegar |
|---|---|
| Ortografía y gramática | Decisiones de arquitectura o seguridad |
| Consistencia de estilo | Afirmaciones legales o médicas |
| Enlaces rotos y anclas | Licencias y derechos de uso |
| Texto alternativo provisional | Datos de contacto o cifras |
| Resúmenes de cambios | Aprobación final de una publicación |

Una revisión asistida debe dejar rastro: qué se cambió, con qué criterio y quién lo aceptó. Si el modelo reescribe un párrafo entero, conviene comparar el original y la propuesta antes de fusionar.

## 61.5 Documentación para agentes

Además de las personas, un repositorio puede tener lectores automáticos: asistentes que responden preguntas, agentes que ejecutan tareas o sistemas que indexan documentación. Tres convenciones aparecen con frecuencia:

- **`llms.txt`.** Propuesta de archivo Markdown en la raíz del sitio con un resumen y enlaces curados a la documentación principal, pensada para que un modelo encuentre lo esencial sin rastrear todo el sitio. Puede acompañarse de `llms-full.txt` con el texto completo. Es una convención, no un estándar: su adopción varía y no sustituye a `robots.txt` ni a un sitemap.
- **`AGENTS.md`.** Archivo con instrucciones para agentes que trabajan en el repositorio: comandos de compilación, convenciones, rutas que no deben tocarse y criterios de revisión. Es una convención emergente, no una especificación.
- **MCP (Model Context Protocol).** Protocolo abierto para que una aplicación conecte un modelo con herramientas y fuentes de datos. Un servidor MCP puede exponer recursos, herramientas y plantillas; Markdown suele ser el formato de los recursos textuales.

Ninguna de las tres reemplaza la documentación para personas. Si el contenido solo existe para un agente, sigue necesitando versión, propietario y fecha de revisión.

```markdown
# Proyecto X

> Documentación para personas y agentes.

- [Guía de inicio](docs/inicio.md): instalación y primera ejecución.
- [Referencia de la API](docs/api.md): endpoints y errores.
- [Guía de contribución](CONTRIBUTING.md): entorno, pruebas y estilo.
```

## 61.6 RAG y fragmentación

En un sistema de recuperación aumentada (RAG), el documento se divide en fragmentos, se indexa y se recupera cuando una pregunta se parece a su contenido. La estructura de Markdown influye directamente en la calidad:

- **Fragmenta por encabezados**, no por número fijo de caracteres. Una sección completa suele tener sentido por sí misma.
- **Haz que cada sección sea autónoma.** Si depende de un «como se dijo arriba», el fragmento pierde contexto al recuperarse.
- **Repite el sujeto en los títulos.** «Instalación» es peor que «Instalación en Linux» si el fragmento se muestra aislado.
- **Conserva el código y las tablas enteros.** Un bloque partido a la mitad es peor que un fragmento más largo.
- **Añade metadatos.** Ruta, título, versión, fecha y audiencia permiten filtrar antes de recuperar.
- **Evalúa.** Prepara preguntas reales con su respuesta y su fuente; mide si el fragmento recuperado contiene la respuesta.

La estructura también ayuda a citar: un encabezado estable y un ancla permiten devolver «consulta 61.6» en lugar de un texto sin procedencia.

## 61.7 Traducción automática

La traducción de Markdown tiene riesgos específicos:

- **No traducir código, rutas, identificadores ni claves de Front Matter.**
- **Mantener la sintaxis:** un asterisco de énfasis o un enlace mal cerrado rompe el render.
- **Proteger enlaces y anclas.** Si se traduce el texto visible, el destino debe seguir siendo válido.
- **Usar un glosario.** Los términos técnicos se traducen de forma distinta según el contexto.
- **Revisar la tipografía.** Comillas, guiones y espacios cambian entre idiomas.
- **Revisar con una persona que lea el idioma de destino.** Un texto fluido puede seguir siendo incorrecto.

El capítulo [45](45-internacionalizacion-y-escritura-multilingue.md) detalla la organización de traducciones y los identificadores.

## 61.8 Riesgos

| Riesgo | Ejemplo | Mitigación |
|---|---|---|
| Alucinación | Una URL o una versión que no existe | Verificar cada dato y enlace |
| Contenido obsoleto | El modelo repite una función retirada | Contrastar con la documentación vigente |
| Pérdida de matices | Un «no recomendado» se convierte en «prohibido» | Revisión humana del diff |
| Privacidad | Se envía documentación interna a un servicio externo | Acuerdo, minimización y retención |
| Licencias | Se reproduce texto protegido | Citar, resumir o pedir permiso |
| Inyección de instrucciones | Un documento recuperado contiene órdenes maliciosas | Tratar el contenido como dato, no como instrucción |
| Dependencia | Nadie sabe explicar lo que se publicó | Registro de decisiones y revisión |

La inyección de instrucciones merece atención: si un agente lee documentación de terceros, un texto puede intentar que ignore sus reglas o revele información. La defensa no es solo del modelo; también del sistema que limita permisos, separa datos de instrucciones y registra acciones.

## 61.9 Lista de comprobación

- [ ] El texto generado se contrastó con una fuente primaria.
- [ ] Los enlaces y las versiones se verificaron antes de publicar.
- [ ] Una persona revisó el diff completo, no solo el resultado final.
- [ ] No se enviaron datos confidenciales a servicios sin acuerdo.
- [ ] La licencia del contenido permite el uso previsto.
- [ ] Las instrucciones para agentes no contradicen la documentación pública.
- [ ] Los fragmentos de RAG conservan título, ruta y versión.
- [ ] La publicación tiene propietario y fecha de revisión.

---

[← 60. Bibliografía y referencias](60-bibliografia-y-referencias.md) · [Índice general](README.md) · [62. Gobierno, frescura y métricas de la documentación →](62-gobierno-frescura-y-metricas.md)
