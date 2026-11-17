# 4. Sintaxis básica

> [← Índice general](README.md) · Capítulo 4 de 63

> **Convención de compatibilidad** usada a partir de aquí: 🟢 = Markdown original / CommonMark; 🟡 = extensión extendida (GFM u otros); 🔴 = depende de la plataforma.

## 4.1 Títulos

**Sintaxis:** estilo ATX (`#` a `######`) 🟢 y estilo Setext (subrayado con `=` o `-`, solo niveles 1 y 2) 🟢.

```markdown
# Título nivel 1
## Título nivel 2
### Título nivel 3
#### Título nivel 4
##### Título nivel 5
###### Título nivel 6

Título Setext 1
===============

Título Setext 2
---------------
```

**Resultado:** seis niveles de título (`<h1>`…`<h6>`).

**Observaciones:**
- CommonMark exige un **espacio** tras `#` (`#Título` no es título en CommonMark; algunos dialectos antiguos sí lo aceptaban).
- Usa un único `#` (H1) por documento y no saltes niveles (de H2 a H4).
- Deja una línea en blanco antes y después.

## 4.2 Párrafos

**Sintaxis:** uno o más renglones de texto seguidos, separados por **líneas en blanco** 🟢.

```markdown
Este es el primer párrafo.
Sigue en el mismo párrafo.

Este es el segundo párrafo.
```

**Resultado:** dos `<p>`. El salto de línea simple dentro de un párrafo **no** genera un salto visible (se trata como espacio).

**Observaciones:** no sangres párrafos con espacios; con 4 o más espacios se interpreta como bloque de código indentado.

## 4.3 Saltos de línea

| Método | Sintaxis | Compatibilidad |
|---|---|---|
| Dos espacios al final de línea | `línea··` (↵) | 🟢 |
| Barra invertida al final | `línea\` (↵) | 🟢 CommonMark |
| Etiqueta HTML | `línea<br>` | 🟢 (HTML permitido) |

```markdown
Primera línea  
Segunda línea (dos espacios al final de la anterior)

Otra primera línea\
Otra segunda línea
```

**Observaciones:** los espacios finales son invisibles y se pierden fácilmente en editores que recortan espacios; la barra invertida es más robusta. Algunas plataformas (comentarios de GitHub) convierten saltos simples en `<br>`; los archivos `.md` renderizados **no**.

## 4.4 Énfasis

```markdown
*cursiva* o _cursiva_
**negrita** o __negrita__
***negrita y cursiva*** o ___negrita y cursiva___
~~tachado~~
```

| Estilo | Resultado | Compatibilidad |
|---|---|---|
| Cursiva | *texto* | 🟢 |
| Negrita | **texto** | 🟢 |
| Negrita + cursiva | ***texto*** | 🟢 |
| Tachado | ~~texto~~ | 🟡 GFM (no está en CommonMark ni en el original) |

**Observaciones:** el guion bajo dentro de palabras (`snake_case_word`) no activa cursiva en CommonMark; el asterisco sí funciona dentro de palabras (`in*tra*palabra`).

## 4.5 Citas

```markdown
> Esto es una cita.
>
> Segundo párrafo de la cita.
>
> > Cita anidada.
```

**Resultado:** `<blockquote>`. 🟢

**Observaciones:** dentro de una cita se pueden usar otros elementos (listas, código). **Alertas de GitHub** (`> [!NOTE]`) son una extensión de GitHub, no Markdown estándar (véase [sección 10](10-github-flavored-markdown-gfm.md)).

## 4.6 Listas

### Listas no ordenadas 🟢

```markdown
- Elemento A
- Elemento B
* También con asterisco
+ O con signo más
```

### Listas ordenadas 🟢

```markdown
1. Primero
2. Segundo
3. Tercero
```

CommonMark usa el **número inicial** de la lista; los siguientes números se ignoran (`1. 1. 1.` produce 1, 2, 3). Un delimitador `)` también es válido en CommonMark (`1)`).

### Listas anidadas 🟢

```markdown
1. Fase uno
   - Tarea A
   - Tarea B
2. Fase dos
   1. Subpaso
