# 27. Badges

> [← Índice general](README.md) · Capítulo 27 de 63

Los **badges** son pequeñas imágenes, normalmente SVG, que muestran el estado o los metadatos de un proyecto: compilación, cobertura, versión, licencia o plataforma. No son una función de Markdown: son **imágenes enlazadas**, y su utilidad depende de que el dato sea correcto y relevante.

Un README con diez badges desactualizados comunica menos que uno con dos que funcionan. Este capítulo explica cómo construirlos, qué significan y cuándo conviene retirarlos.

## 27.1 Qué son y qué no

Un badge es una imagen con un enlace:

```markdown
[![Texto alternativo](URL_DE_LA_IMAGEN)](URL_DE_DESTINO)
```

- La **imagen** muestra el dato.
- El **enlace** lleva a la fuente: el flujo de CI, la licencia, la versión publicada.
- El **texto alternativo** describe el dato para quien no ve la imagen.

No es un sello de calidad. Un badge de «build passing» solo indica que el último flujo terminó bien; no dice que el proyecto sea seguro, útil o mantenido.

## 27.2 Anatomía y accesibilidad

```markdown
[![CI: passing](https://github.com/usuario/repo/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/usuario/repo/actions/workflows/ci.yml)
```

| Parte | Ejemplo | Función |
|---|---|---|
| Texto alternativo | `CI: passing` | Describe el estado si la imagen no carga |
| Imagen | `.../badge.svg` | Muestra el dato |
| Destino | `.../actions/workflows/ci.yml` | Permite comprobar la fuente |

Recomendaciones:

- El texto alternativo debe incluir el **nombre del dato** y, si es dinámico, el valor esperado: «CI: passing», no «badge».
- No uses el mismo texto para todos los badges.
- Si el badge es puramente decorativo, probablemente no aporta nada; considera quitarlo.
- Comprueba el contraste y el tamaño: un SVG con texto diminuto es ilegible en móvil.

## 27.3 Shields.io

