# 22. Changelog

> [← Índice general](README.md) · Capítulo 22 de 63

Un **changelog** (`CHANGELOG.md`) es el registro legible por personas de los cambios notables de cada versión. No es el historial de commits ni las notas de una release: es el texto que alguien lee para decidir si actualiza, qué se rompe y qué gana.

Un changelog útil responde a tres preguntas: **qué cambió**, **a quién afecta** y **qué debe hacer** quien actualiza.

## 22.1 Qué incluir y qué no

Incluye:

- Funcionalidades nuevas visibles para el usuario.
- Cambios de comportamiento, aunque sean pequeños.
- Funcionalidades obsoletas y eliminadas.
- Correcciones de errores que afectaban a usuarios.
- Vulnerabilidades corregidas.
- Cambios incompatibles y pasos de migración.

No incluyas:

- Cada commit de refactorización interna.
- Cambios de formato o de CI que no afectan al usuario.
- Listados de dependencias sin impacto funcional.
- Detalles de implementación que nadie necesita para decidir.

La prueba: si una persona que usa el proyecto no necesita saberlo para trabajar, probablemente no va en el changelog.

## 22.2 Keep a Changelog

**Keep a Changelog** es una convención extendida. Principios:

- Una entrada por versión, la más reciente arriba.
- Fechas en formato ISO (`AAAA-MM-DD`).
- Sección `Unreleased` para lo que aún no se ha publicado.
- Categorías estándar y en el mismo orden.
- Enlaces a las comparaciones entre versiones.

| Categoría | Uso |
|---|---|
| `Added` | Funcionalidades nuevas |
| `Changed` | Cambios en funcionalidades existentes |
| `Deprecated` | Funcionalidades que se retirarán |
| `Removed` | Funcionalidades eliminadas |
| `Fixed` | Correcciones de errores |
| `Security` | Vulnerabilidades corregidas |

```markdown
# Changelog

Todos los cambios notables de este proyecto se documentarán en este archivo.

El formato se basa en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y este proyecto se adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [Unreleased]

### Added
- Exportación a PDF mediante plantilla.

## [1.1.0] - 2026-10-28

### Added
- Soporte para exportar a PDF.

### Fixed
- Corregido el cierre inesperado al abrir archivos vacíos.

## [1.0.0] - 2026-09-01

### Added
- Primera versión estable.

[Unreleased]: https://github.com/usuario/repo/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/usuario/repo/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/usuario/repo/releases/tag/v1.0.0
```

## 22.3 Versionado semántico

Formato `MAJOR.MINOR.PATCH` (por ejemplo `2.4.1`):

- **MAJOR**: cambios incompatibles en la API pública.
- **MINOR**: funcionalidad nueva compatible hacia atrás.
- **PATCH**: correcciones compatibles.
- **Preproducción**: `1.0.0-alpha.1`, `1.0.0-rc.1`.
- **Metadatos**: `1.0.0+build.5`.

SemVer describe la **API pública**, no el número de commits ni la importancia comercial. Si el proyecto no tiene una API estable, dilo: un `0.x` puede cambiar sin aviso, y el changelog debe reflejarlo.

| Cambio | Versión |
|---|---|
| Añadir un endpoint | MINOR |
| Corregir un cálculo incorrecto | PATCH |
| Renombrar un campo de la API | MAJOR |
| Añadir un valor a un enum | Depende: puede romper clientes; suele ser MINOR con aviso |
| Eliminar una opción de CLI | MAJOR |
| Actualizar una dependencia sin cambio visible | PATCH o ninguna entrada |

## 22.4 Cómo escribir una entrada

- **Empieza por el efecto**, no por el archivo: «La exportación a PDF conserva los enlaces» es mejor que «cambios en pdf.js».
- **Usa el infinitivo o el pretérito de forma consistente.** El corpus de este libro usa pretérito («Se añadió»), pero lo importante es no mezclar.
- **Incluye el número de issue** si aporta contexto, no como sustituto de la explicación.
- **Agrupa** cambios relacionados en una sola entrada.
- **Marca lo incompatible** con una nota y un enlace a la guía de migración.
- **No prometas fechas** que no controlas en `Unreleased`.

Mal: «Varios arreglos y mejoras».
Bien: «Corregido el error que impedía guardar tablas con celdas vacías (#128)».

## 22.5 Changelog, releases y commits

| Artefacto | Audiencia | Contenido |
|---|---|---|
| Changelog | Usuarios y contribuidores | Cambios notables por versión |
| Notas de release | Usuarios de esa versión | Resumen, enlaces y agradecimientos |
| Commits | Personas que mantienen | Cambios atómicos y su motivo |
| Historial de PR | Revisores | Discusión y decisiones |

GitHub puede generar notas de release a partir de los PR fusionados. El resultado suele ser una lista de títulos técnicos; edítala antes de publicar. Un changelog generado automáticamente sin revisión tiende a incluir ruido y a omitir el impacto.

## 22.6 Automatización

| Enfoque | Ventaja | Riesgo |
|---|---|---|
| Convención de commits + generador | Consistencia y menos trabajo manual | Lista técnica, poco útil para usuarios |
| `release-please` u similar | Actualiza changelog y versión | Requiere disciplina en los mensajes |
| Herramienta de cambios (changesets) | Entradas revisadas por PR | Más pasos para el equipo |
| Edición manual | Control editorial | Se olvida con facilidad |

Si automatizas, define qué tipos de commit aparecen y cuáles se omiten. Un changelog lleno de `chore`, `ci` y `refactor` no ayuda a decidir una actualización.

## 22.7 Errores frecuentes

| Error | Efecto |
|---|---|
| Duplicar el historial de commits | Ruido y poca legibilidad |
| Omitir los cambios incompatibles | Actualizaciones que rompen sin aviso |
| Fechas en formatos locales | Ambigüedad entre países |
| Versiones sin enlace | No se puede comparar ni descargar |
| `Unreleased` eterno | Nadie sabe qué está publicado |
| Entradas sin efecto para el usuario | El lector deja de leerlo |

## 22.8 Lista de comprobación

- [ ] Existe `CHANGELOG.md` y se actualiza en cada versión.
- [ ] La versión más reciente aparece arriba.
- [ ] Las fechas usan ISO 8601.
- [ ] Hay una sección `Unreleased` mientras se acumulan cambios.
- [ ] Las categorías son consistentes y están en el orden acordado.
- [ ] Los cambios incompatibles están marcados y explican la migración.
- [ ] Cada versión enlaza a su comparación o release.
- [ ] El changelog no es una copia del historial de commits.
- [ ] Las notas de release se editan antes de publicarlas.
- [ ] La versión del changelog coincide con la etiqueta publicada.

---

[← 21. Documentación de proyectos de software](21-documentacion-de-proyectos-de-software.md) · [Índice general](README.md) · [23. ADR →](23-adr.md)
