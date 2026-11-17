# 23. ADR

> [← Índice general](README.md) · Capítulo 23 de 63

Los **Architecture Decision Records (ADR)** son documentos breves que registran una decisión de arquitectura significativa: el contexto, las alternativas, la decisión y sus consecuencias. Su valor no está en la decisión, sino en el **razonamiento** que permite entenderla y revisarla cuando cambian las circunstancias.

## 23.1 Qué problema resuelven

Sin ADR, el conocimiento vive en la memoria de quien tomó la decisión, en un hilo de chat o en un comentario de código. Meses después, alguien propone cambiar algo que ya se evaluó, o defiende una opción sin conocer sus costes.

Un ADR:

- Conserva el **porqué**, no solo el qué.
- Evita repetir debates cerrados.
- Da contexto a quien llega nuevo.
- Permite revisar una decisión con criterios explícitos.
- Deja rastro de quién decidió y cuándo.

No es una especificación ni un documento de diseño: es un registro corto, con fecha y estado.

## 23.2 Cuándo escribir uno

| Situación | ¿ADR? |
|---|---|
| Elegir base de datos, lenguaje o proveedor | Sí |
| Adoptar un patrón o protocolo con impacto duradero | Sí |
| Cambiar la arquitectura de despliegue | Sí |
| Decisión difícil de revertir o costosa | Sí |
| Renombrar una variable | No |
| Corregir un error puntual | No |
| Elegir el formato de una fecha en un formulario | Normalmente no |

La prueba: si dentro de un año alguien podría preguntar «¿por qué está hecho así?» y la respuesta no cabe en un comentario de código, merece un ADR.

## 23.3 Estructura

El formato clásico de Nygard tiene cinco partes:

1. **Título:** número y decisión, en forma de frase.
2. **Estado:** propuesta, aceptada, rechazada, obsoleta o reemplazada.
3. **Contexto:** fuerzas, restricciones y problema.
4. **Decisión:** qué se decide y por qué.
5. **Consecuencias:** qué mejora, qué empeora y qué queda pendiente.

Plantillas ampliadas como **MADR** añaden opciones consideradas, criterios de decisión y pros y contras. Cuanto más compleja es la decisión, más útil es explicar las alternativas descartadas.

## 23.4 Estados y ciclo de vida

| Estado | Significado |
|---|---|
| `Proposed` | En discusión; aún no se ha aceptado |
| `Accepted` | Vigente y aplicable |
| `Rejected` | Se evaluó y se descartó |
| `Deprecated` | Sigue en el historial, pero ya no se recomienda |
| `Superseded` | Reemplazada por otro ADR |

Reglas:

- Un ADR aceptado **no se reescribe** cuando cambia la decisión. Se marca como reemplazado y se enlaza el nuevo.
- Un ADR rechazado también se conserva: evita volver a proponer lo mismo sin contexto.
- El número es estable y no se reutiliza.
- El estado se actualiza con una fecha, no se borra el historial.

## 23.5 Ejemplo completo

```markdown
# ADR-0007: Usar PostgreSQL como base de datos principal

- **Estado:** Aceptada
- **Fecha:** 2026-10-28
- **Decisores:** Equipo de plataforma
- **Reemplaza a:** ADR-0003

## Contexto

Necesitamos una base de datos relacional con transacciones ACID, consultas
JSON y un ecosistema maduro. El equipo conoce SQL y la operación actual
se basa en copias de seguridad periódicas. Las alternativas consideradas
fueron MySQL, MongoDB y SQLite.

## Decisión

Usaremos **PostgreSQL 16** como base de datos principal.

## Alternativas consideradas

| Opción | Pros | Contras |
|---|---|---|
| PostgreSQL | ACID, JSONB, extensiones | Más configuración que SQLite |
| MySQL | Muy extendido | Menos funciones avanzadas |
| MongoDB | Esquema flexible | Transacciones multi-documento más costosas en este caso |
| SQLite | Operación simple | Poco adecuado para escritura concurrente |

## Consecuencias

- Positivas: consultas potentes, ecosistema amplio, soporte de JSONB.
- Negativas: operación y copias de seguridad a cargo del equipo.
- Pendiente: definir la política de migraciones y el tamaño de las instancias.
- Reemplaza: ADR-0003.
```

Un ADR de una página suele ser suficiente. Si necesita veinte, probablemente sea un documento de diseño; el ADR puede resumirlo y enlazarlo.

## 23.6 Numeración y organización

```text
docs/adr/
├── README.md
├── 0001-elegir-base-de-datos.md
├── 0002-api-versionada.md
├── 0003-monolito-modular.md
└── 0007-usar-postgresql.md
```

- Numera de forma secuencial con cuatro dígitos.
- Usa un nombre corto y estable; el título puede cambiar.
- Mantén un índice en `README.md` con número, título, estado y fecha.
- Enlaza los ADR relacionados desde el código o la documentación de arquitectura.
- No los mezcles con guías: tienen un ciclo de vida distinto.

## 23.7 Relación con Markdown

Los ADR se guardan como archivos `.md`, se revisan en un pull request y su historial queda en Git. Markdown aporta:

- **Portabilidad:** se leen en GitHub, en el editor y en el sitio generado.
- **Diff legible:** se ve qué cambió en el contexto o en las consecuencias.
- **Enlaces:** cada decisión puede enlazar a código, issues y otros ADR.
- **Búsqueda:** un título claro y un estado permiten encontrar decisiones por tema.

El capítulo [25](25-markdown-y-git.md) explica la revisión y el historial; el [9](09-documentacion-tecnica-con-markdown.md), la relación entre arquitectura, referencia y decisiones.

## 23.8 Errores frecuentes

| Error | Consecuencia |
|---|---|
| Escribir el ADR después de implementar y sin contexto | Se convierte en justificación, no en registro |
| Omitir las alternativas | No se entiende por qué se descartaron |
| No actualizar el estado | Decisiones viejas parecen vigentes |
| Reescribir un ADR aceptado | Se pierde el historial |
| Numerar de nuevo al mover archivos | Se rompen enlaces |
| Convertirlo en un documento de diseño | Nadie lo lee |
| No enlazarlo desde el código | Se descubre por casualidad |

## 23.9 Lista de comprobación

- [ ] El ADR tiene número, título, estado y fecha.
- [ ] El contexto explica las fuerzas y restricciones, no solo el problema.
- [ ] La decisión es una frase clara y accionable.
- [ ] Las alternativas relevantes están enumeradas con pros y contras.
- [ ] Las consecuencias incluyen lo negativo y lo pendiente.
- [ ] El estado refleja la situación actual.
- [ ] Si reemplaza a otro ADR, el enlace es explícito.
- [ ] Está enlazado desde el índice y desde la documentación relacionada.
- [ ] Se revisó en un pull request como cualquier cambio de código.
- [ ] El archivo conserva su nombre y número aunque cambie el título.

---

[← 22. Changelog](22-changelog.md) · [Índice general](README.md) · [24. Front Matter →](24-front-matter.md)
