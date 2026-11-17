# 19. Organización de documentación

> [← Índice general](README.md) · Capítulo 19 de 63

La organización de una carpeta de documentación parece un detalle administrativo hasta que alguien necesita encontrar algo. Un árbol coherente reduce enlaces rotos, evita duplicados y hace que el sitio generado tenga URLs predecibles. Un árbol improvisado funciona mientras el proyecto es pequeño; después se convierte en un laberinto de nombres y carpetas heredadas.

Este capítulo propone criterios para organizar el contenido, no una estructura única. La forma correcta depende del producto, del equipo y de cómo se publica.

## 19.1 Principios de organización

1. **Una página, un propósito.** Si un archivo responde a dos preguntas distintas, probablemente sean dos páginas.
2. **La URL es parte del contrato.** Cambiarla rompe enlaces, marcadores y citas.
3. **La profundidad no es calidad.** Tres niveles suelen ser suficientes; cinco indican una jerarquía que nadie recorre.
4. **Los nombres describen la tarea.** `instalacion-linux.md` es mejor que `doc2.md`.
5. **El índice es una página más.** Debe mantenerse y revisarse, no generarse una vez y olvidarse.
6. **Lo que no está enlazado no existe.** Una página huérfana es invisible para las personas y para los buscadores.

## 19.2 Estructura según el tipo de proyecto

| Proyecto | Estructura habitual | Riesgo principal |
|---|---|---|
| Producto con usuarios | Tutoriales, guías, referencia, explicaciones | Mezclar audiencias |
| Biblioteca o SDK | Inicio rápido, guías, referencia de API, ejemplos | Referencia generada sin contexto |
| Monorepo | `docs/` por paquete o un `docs/` central | Duplicación entre paquetes |
| Infraestructura | Runbooks, arquitectura, ADR, postmortems | Documentación operativa desactualizada |
| Proyecto de datos | Cuadernos, metodología, diccionario de datos | Resultados no reproducibles |
| Organización | Políticas, procesos, plantillas | Documentos sin propietario |

No fuerces la misma estructura en todos los casos. Una biblioteca necesita una referencia exhaustiva; un producto, más guías de tareas. Lo que sí debería ser común es el criterio de nombres, la navegación y el ciclo de revisión.

## 19.3 Árbol de ejemplo

```text
docs/
├── README.md                 Índice general y punto de entrada
├── inicio/
│   ├── instalacion.md
│   ├── primera-ejecucion.md
│   └── actualizacion.md
├── guias/
│   ├── configuracion.md
│   ├── autenticacion.md
│   └── migracion-v1-v2.md
├── referencia/
│   ├── cli.md
│   ├── api.md
│   └── errores.md
├── explicaciones/
│   ├── arquitectura.md
│   └── modelo-de-datos.md
├── operaciones/
│   ├── runbook-ingestas.md
│   └── recuperacion.md
├── decisiones/
│   ├── 0001-usar-postgresql.md
│   └── 0002-api-versionada.md
├── releases/
│   └── 2026-10.md
└── assets/
    ├── diagramas/
    └── capturas/
```

Ventajas:

- Las carpetas reflejan **para qué** sirve el contenido, no quién lo escribió.
- `inicio/` y `guias/` separan el aprendizaje de la resolución de tareas.
- `referencia/` puede generarse o validarse contra el código.
- `operaciones/` y `decisiones/` tienen ciclos de vida distintos.
- `assets/` evita mezclar imágenes con documentos.

Si el proyecto es pequeño, no crees todas las carpetas: empieza por `README.md`, `inicio/` y `referencia/`, y añade el resto cuando aparezca la necesidad.

## 19.4 Nombres de archivos y slugs

Reglas que evitan problemas:

- **Minúsculas y guiones:** `instalacion-linux.md`, no `Instalación Linux.md`.
- **Sin espacios ni caracteres reservados:** los espacios se codifican como `%20` y complican los enlaces.
- **Slugs estables:** si el título cambia, el archivo puede conservar su nombre.
- **Sin versiones en el nombre** salvo que la versión sea parte del contrato: `api-v1.md` sí, `guia-2024.md` no.
- **Sin prefijos innecesarios:** `docs/docs-guia.md` no aporta nada.
- **Idioma coherente:** si el corpus está en español, los nombres también.

Las tildes y la `ñ` son válidas en HTML, pero en una URL se percent-encoden y se vuelven difíciles de escribir. Para la ruta pública, prefiere ASCII; para el título visible, conserva la ortografía correcta.

## 19.5 Índices, navegación y búsqueda

Una estructura clara no se explica sola. Necesita:

- **Un índice general** (`README.md`) con una frase por sección y enlaces a las páginas principales.
- **Índices locales** al inicio de cada carpeta, si tiene más de cinco páginas.
- **Navegación anterior/siguiente** en el sitio generado.
- **Migas de pan** para saber dónde estás.
- **Buscador** si el corpus supera lo que se puede recorrer a mano.

