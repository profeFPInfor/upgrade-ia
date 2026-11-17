# 18. Imágenes y recursos multimedia

> [← Índice general](README.md) · Capítulo 18 de 63

Una imagen puede explicar en un segundo lo que un párrafo tarda en describir, pero también puede romper el diseño, añadir peso, filtrar datos o dejar fuera a quien no puede verla. Markdown solo ofrece una sintaxis mínima para imágenes; todo lo demás —tamaño, formato, texto alternativo, pie de figura, privacidad— se decide fuera del lenguaje.

## 18.1 Formatos y cuándo usar cada uno

| Formato | Uso recomendado | Ventajas | Limitaciones |
|---|---|---|---|
| PNG | Capturas, diagramas, transparencias | Sin pérdida, bordes nítidos | Peso alto en fotografías |
| JPEG | Fotografías | Compresión eficiente | Sin transparencia; artefactos |
| SVG | Diagramas, iconos, logotipos | Escalable, texto seleccionable | Sanitización; fuentes externas |
| WebP | Fotos y capturas en web | Buen equilibrio peso/calidad | Soporte variable en herramientas antiguas |
| AVIF | Web moderna | Compresión muy alta | Soporte y decodificación más lentos |
| GIF | Demos cortas | Reproducción automática | Peso desproporcionado y 256 colores |
| MP4 / WebM | Vídeo | Compresión y control | No es una imagen; requiere reproductor |

Para documentación técnica, la combinación habitual es **PNG para capturas**, **SVG para diagramas** y **JPEG/WebP para fotografías**. Un GIF de cinco segundos puede pesar más que un MP4 de treinta; si necesitas animación, valora vídeo (capítulo [38](38-exportacion-a-video.md)).

## 18.2 Sintaxis Markdown y HTML

```markdown
![Diagrama de arquitectura general](docs/img/arquitectura.png)
![Logo remoto](https://example.com/logo.png)
```

- El texto entre corchetes es el **texto alternativo**.
- La ruta puede ser relativa o absoluta.
- Markdown no permite fijar tamaño, pie de figura ni clase.

Con HTML se controlan más atributos, a costa de portabilidad:

```html
<figure>
  <img src="docs/img/arquitectura.png"
       alt="Tres servicios conectados a una cola central"
       width="800" height="450" loading="lazy">
  <figcaption>Figura 1. Arquitectura de ingestas.</figcaption>
</figure>
```

El sanitizador de cada plataforma decide qué atributos sobreviven. GitHub elimina scripts y eventos, y puede ignorar parte del HTML; un sitio propio con HTML permitido acepta más. Comprueba el render, no supongas.

## 18.3 Rutas y organización

1. Guarda los recursos en una carpeta dedicada: `docs/img/`, `assets/`, `static/`.
2. Usa rutas **relativas al archivo** que referencia (`../img/foto.png`).
3. Evita espacios, mayúsculas y caracteres reservados: `captura-login.png`, no `Captura Login (1).PNG`.
4. Incluye la imagen en el repositorio si es documentación estable.
5. Para recursos generados, documenta el script que los produce.

| Contexto | Ruta que funciona |
|---|---|
| README en la raíz | `docs/img/diagrama.png` |
| Página en `docs/guias/` | `../img/diagrama.png` |
| Sitio Jekyll con `baseurl` | `{{ '/assets/img/diagrama.png' \| relative_url }}` |
| Paquete npm o PyPI | URL absoluta a la rama o etiqueta |
| PDF generado con Pandoc | Ruta local o `--resource-path` |

En un paquete publicado, las rutas relativas del README suelen romperse porque el registro muestra el texto fuera del repositorio. Usa una URL absoluta a `raw.githubusercontent.com` o al sitio del proyecto, y comprueba que la rama o etiqueta exista.

## 18.4 Texto alternativo

El texto alternativo no es un adorno: es la imagen para quien usa un lector de pantalla y el contenido que se muestra si la imagen no carga.

| Imagen | Mal | Mejor |
|---|---|---|
| Captura de un botón | `alt="imagen"` | `alt="Botón Guardar en la esquina inferior derecha"` |
| Diagrama de flujo | `alt="diagrama"` | `alt="Flujo: solicitud, validación, cola y respuesta"` |
| Logotipo decorativo | `alt="logo"` | `alt=""` si ya hay texto al lado |
| Gráfico de ventas | `alt="gráfico"` | `alt="Ventas trimestrales: 12, 18 y 25 millones"` |

Reglas:

- **No empieces con «imagen de»** ni «foto de»: el lector ya lo anuncia.
- **Describe la función**, no cada píxel. En una captura, indica qué debe mirar la persona.
- **Sé breve** en imágenes simples; para diagramas complejos, añade una descripción larga en el texto o una tabla de datos.
- **Vacío para decorativas** (`alt=""`), nunca omitido si la imagen transmite información.
- **No dupliques el pie de figura** en el alt; el pie añade contexto, el alt describe.

El capítulo [47](47-accesibilidad.md) desarrolla los criterios WCAG aplicados a imágenes y multimedia.