[Shields.io](https://shields.io/) genera badges estáticos y dinámicos.

### Badge estático

```text
https://img.shields.io/badge/LABEL-MESSAGE-COLOR
```

```markdown
![Licencia MIT](https://img.shields.io/badge/licencia-MIT-blue)
![Versión 2.4](https://img.shields.io/badge/versi%C3%B3n-2.4.0-green)
```

Reglas de codificación:

- `-` separa las tres partes.
- `--` representa un guion literal.
- `_` representa un espacio.
- `__` representa un guion bajo literal.
- Los caracteres especiales se codifican con percent-encoding (`%C3%B3` para `ó`).

Parámetros habituales:

| Parámetro | Ejemplo | Efecto |
|---|---|---|
| `style` | `flat`, `flat-square`, `plastic`, `for-the-badge`, `social` | Forma |
| `logo` | `github`, `rust`, `python` | Icono |
| `logoColor` | `white` | Color del icono |
| `label` | `CI` | Texto de la etiqueta |
| `color` | `blue`, `ff69b4` | Color del mensaje |

```markdown
![Estado](https://img.shields.io/badge/estado-activo-brightgreen?style=flat-square)
```

Los nombres de color y los iconos disponibles cambian; consulta la documentación de Shields antes de fijar una URL.

### Badge dinámico

Shields consulta un servicio y genera el valor actual:

```text
https://img.shields.io/github/v/release/usuario/repo
https://img.shields.io/npm/v/paquete
https://img.shields.io/github/license/usuario/repo
```

Ventaja: el dato se actualiza solo. Inconveniente: depende de la disponibilidad de Shields y del servicio consultado; si uno falla, el badge puede mostrar «unknown» o no cargar.

## 27.4 Badges de CI y servicios

GitHub genera una URL de estado para cada flujo:

```text
https://github.com/OWNER/REPO/actions/workflows/WORKFLOW.yml/badge.svg?branch=main
```

```markdown
[![CI](https://github.com/usuario/repo/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/usuario/repo/actions/workflows/ci.yml)
```

- `WORKFLOW.yml` es el nombre del archivo dentro de `.github/workflows/`.
- `?branch=main` limita el estado a esa rama; sin parámetro, se usa la rama por defecto.
- El enlace debe llevar al flujo, no a la imagen.

Otros servicios (cobertura, análisis estático, tiendas de paquetes) ofrecen badges propios. Antes de añadirlos, comprueba que el dato se actualiza y que el servicio sigue activo.

## 27.5 Buenas prácticas

- **Tres a seis badges** relevantes suelen ser suficientes. Más distraen.
- **Prioriza lo que ayuda a decidir:** versión, licencia, estado de CI, plataforma compatible.
- **Enlaza la fuente**, no solo la imagen.
- **Usa texto alternativo descriptivo.**
- **Agrupa** los badges en una línea o una tabla, no los disperses por el README.
- **Comprueba el render** en tema claro y oscuro; algunos SVG tienen fondo transparente y poco contraste.
- **Evita badges de métricas vanity** (estrellas, descargas) si no aportan a quien evalúa el proyecto.

## 27.6 Privacidad, rendimiento y disponibilidad

Cada badge es una petición a un servidor externo. Eso implica:

- **Privacidad:** el servicio recibe la IP, el agente de usuario y, según el caso, la página de referencia. GitHub suele servir imágenes externas a través de un proxy de caché, pero no es una garantía para todos los renders.
- **Rendimiento:** varias imágenes añaden DNS, TLS y peticiones; el impacto suele ser pequeño, pero no es cero.
- **Disponibilidad:** si el servicio cae, el README muestra una imagen rota o el texto alternativo.
- **Actualización:** un badge dinámico puede quedar obsoleto si el servicio deja de actualizarlo; uno estático caduca en cuanto cambia el dato.

Para proyectos con requisitos estrictos de privacidad, guarda el SVG en el repositorio y actualízalo en CI, o usa una línea de texto con el dato y un enlace a la fuente.

## 27.7 Cuándo retirarlos

Retira un badge cuando:

- El dato ya no es cierto (versión, cobertura, licencia).
- El servicio que lo genera ha desaparecido.
- Duplica información que ya está en el texto.
- Es decorativo y no ayuda a decidir.
- Genera peticiones externas sin una razón clara.

Un badge roto es una señal de abandono. Si no puedes mantenerlo, es mejor un enlace a la fuente que una imagen que miente.

## 27.8 Alternativas

| Alternativa | Ventaja | Inconveniente |
|---|---|---|
| Línea de texto | Sin peticiones externas | No se actualiza sola |
| Tabla de estado | Más contexto | Ocupa espacio |
| Enlace a la release | Siempre vigente | Menos visual |
| SVG en el repositorio | Control y privacidad | Hay que regenerarlo |
| Badge dinámico | Se actualiza solo | Depende de un servicio |

Para un README pequeño, una frase como «Versión 2.4.0 · Licencia MIT · CI en GitHub Actions» con enlaces puede ser más útil que cuatro imágenes.

## 27.9 Lista de comprobación

- [ ] Cada badge muestra un dato relevante y actual.
- [ ] La imagen enlaza a la fuente que permite verificarlo.
- [ ] El texto alternativo describe el dato, no «badge».
- [ ] La URL funciona en el render final y en tema oscuro.
- [ ] No hay badges duplicados ni decorativos.
- [ ] Se revisa la vigencia al publicar una versión.
- [ ] Se conoce el impacto de las peticiones externas.
- [ ] Los badges rotos se retiran o se sustituyen.

---

[← 26. Markdown y GitHub](26-markdown-y-github.md) · [Índice general](README.md) · [28. Generadores de sitios estáticos →](28-generadores-de-sitios-estaticos.md)