```

**Regla práctica:** indenta el contenido anidado alineándolo con el texto del marcador del elemento padre (3 espacios tras `1. `, 2 tras `- `). Mezclar tabuladores y espacios provoca anidaciones erróneas.

### Listas de tareas 🟡 (GFM)

```markdown
- [ ] Pendiente
- [x] Hecha
```

Véase la [sección 6](06-listas-de-tareas.md).

**Elementos con varios párrafos o bloques de código:** indenta el contenido para que pertenezca al elemento:

````markdown
1. Instalar dependencias:

   ```bash
   npm install
   ```

2. Ejecutar:

   ```bash
   npm start
   ```
````

**Observaciones:**
- Una línea en blanco entre elementos crea una lista "suelta" (con `<p>` dentro de cada `<li>`).
- No mezcles marcadores distintos en la misma lista: en CommonMark, pasar de `-` a `*` inicia una lista nueva.
- La indentación incoherente es una de las causas más frecuentes de listas mal renderizadas.

## 4.7 Enlaces

```markdown
[Texto del enlace](https://example.com "Título opcional")

<https://example.com>

[Enlace de referencia][ref]
[Otro por texto][]
[ref]: https://example.com "Título"
[Otro por texto]: https://example.org

[Archivo local](./docs/instalacion.md)

[Ir a una sección](#4-sintaxis-básica)
```

| Tipo | Sintaxis | Compatibilidad |
|---|---|---|
| Normal | `[texto](url)` | 🟢 |
| Con título | `[texto](url "título")` | 🟢 |
| Autoenlace | `<https://…>` | 🟢 |
| Referencia | `[texto][id]` + definición | 🟢 |
| URL "desnuda" autolinkeada | `https://example.com` | 🟡 GFM |
| Enlace a archivo | ruta relativa | 🟢 (la resolución depende del entorno) |
| Enlace a sección | `#slug-del-título` | 🔴 los *slugs* los genera cada plataforma |

**Observaciones:** los enlaces a secciones no están definidos por Markdown; dependen de cómo el renderizador genera los identificadores ([sección 17](17-enlaces-internos.md)).

## 4.8 Imágenes

```markdown
![Texto alternativo](ruta/imagen.png "Título opcional")

![Referencia][logo]
[logo]: ./img/logo.svg

[![Imagen con enlace](img/banner.png)](https://example.com)
```

**Observaciones:** la sintaxis es la del enlace precedida de `!`. No hay forma estándar de indicar tamaño o alineación; usa HTML (`<img width="300">`) si la plataforma lo permite. Escribe siempre un **alt** descriptivo ([sección 47](47-accesibilidad.md)).

## 4.9 Código

### Código inline 🟢

```markdown
Usa el comando `git status` para ver el estado.

Para incluir un acento grave: `` `código` ``
```

### Bloques de código 🟢

Con valla (*fenced*, CommonMark) o con sangría de 4 espacios (*indented*, original):

````markdown
```python
def saludar(nombre):
    return f"Hola, {nombre}"
```

~~~bash
echo "También con virgulillas"
~~~

    # Bloque indentado (4 espacios)
    echo "indented"
````

**Lenguajes y resaltado:** el texto tras las comillas de apertura (*info string*) indica el lenguaje (`python`, `rust`, `bash`…). CommonMark **solo recomienda** usar la primera palabra como nombre de clase `language-xxx`; el **resaltado de sintaxis** lo aporta cada herramienta (GitHub, highlight.js, Prism, Shiki, Pygments…), por lo que los identificadores admitidos varían. 🔴

**Observaciones:** para mostrar un bloque que contenga ```` ``` ````, usa una valla **más larga** (cuatro o más backticks) o virgulillas.

## 4.10 Líneas horizontales

```markdown
---
***
___
```

Tres o más guiones, asteriscos o guiones bajos en una línea. 🟢 Ojo: `---` bajo un texto lo convierte en título Setext de nivel 2; deja una línea en blanco antes.

## 4.11 Escape de caracteres

Usa la barra invertida `\` para mostrar literalmente caracteres con significado:

```markdown
\*no es cursiva\*
\# no es título
1\. no es lista
\[no es enlace\]
```

Caracteres escapables en CommonMark: ``\ ` * _ { } [ ] ( ) # + - . ! | < > ~ " $ % & ' , / : ; = ? @ ^``(cualquier puntuación ASCII).

## 4.12 Caracteres especiales

- Los caracteres Unicode (acentos, `ñ`, emojis, `€`) funcionan directamente si el archivo se guarda en **UTF-8**.
- `&` y `<` se tratan de forma inteligente: `AT&T` y `4 < 5` se convierten a `&amp;` y `&lt;` automáticamente cuando no forman parte de una entidad o etiqueta.
- Emojis con *shortcodes* (`:smile:`) son una **extensión** de plataformas como GitHub 🔴.

## 4.13 Entidades HTML

```markdown
&copy; &lt;div&gt; &amp; &nbsp; &#169; &#x1F600;
```

Resultado: © <div> & (espacio no separable) © 😀. 🟢 CommonMark reconoce entidades HTML (nombradas y numéricas).

| Entidad | Resultado |
|---|---|
| `&copy;` | © |
| `&lt;` | < |
| `&gt;` | > |
| `&amp;` | & |
| `&nbsp;` | espacio de no ruptura |
| `&#169;` | © (referencia numérica) |
| `&#x1F600;` | 😀 (referencia hexadecimal) |

**Dentro de bloques de código** las entidades no se interpretan: se muestran literalmente. 🟢

## 4.14 HTML dentro de Markdown: cuándo sí y cuándo no

| Usar HTML cuando… | Evitarlo cuando… |
|---|---|
| Necesitas control de tamaño/alineación de imágenes | Existe sintaxis Markdown equivalente |
| Quieres `<details>`/`<summary>` desplegables | El documento debe renderizarse en entornos que eliminan HTML |
| Necesitas `<kbd>`, `<sub>`, `<sup>`, `<br>` | El contenido es de usuarios no confiables (véase [sección 48](48-seguridad.md)) |
| Insertas multimedia (`<video>`, `<audio>`) | Se va a convertir a PDF/DOCX donde el HTML puede perderse |

Detalle completo en la [sección 13](13-html-dentro-de-markdown.md).

---

[← 3. Cómo funciona Markdown](03-como-funciona-markdown.md) · [Índice general](README.md) · [5. Tablas →](05-tablas.md)
