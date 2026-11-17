# 43. Cuadernos y publicación científica

> [← Índice general](README.md) · Capítulo 43 de 63

En ciencia de datos y análisis reproducible, Markdown convive con **código ejecutable**. Los cuadernos combinan texto, fórmulas, gráficos y resultados en un mismo documento. Este capítulo cubre Jupyter, MyST, Quarto y R Markdown, y las prácticas para que el resultado sea reproducible.

## 43.1 Qué es un cuaderno

Un cuaderno es una secuencia de **celdas**:

- **Markdown**: texto, títulos, listas, fórmulas y enlaces.
- **Código**: instrucciones que se ejecutan y producen salidas.
- **Resultados**: tablas, gráficos, texto e imágenes.

El orden de ejecución importa: una celda puede depender de otra ejecutada antes. Un cuaderno no es un documento estático hasta que se ejecuta y se exporta.

## 43.2 Jupyter

Jupyter almacena los cuadernos en `.ipynb`, un archivo JSON con celdas, metadatos y salidas.

```bash
# Abrir la interfaz
jupyter notebook
jupyter lab

# Ejecutar y exportar
jupyter nbconvert --to html --execute analisis.ipynb
jupyter nbconvert --to pdf --execute analisis.ipynb
jupyter nbconvert --to markdown --execute analisis.ipynb
jupyter nbconvert --to slides analisis.ipynb
```

| Opción | Efecto |
|---|---|
| `--execute` | Ejecuta el cuaderno antes de exportar |
| `--to html` | HTML autocontenido o con recursos |
| `--to pdf` | PDF (requiere LaTeX o un motor configurado) |
| `--to markdown` | Markdown con imágenes extraídas |
| `--to slides` | Presentación reveal.js |
| `--no-prompt` | Oculta los números de ejecución |
| `--ClearOutputPreprocessor.enabled=True` | Limpia las salidas |

- Jupyter: <https://jupyter.org/>
- nbconvert: <https://nbconvert.readthedocs.io/>

### 43.2.1 MyST Markdown

**MyST** amplía Markdown con *directivas* y *roles* para documentos científicos:

````markdown
```{figure} img/resultado.png
:name: fig-resultado
:alt: Gráfico de resultados

Resultados del experimento.
```

Como muestra {numref}`fig-resultado`, la tendencia es creciente.
````

MyST se usa en Jupyter Book y en el ecosistema `mystmd`:

- MyST: <https://mystmd.org/>
- Jupyter Book: <https://jupyterbook.org/>

### 43.2.2 Jupytext

Jupytext mantiene un `.ipynb` y un `.md` (o `.py`) sincronizados:

```bash
jupytext --to markdown analisis.ipynb
jupytext --sync analisis.ipynb
```

Ventaja: el Markdown se revisa en Git con diffs legibles; el cuaderno conserva las salidas para ejecutar.

- Jupytext: <https://jupytext.readthedocs.io/>

## 43.3 Quarto

Quarto es un sistema de publicación que ejecuta código y genera HTML, PDF, DOCX, presentaciones y sitios. Usa archivos `.qmd` con Front Matter YAML y bloques de código.

```yaml
---
title: "Análisis de datos"
author: "Equipo"
format:
  html:
    toc: true
    code-fold: true
  pdf:
    documentclass: article
execute:
  echo: true
  warning: false
---
```

````markdown
```{python}
import pandas as pd
datos = pd.read_csv("datos.csv")
datos.head()
```

El promedio es @fig-tendencia.
````

```bash
quarto preview
quarto render
quarto render --to pdf
quarto publish gh-pages
```

| Función | Descripción |
|---|---|
| `format` | HTML, PDF, DOCX, PPTX, reveal.js, dashboard |
| `execute` | Controla `echo`, `eval`, `warning`, `freeze` |
| `_quarto.yml` | Configuración del proyecto |
| Referencias | `@fig-`, `@tbl-`, `@eq-` |
| Citas | `--citeproc` y BibTeX integrados |
| `freeze` | Evita reejecutar código sin cambios |

- Quarto: <https://quarto.org/>

## 43.4 R Markdown

R Markdown combina Markdown con chunks de R (y otros lenguajes) y `knitr`:

````markdown
---
title: "Informe"
output:
  html_document:
    toc: true
  pdf_document: default
---

```{r setup, include=FALSE}
knitr::opts_chunk$set(echo = TRUE)
```