## 18.5 Figuras, leyendas y diagramas

Una imagen con pie de figura se marca con `<figure>` y `<figcaption>`. En Markdown puro no existe equivalente; algunos generadores aceptan una convención propia, pero no es portable.

Para diagramas:

- **Mermaid** genera el diagrama desde texto y permite `accTitle` y `accDescr` (capítulos [14](14-mermaid.md) y [16](16-uml-y-markdown.md)).
- **SVG** conserva texto seleccionable y escala sin pérdida; incluye `<title>` y `<desc>` si lo editas a mano.
- **Capturas** deben mostrar la versión actual de la interfaz; una captura antigua es documentación incorrecta.
- **Diagramas complejos** necesitan una explicación textual equivalente, no solo un alt de una línea.

## 18.6 SVG y tema claro/oscuro

El SVG es ideal para logotipos e iconos, pero puede tener problemas:

- **Sanitización:** GitHub elimina scripts, eventos y recursos externos. Un SVG con JavaScript no funciona.
- **Fuentes:** si el SVG depende de una fuente del sistema, puede cambiar de aspecto o perder texto.
- **Colores:** un trazo oscuro desaparece en tema oscuro. Usa `currentColor` o variantes por tema.
- **Tamaño:** sin `viewBox`, el escalado es impredecible.

GitHub permite variantes por tema con fragmentos en la URL:

```markdown
![Logo](logo-claro.png#gh-light-mode-only)
![Logo](logo-oscuro.png#gh-dark-mode-only)
```

O con HTML estándar:

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="logo-oscuro.png">
  <img alt="Logo del proyecto" src="logo-claro.png" width="200">
</picture>
```

La segunda opción es más portable en sitios propios; la primera es específica de GitHub.

## 18.7 Vídeo y audio

Markdown no define vídeo ni audio. Opciones:

```html
<video src="demo.mp4" controls width="600"></video>
<audio src="entrevista.mp3" controls></audio>
```

- GitHub no reproduce siempre `<video>` desde una ruta del repositorio; en issues, PR y README permite **subir** el vídeo arrastrándolo al editor y lo aloja.
- En un sitio propio, el elemento funciona si el navegador soporta el códec y el servidor sirve el rango correcto.
- La alternativa universal es una **miniatura enlazada** a YouTube, Vimeo o el alojamiento del proyecto:

```markdown
[![Ver la demo en vídeo](docs/img/miniatura.png)](https://www.youtube.com/watch?v=ID_DEL_VIDEO)
```

- Añade subtítulos y transcripción. Un vídeo sin subtítulos excluye a quien no puede oírlo y a quien lo ve sin sonido.
- No incrustes un vídeo que se reproduzca automáticamente con sonido.

## 18.8 Rendimiento y privacidad

| Práctica | Efecto |
|---|---|
| Comprimir imágenes | Menos peso y carga más rápida |
| Indicar `width` y `height` | Evita saltos de diseño al cargar |
| Usar `loading="lazy"` | Difiere imágenes fuera de pantalla |
| Servir varios tamaños (`srcset`) | Mejor experiencia en móvil |
| Evitar GIF largos | Reduce transferencia |
| Alojar en el repositorio | Sin dependencia externa |

Cada imagen remota es una petición a otro servidor: revela la IP y el agente de usuario, y puede actuar como píxel de seguimiento. GitHub suele intermediar con un proxy de caché, pero no es una garantía universal. Para documentación con requisitos de privacidad, aloja los recursos en el propio sitio o en un CDN controlado.

## 18.9 Limitaciones por plataforma

| Plataforma | Notas |
|---|---|
| GitHub | HTML saneado; SVG sin scripts; vídeo mediante subida o URL |
| GitLab | Soporta vídeo y audio con sintaxis de imagen para ciertas extensiones |
| Sitios estáticos | Depende de la configuración de HTML y del generador |
| PDF/DOCX (Pandoc) | Imágenes estáticas; GIF no se anima; vídeo no aplica |
| EPUB | Imágenes incrustadas; comprobar tamaño y formato |
| Presentaciones | Imágenes grandes y legibles; evitar capturas diminutas |

## 18.10 Lista de comprobación

- [ ] El formato elegido es adecuado para el tipo de imagen.
- [ ] La imagen está comprimida y tiene dimensiones razonables.
- [ ] La ruta es relativa y funciona en el destino final.
- [ ] El texto alternativo describe la información, no el archivo.
- [ ] Las imágenes decorativas tienen `alt=""`.
- [ ] Los diagramas complejos tienen una explicación textual equivalente.
- [ ] El SVG no depende de scripts ni de fuentes externas.
- [ ] Se comprobó el contraste en tema claro y oscuro.
- [ ] El vídeo tiene subtítulos o transcripción.
- [ ] No hay recursos externos innecesarios que filtren datos.

---

[← 17. Enlaces internos](17-enlaces-internos.md) · [Índice general](README.md) · [19. Organización de documentación →](19-organizacion-de-documentacion.md)
