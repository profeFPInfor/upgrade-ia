# 50. Errores frecuentes

> [← Índice general](README.md) · Capítulo 50 de 63

La mayoría de los problemas de Markdown provienen de tres causas: **falta de líneas en blanco**, **dialecto equivocado** y **caracteres especiales sin escapar**. Esta tabla recoge errores habituales y su solución.

| Error | Problema | Solución |
|---|---|---|
| Saltos de línea incorrectos | Markdown une líneas consecutivas en un mismo párrafo | Deja una línea en blanco entre párrafos; para un salto duro, usa dos espacios al final o `\` |
| Listas mal anidadas | La sangría no coincide con el contenido del elemento padre | Indenta 2–4 espacios respecto al marcador padre y deja líneas en blanco si hay varios párrafos |
| Enlaces rotos | Ruta incorrecta, mayúsculas distintas o ancla inexistente | Comprueba la ruta, usa rutas relativas correctas y valida con un link checker |
| Código sin especificar lenguaje | No hay resaltado ni semántica de lenguaje | Añade el lenguaje tras los backticks de apertura (por ejemplo, `python`) |
| Títulos mal jerarquizados | Se saltan niveles o hay varios H1 | Usa un solo H1 y avanza de nivel en nivel |
| Imágenes sin `alt` | Los lectores de pantalla no pueden describirlas | Añade texto alternativo descriptivo o `alt=""` si es decorativa |
| `#Título` sin espacio | No se interpreta como encabezado | Escribe `# Título` |
| `##Título` sin espacio | Igual que el anterior | Escribe `## Título` |
| Énfasis con espacios | `** texto **` no se renderiza como negrita | No pongas espacios dentro de los delimitadores: `**texto**` |
| Guiones bajos en palabras | `snake_case` puede interpretarse como cursiva | Usa `` `snake_case` `` o escapa los guiones bajos |
| Asteriscos literales | Se interpretan como énfasis | Escapa con `\*` o usa un bloque de código |
| Barra vertical en tablas | Rompe las celdas | Escapa con `\|` o usa `&#124;` |
| Tabla sin fila separadora | No se reconoce como tabla | Añade `\|---\|` después del encabezado |
| Tabla sin encabezado | GFM requiere una fila de encabezado | Añade la primera fila y la separadora |
| Bloque de código sin cerrar | El resto del documento se interpreta como código | Cierra el fence con el mismo número de backticks |
| Fences anidados | El fence interior cierra el exterior | Usa más backticks en el fence exterior |
| HTML que se traga Markdown | Un bloque HTML sin línea en blanco impide procesar el Markdown interior | Deja líneas en blanco alrededor del HTML o usa un componente |
| Comentarios HTML en MDX | MDX 2+ no los admite | Usa `{/* comentario */}` |
| Llaves literales en MDX | `{` inicia una expresión | Escapa con `\{` o `&#123;` |
| `<` literal en MDX | Inicia una etiqueta JSX | Escapa con `\<` o `&lt;` |
| Etiqueta JSX sin cerrar | Error de compilación | Cierra con `/>` o `</Etiqueta>` |
| `class` en JSX | En React se usa `className` | Cambia a `className` |
| `style="..."` en JSX | React espera un objeto | Usa `style={{ color: "red" }}` |
| `import` fuera del nivel superior | Error de sintaxis ESM | Mueve los imports al principio del documento |
| Front Matter mal delimitado | No se reconoce como metadatos | Usa `---` en la primera línea y ciérralo con `---` |
| YAML inválido | Tabulaciones, dos puntos o comillas mal puestas | Usa espacios, comillas cuando sea necesario y valida el YAML |
| Front Matter no reconocido | El framework no lo procesa | Activa el plugin o usa el mecanismo del framework |
| Ancla con acentos o puntuación | El enlace no coincide con el ID generado | Copia el ancla real o define un ID explícito si la herramienta lo permite |
| Enlaces relativos en GitHub | Se resuelven respecto al archivo, no al sitio | Usa la ruta correcta y comprueba en el repositorio |
| Imágenes relativas en GitHub | Ruta incorrecta o sensible a mayúsculas | Usa rutas relativas al archivo y verifica el nombre exacto |
| Mermaid no se renderiza | La plataforma no lo soporta o falta el plugin | Comprueba el soporte y la configuración; usa una imagen si no hay soporte |
| Mermaid con sintaxis inválida | El diagrama no se genera | Valida con `mmdc` y revisa palabras reservadas |
| Palabras reservadas en Mermaid | `end`, `graph`, etc. pueden romper el diagrama | Entrecomilla las etiquetas o cambia el identificador |
| Notas al pie no soportadas | Es una extensión, no Markdown estándar | Activa la extensión o usa una lista de referencias |
| Listas de tareas no soportadas | GFM/extensión | Activa GFM o usa `- [ ]` solo en plataformas compatibles |
| Fórmulas no soportadas | Matemáticas no son estándar | Activa MathJax/KaTeX o usa una imagen |
| Emojis no soportados | Los shortcodes son una extensión | Usa el emoji Unicode o activa la extensión |
| HTML eliminado por la plataforma | Sanitización de seguridad | No dependas de HTML para contenido esencial |
| Codificación incorrecta | Acentos o emojis corruptos | Guarda en UTF-8 |
| BOM al inicio | Puede romper el Front Matter o el primer encabezado | Guarda UTF-8 sin BOM |
| CRLF inesperado | Diferencias en diffs y algunas herramientas | Normaliza a LF con `.gitattributes` o el editor |
| Línea demasiado larga | Regla de linting o mala legibilidad | Ajusta el texto o configura `MD013` |
| Encabezados duplicados | Anclas duplicadas | Renombra o usa IDs explícitos |
| Documento demasiado grande | Difícil de navegar y mantener | Divide por temas y enlaza |
| URL con espacios | El enlace se corta | Usa `<url con espacios>` o codifica `%20` |
| Paréntesis en URL | El parser cierra el enlace antes | Usa `<...>` o codifica los paréntesis |
| Autoenlaces `<...>` en MDX | MDX 2+ los interpreta como JSX | Usa `[texto](url)` |
| Ruta de Windows con `\` | Se interpreta como escape | Usa `/` o un bloque de código |
| Comillas tipográficas en código | El código no funciona | Usa comillas rectas dentro del código |
| Negrita dentro de código | El código no se interpreta | No uses Markdown dentro de fragmentos de código |
| Enlace dentro de imagen | Sintaxis incorrecta | Usa `[![alt](imagen)](url)` |
| Título con enlace | El ancla puede cambiar | Comprueba el ID generado o usa un encabezado explícito |
| Lista pegada a un párrafo | Puede interpretarse como parte del párrafo | Deja una línea en blanco antes de la lista |
| Cita sin espacio | `>cita` puede no renderizarse | Escribe `> cita` |
| Cita anidada mal indentada | Se pierde la jerarquía | Usa `>>` o una sangría coherente |
| Regla horizontal ambigua | `---` después de texto puede convertirse en Setext | Deja una línea en blanco antes |
| Setext no deseado | `---` debajo de una línea crea un H2 | Usa `***` o `___` para la regla horizontal |
| Enlaces de referencia sin definición | Se muestran como texto | Define `[id]: https://...` en el documento |
| Referencias duplicadas | La primera definición gana | Usa identificadores únicos |
| Imágenes que no cargan | Ruta, permisos o formato | Comprueba la ruta, el formato y el servidor |
| SVG con scripts | Riesgo de XSS | Sanitiza o sirve SVG como imagen, no como HTML |
| Tabla demasiado ancha | Mala legibilidad y scroll | Reduce columnas o divide la tabla |
| Anidación excesiva de listas | Difícil de leer | Reestructura con subsecciones |
| Uso de tabs | Renderizado inconsistente | Configura el editor para espacios |
| Falta de línea final | Algunos linters lo exigen | Termina con una sola línea en blanco |

