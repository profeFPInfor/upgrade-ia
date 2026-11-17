# 62. Gobierno, frescura y métricas de la documentación

> [← Índice general](README.md) · Capítulo 62 de 63

Escribir documentación es la parte visible. Mantenerla viva es el trabajo que casi nunca se ve: decidir quién responde de cada página, cuándo se revisa, qué se retira y cómo se comprueba que sigue siendo útil. Sin ese gobierno, un corpus correcto se degrada en silencio: enlaces rotos, capturas desactualizadas, procedimientos que ya no funcionan y páginas que nadie se atreve a borrar.

Este capítulo propone un sistema mínimo, compatible con Markdown y con cualquier generador de sitios.

## 62.1 Qué es gobierno de la documentación

Gobierno no es burocracia: es responder de forma explícita a cinco preguntas.

1. **Quién** es responsable de cada documento.
2. **Qué** debe contener y qué no.
3. **Cuándo** se revisa y cuándo caduca.
4. **Cómo** se aprueba un cambio.
5. **Dónde** se registra lo que se decide.

En un flujo *docs-as-code*, estas respuestas viven en el repositorio: propietarios en `CODEOWNERS`, estados y fechas en el Front Matter, reglas en la guía de contribución y validaciones en CI. Lo que no está escrito en el repositorio tiende a depender de la memoria de una persona.

## 62.2 Propiedad y responsabilidades

Cada página debe tener un **propietario** identificable, no un equipo genérico sin nombre. El propietario no es necesariamente quien escribe: es quien decide si el contenido sigue siendo correcto y quién aprueba los cambios sustantivos.

GitHub permite declarar propietarios por ruta en un archivo `CODEOWNERS`, situado en la raíz, en `docs/` o en `.github/`:

```text
# Comentario: el último patrón que coincide tiene prioridad.
*                   @equipo-docs
*.md                @equipo-docs
docs/               @equipo-docs
docs/api/**         @equipo-api
docs/runbooks/**    @equipo-operaciones
```

- Los patrones siguen la sintaxis de `.gitignore`.
- **Gana el último patrón que coincide**, no el más específico.
- Los propietarios deben tener permiso de escritura en el repositorio.
- `CODEOWNERS` solicita revisión; no impide fusionar si la protección de rama no lo exige.

En el Front Matter se puede añadir el propietario visible y el estado editorial:

```yaml
---
title: "Instalación en Linux"
owner: "@equipo-docs"
status: published
reviewed: 2026-10-28
review_by: 2027-04-28
version: "2.4"
---
```

`owner`, `status` y `review_by` son convenciones del proyecto, no campos estándar. Lo importante es que el generador, el revisor y el script de validación usen los mismos nombres.

## 62.3 Ciclo de vida y estados

Un documento no pasa de «borrador» a «publicado» y se queda ahí para siempre. Un ciclo útil distingue al menos cinco estados:

| Estado | Significado | Visible para el lector |
|---|---|---|
| `draft` | En elaboración; no se enlaza desde índices | No, salvo en una vista previa |
| `review` | Listo para revisión editorial o técnica | Previsualización |
| `published` | Aprobado y mantenido | Sí |
| `deprecated` | Sigue disponible, pero tiene sustituto | Sí, con aviso |
| `archived` | Se conserva por historial; no se actualiza | Sí, con aviso y sin promesa de vigencia |

Reglas que evitan ambigüedad:

- Un documento `draft` no aparece en el sitemap ni en la navegación principal.
- Un documento `deprecated` incluye al principio el enlace al sustituto.
- Un documento `archived` no recibe correcciones menores: se marca y se conserva.
- El cambio de estado se revisa en el mismo *pull request* que el contenido.

## 62.4 Frescura y revisión programada

La **fecha de publicación** no dice si el contenido sigue siendo válido. La **fecha de última revisión** sí, siempre que la revisión sea real y no un cambio de formato.

Dos campos ayudan:

- `reviewed`: cuándo se comprobó por última vez el contenido.
- `review_by`: cuándo toca la siguiente revisión.

Los intervalos se deciden por tipo de documento, no por igual para todo. Un ejemplo de política:

| Tipo | Intervalo orientativo | Motivo |
|---|---|---|
| Referencia de API | 3-6 meses | Cambia con el producto |
| Tutorial de inicio | 6-12 meses | Depende de versiones y capturas |
| Guía conceptual | 12 meses | Cambia menos, pero envejece |
| Runbook | 3 meses o tras cada incidente | Debe funcionar bajo presión |
| ADR | Sin revisión periódica | Es un registro histórico |
| Página archivada | Ninguna | No se mantiene |

Una validación en CI puede fallar cuando `review_by` ya pasó:

```yaml
# .github/workflows/docs.yml (fragmento ilustrativo)
- name: Comprobar revisión
  run: node scripts/check-front-matter.mjs
```

El script debe leer el Front Matter, comparar `review_by` con la fecha actual y fallar solo en las páginas `published`. Si se aplica a todo el corpus de golpe, el ruido será enorme: empieza por las páginas críticas y amplía por lotes.

## 62.5 Deprecación, redirecciones y archivo

Retirar documentación es tan importante como publicarla. Un enlace roto es peor que una página antigua bien señalizada.