```{r grafico, fig.cap="Tendencia anual"}
plot(datos$anio, datos$valor)
```
````

```r
rmarkdown::render("informe.Rmd")
rmarkdown::render("informe.Rmd", output_format = "pdf_document")
```

| Opción de chunk | Efecto |
|---|---|
| `echo` | Muestra el código |
| `eval` | Ejecuta el código |
| `include` | Incluye código y resultados |
| `warning`, `message` | Muestra avisos |
| `fig.cap` | Leyenda de la figura |
| `cache` | Reutiliza resultados |

- R Markdown: <https://rmarkdown.rstudio.com/>
- knitr: <https://yihui.org/knitr/>
- bookdown: <https://bookdown.org/>

## 43.5 Reproducibilidad

Un cuaderno es reproducible si otra persona puede obtener el mismo resultado:

1. **Fija el entorno**: versiones de lenguajes y paquetes.
   - Python: `requirements.txt`, `pyproject.toml` o `conda env export`.
   - R: `renv::init()` y `renv.lock`.
   - Quarto: `freeze` y un entorno documentado.
2. **Fija las semillas** de aleatoriedad (`set.seed()`, `numpy.random.default_rng(…`).
3. **Evita rutas absolutas**; usa rutas relativas al proyecto.
4. **No dependas de datos externos cambiantes**; guarda una copia o una versión.
5. **Documenta el orden de ejecución** si no es lineal.
6. **Ejecuta de cero** antes de publicar (`Restart & Run All`, `quarto render`, `rmarkdown::render`).
7. **Registra la sesión** (`sessionInfo()`, `pip freeze`).

## 43.6 Control de versiones de cuadernos

Los `.ipynb` son JSON con salidas y metadatos; los diffs son ruidosos.

- **Limpia las salidas** antes de hacer commit, salvo que necesites conservarlas.
- Usa **Jupytext** para revisar el Markdown o el script.
- Usa **nbdime** para comparar cuadernos: <https://nbdime.readthedocs.io/>.
- No versiones datos pesados ni secretos; usa `.gitignore`.
- Revisa que las rutas y los tokens no queden en las salidas.

## 43.7 Publicación

| Destino | Cómo |
|---|---|
| **GitHub** | Renderiza `.ipynb` en el navegador |
| **nbviewer** | Vista pública de un cuaderno: <https://nbviewer.org/> |
| **GitHub Pages** | HTML generado con nbconvert, Quarto o Jupyter Book |
| **Binder** | Entorno ejecutable: <https://mybinder.org/> |
| **Colab** | Ejecución en la nube: <https://colab.research.google.com/> |
| **Quarto Pub** | `quarto publish` |
| **Revistas y repositorios** | PDF/HTML con material suplementario |

Antes de publicar, comprueba licencias de datos, imágenes y código, y elimina información personal.

## 43.8 Seguridad

- **No ejecutes cuadernos de terceros** sin revisar el código: pueden borrar archivos, exfiltrar datos o instalar paquetes.
- No incluyas tokens, contraseñas ni rutas privadas en las celdas.
- Revisa las salidas: pueden contener datos sensibles.
- Fija versiones de dependencias para evitar ataques de suministro.
- Ejecuta en un entorno aislado (contenedor, máquina virtual) si el origen no es de confianza.

## 43.9 Accesibilidad

- Los gráficos necesitan texto alternativo o una tabla de datos equivalente.
- No uses solo el color para distinguir series.
- Estructura el documento con encabezados jerárquicos.
- Las tablas deben tener cabeceras.
- Los resultados interactivos deben tener una versión estática.
- Los PDF generados deben conservar el orden de lectura.

## 43.10 Lista de comprobación

- [ ] El cuaderno se ejecuta de principio a fin sin errores.
- [ ] Las dependencias y versiones están documentadas.
- [ ] Las semillas y rutas son reproducibles.
- [ ] Las salidas no contienen secretos ni datos personales.
- [ ] El formato de publicación es el adecuado.
- [ ] Las figuras y tablas tienen alternativa textual.
- [ ] El repositorio incluye una licencia y un README.

---

[← 42. Notas al pie, definiciones y referencias](42-notas-al-pie-definiciones-y-referencias.md) · [Índice general](README.md) · [44. Bases de conocimiento personal →](44-bases-de-conocimiento-personal.md)