## 50.1 Cómo diagnosticar un problema

1. **Aísla el fragmento**: copia el bloque en un documento mínimo.
2. **Prueba en un renderizador de referencia**: CommonMark Dingus, GFM, el sitio de destino.
3. **Revisa las líneas en blanco** alrededor del bloque.
4. **Comprueba el dialecto**: ¿es estándar, GFM, una extensión o una función de plataforma?
5. **Escapa caracteres especiales** (`*`, `_`, `[`, `]`, `<`, `>`, `|`, `{`, `}`).
6. **Valida con el linter** y lee el mensaje de la regla.
7. **Comprueba la codificación** y los saltos de línea.
8. **Elimina HTML y componentes** para ver si el problema es de sintaxis o de renderizado.

## 50.2 Errores de contenido frente a errores de sintaxis

| Tipo | Ejemplo | Enfoque |
|---|---|---|
| Sintaxis | Falta un fence, una tabla mal formada | Corregir el marcado |
| Dialecto | Una nota al pie no se renderiza | Activar extensión o cambiar de sintaxis |
| Renderizador | El HTML se ve distinto en GitHub y en el sitio | Probar en el destino real |
| Contenido | El ejemplo está desactualizado | Revisar y probar el código |
| Accesibilidad | Falta `alt` | Añadir descripción |
| Seguridad | HTML sin sanear | Sanitizar o desactivar HTML |

---

[← 49. Buenas prácticas](49-buenas-practicas.md) · [Índice general](README.md) · [51. Compatibilidad →](51-compatibilidad.md)