1. **Marca el estado.** Añade `status: deprecated` y un aviso al principio.
2. **Enlaza el sustituto.** El lector debe poder continuar en un clic.
3. **Conserva la URL si es posible.** Si cambia, responde con una redirección permanente (301).
4. **Actualiza enlaces internos.** Un verificador de enlaces debe detectar los que apuntan al documento retirado.
5. **Archiva con fecha.** Indica cuándo dejó de mantenerse y por qué.
6. **No borres sin sustituto.** Si el contenido ya no es válido y no hay reemplazo, explica qué hacer en su lugar.

En un sitio estático, las redirecciones dependen del generador o del host. Si no hay soporte de 301, una página de aviso con enlace al sustituto es mejor que un 404, pero no transmite el mismo significado a los buscadores. El capítulo [63](63-publicacion-y-distribucion.md) trata las redirecciones desde el punto de vista de la publicación.

## 62.6 Métricas que sirven para decidir

Una métrica útil tiene una pregunta asociada, una fuente y una acción prevista. Si no cambia ninguna decisión, es decorativa.

| Métrica | Pregunta | Fuente | Acción |
|---|---|---|---|
| Enlaces rotos | ¿La navegación funciona? | Verificador en CI | Corregir o redirigir |
| 404 | ¿Qué buscan y no encuentran? | Registros del servidor o analítica | Crear, redirigir o enlazar |
| Búsquedas sin resultados | ¿Falta contenido o vocabulario? | Buscador del sitio | Añadir página, sinónimos o redirección |
| Páginas sin propietario | ¿Quién responde? | Front Matter + `CODEOWNERS` | Asignar responsable |
| Revisiones vencidas | ¿Qué está caducado? | CI | Revisar, actualizar o archivar |
| Feedback útil / no útil | ¿La página resuelve la tarea? | Widget de feedback | Revisar las peores |
| Tiempo hasta la primera revisión | ¿El proceso es ágil? | Pull requests | Ajustar revisores o plantillas |
| Páginas más vistas | ¿Dónde invertir esfuerzo? | Analítica | Priorizar mejoras |

Precauciones:

- **Las visitas no miden calidad.** Una página muy visitada puede ser un problema recurrente.
- **El tiempo en página es ruidoso.** Pestañas abiertas, bots y lectura en segundo plano lo distorsionan.
- **El rebote no siempre es malo.** Puede indicar que la persona encontró lo que buscaba.
- **Compara periodos equivalentes.** Un lanzamiento o una campaña alteran la serie.
- **Segmenta.** No mezcles tráfico de bots, búsqueda interna y usuarios autenticados.

## 62.7 Analítica y privacidad

La medición también es un tratamiento de datos. Antes de instalar analítica:

- **Define la base legal y el consentimiento** cuando la normativa lo exija.
- **Minimiza:** evita cookies innecesarias, identificadores personales y datos de formularios.
- **Anonimiza o agrega** las direcciones IP cuando sea posible.
- **Documenta la retención** y elimina lo que ya no necesitas.
- **Revisa el feedback:** un campo libre puede contener datos personales; no lo publiques sin filtrar.
- **Prefiere herramientas respetuosas o autoalojadas** si el proyecto lo permite.

La analítica debe explicar el uso, no vigilar a las personas. Si no puedes justificar una métrica, no la recojas.

## 62.8 Revisión y auditoría

Además de la revisión página a página, conviene una auditoría periódica del conjunto:

1. **Muestra por riesgo.** Empieza por seguridad, instalación, API y runbooks.
2. **Comprueba enlaces y anclas.** Incluye los enlaces internos del sitio generado.
3. **Revisa propietarios y fechas.** Detecta páginas huérfanas y revisiones vencidas.
4. **Prueba los procedimientos.** Un runbook que no se ha ejecutado es una hipótesis.
5. **Lee como usuario nuevo.** Pide a alguien ajeno al equipo que siga la guía.
6. **Registra hallazgos y decisiones.** Sin registro, la auditoría se repite cada año.
7. **Cierra el ciclo.** Cada hallazgo debe tener responsable y fecha.

La auditoría no necesita cubrir el 100 % cada vez. Una muestra pequeña y repetida encuentra más problemas que una revisión total que se hace una sola vez.

## 62.9 Lista de comprobación

- [ ] Cada página publicada tiene un propietario identificable.
- [ ] `CODEOWNERS` cubre las rutas críticas y los patrones están probados.
- [ ] El Front Matter usa un conjunto estable de campos y valores.
- [ ] Las páginas `deprecated` enlazan su sustituto.
- [ ] Las páginas `archived` están señalizadas y no reciben mantenimiento.
- [ ] `review_by` se valida en CI al menos para el contenido crítico.
- [ ] Las métricas tienen pregunta, fuente y acción asociadas.
- [ ] La analítica respeta consentimiento, minimización y retención.
- [ ] Hay una auditoría periódica con muestra por riesgo.
- [ ] Los hallazgos tienen responsable y fecha de cierre.

---

[← 61. Markdown e inteligencia artificial](61-markdown-e-inteligencia-artificial.md) · [Índice general](README.md) · [63. Publicación y distribución: SEO, metadatos y feeds →](63-publicacion-y-distribucion.md)