El capítulo [17](17-enlaces-internos.md) trata las anclas y los enlaces entre documentos; el [42](42-notas-al-pie-definiciones-y-referencias.md), los índices dentro del documento; el [28](28-generadores-de-sitios-estaticos.md), la navegación que genera cada herramienta.

Un índice que no se actualiza es peor que no tenerlo: promete una entrada que ya no existe. Si se genera automáticamente, verifica que excluya encabezados de bloques de código y que use las mismas anclas que el render.

## 19.6 Centralizado o junto al código

| Modelo | Ventaja | Inconveniente |
|---|---|---|
| `docs/` central | Navegación única y coherencia editorial | Se desincroniza del código |
| Junto al código | Cambia en el mismo PR que la función | Dispersión y duplicación |
| Híbrido | Referencia generada + guías centrales | Requiere disciplina y automatización |

En un monorepo, una opción habitual es mantener las guías en `docs/` y generar la referencia de cada paquete desde su código. La clave es que **el cambio de código y el de documentación se revisen juntos** (capítulo [25](25-markdown-y-git.md)).

Si el equipo es pequeño, empieza centralizado y añade documentación junto al código solo cuando un módulo necesite contexto que no encaje en la guía general.

## 19.7 Versionado y archivo

La documentación de un producto con versiones necesita una política explícita:

- **Una versión activa** en la ruta principal (`/docs/`).
- **Versiones anteriores** en rutas separadas (`/docs/v1/`), solo si siguen recibiendo soporte.
- **Una versión `latest`** que apunte a la activa, si el generador lo permite.
- **Un aviso** en las versiones antiguas con enlace a la actual.
- **Un archivo** para lo que ya no se mantiene, sin mezclarlo con la documentación vigente.

No dupliques todo el corpus para cada versión sin necesidad: multiplica el mantenimiento y las correcciones. Si una página es idéntica en dos versiones, enlaza a la común o genera la variante desde una fuente única.

El capítulo [62](62-gobierno-frescura-y-metricas.md) describe los estados `deprecated` y `archived` y las revisiones programadas.

## 19.8 Migraciones y redirecciones

Reorganizar carpetas es inevitable. Hazlo sin romper enlaces:

1. **Diseña el mapa de URLs** antiguas y nuevas antes de mover archivos.
2. **Mueve con `git mv`** para conservar el historial.
3. **Actualiza los enlaces internos** y las anclas.
4. **Añade redirecciones 301** o páginas de aviso.
5. **Comprueba enlaces externos** y busca referencias en otros repositorios.
6. **Mantén las redirecciones** al menos mientras haya tráfico o citas.

Una redirección mal hecha es un enlace roto con pasos extra. Verifica el código de estado y el destino final, no solo que la página cargue. El capítulo [63](63-publicacion-y-distribucion.md) explica las limitaciones de los sitios estáticos.

## 19.9 Señales de alarma

| Señal | Qué indica | Qué hacer |
|---|---|---|
| Carpeta `misc/`, `otros/`, `temp/` | Falta de criterio | Clasificar o eliminar |
| Varias páginas con el mismo título | Duplicación | Fusionar o diferenciar |
| Páginas sin enlaces entrantes | Contenido huérfano | Enlazar, mover o retirar |
| Nombres con fechas o nombres de persona | Organización por autor, no por tema | Renombrar por propósito |
| Más de cuatro niveles de carpetas | Jerarquía excesiva | Aplanar |
| Índice desactualizado | Mantenimiento manual sin control | Generar o revisar en CI |
| Enlaces a rutas locales | Contenido no portable | Usar rutas relativas |
| Capturas sin fecha ni versión | Imágenes caducadas | Añadir contexto o regenerar |

## 19.10 Lista de comprobación

- [ ] Cada página tiene un propósito y un público identificables.
- [ ] La estructura refleja tipos de contenido, no personas ni fechas.
- [ ] Los nombres son minúsculos, con guiones y sin espacios.
- [ ] Los slugs públicos son estables y ASCII.
- [ ] El índice general está actualizado y enlaza las páginas principales.
- [ ] No hay páginas huérfanas ni duplicadas.
- [ ] La documentación de código y la central se revisan juntas.
- [ ] Las versiones antiguas están señalizadas y enlazan la vigente.
- [ ] Las migraciones tienen redirecciones y enlaces actualizados.
- [ ] La estructura se ha probado generando el sitio, no solo en el editor.

---

[← 18. Imágenes y recursos multimedia](18-imagenes-y-recursos-multimedia.md) · [Índice general](README.md) · [20. Documentación de APIs →](20-documentacion-de-apis.md)
