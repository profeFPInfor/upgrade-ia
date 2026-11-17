# 9. Documentación técnica con Markdown

> [← Índice general](README.md) · Capítulo 9 de 63

La documentación técnica no es un conjunto de archivos: es una herramienta de trabajo. Quien la lee quiere instalar algo, resolver un error, entender una decisión o consultar un parámetro. Markdown es un buen soporte porque obliga a separar estructura y presentación, pero no decide por sí solo qué documentar, en qué orden ni con qué nivel de detalle.

Este capítulo propone una estructura común para los documentos técnicos y las reglas que hacen que sigan siendo útiles cuando el producto cambia.

## 9.1 Qué distingue la documentación técnica

Una página técnica útil cumple cuatro condiciones:

1. **Tiene un propósito único.** Se puede resumir en una frase: «instalar», «migrar», «consultar la API».
2. **Se puede seguir.** Los pasos tienen orden, requisitos y un resultado comprobable.
3. **Dice lo que no cubre.** Los límites y los casos excluidos evitan expectativas falsas.
4. **Se puede mantener.** Tiene propietario, fecha de revisión y enlaces a las fuentes.

La calidad no se mide por la cantidad de palabras, sino por el tiempo que tarda alguien en completar la tarea. Un texto breve con un ejemplo ejecutable vale más que una explicación extensa sin verificación.

## 9.2 Tipos de documentos

El marco **Diátaxis** distingue cuatro propósitos: *tutoriales* (aprender), *guías prácticas* (resolver una tarea), *referencia* (consultar) y *explicaciones* (entender). A ellos se añaden documentos operativos y de gobierno:

| Tipo | Objetivo | Audiencia | Ejemplo |
|---|---|---|---|
| Tutorial | Aprender desde cero | Personas nuevas | «Primera aplicación en 15 minutos» |
| Guía práctica | Resolver una tarea concreta | Usuarios con contexto | «Configurar HTTPS» |
| Referencia | Consultar datos exactos | Integradores, operadores | «Opciones de la CLI» |
| Explicación | Entender conceptos y decisiones | Equipo técnico | «Cómo funciona el motor de reglas» |
| Runbook | Ejecutar una operación o un incidente | Operaciones | «Reiniciar el servicio X» |
| ADR | Registrar una decisión de arquitectura | Equipo técnico | «Usar PostgreSQL en lugar de SQLite» |
| Changelog | Comunicar cambios | Todos | «Versión 2.4.0» |
| Especificación | Definir requisitos y contrato | Equipo y cliente | «API de facturación» |

Mezclar tipos en una misma página es la causa más común de documentación confusa. Un tutorial que interrumpe el paso a paso con una explicación teórica de tres párrafos pierde a quien solo quiere terminar. Si el concepto es necesario, enlaza a una página aparte.

El capítulo [20](20-documentacion-de-apis.md) desarrolla la referencia de API; el [23](23-adr.md), las decisiones de arquitectura; el [22](22-changelog.md), el historial de cambios.

## 9.3 Anatomía de una página

Una página técnica completa suele incluir:

| Parte | Pregunta que responde |
|---|---|
| Título | ¿Qué voy a hacer o consultar? |
| Resumen | ¿Para qué sirve y a quién va dirigido? |
| Requisitos | ¿Qué necesito antes de empezar? |
| Pasos | ¿Qué hago, en qué orden? |
| Verificación | ¿Cómo sé que funcionó? |
| Errores | ¿Qué hago si falla? |
| Siguientes pasos | ¿Qué puedo hacer después? |
| Referencias | ¿Dónde está la fuente oficial? |

No todas las páginas necesitan todas las partes. Una referencia de API no tiene «pasos», pero sí parámetros, ejemplos y errores. Un runbook no necesita motivación teórica, pero sí comandos exactos y criterios de aborto.

## 9.4 Plantilla base

````markdown
# Título de la tarea

Resumen en dos o tres frases: qué se consigue y para quién.

## Requisitos

- Versión mínima del producto.
- Permisos necesarios.
- Herramientas que deben estar instaladas.

## Pasos

1. Ejecuta el comando:

   ```bash
   ejemplo --opcion valor
   ```

2. Comprueba el resultado:

   ```bash
   ejemplo --version
   ```

## Verificación

Criterio observable: la salida debe contener `ok` y el código de salida debe ser 0.

## Errores frecuentes

| Error | Causa | Solución |
|---|---|---|
| `EACCES` | Permisos insuficientes | Ejecuta con el usuario correcto |
| `ECONNREFUSED` | Servicio detenido | Inicia el servicio |

## Siguientes pasos

- [Configuración avanzada](configuracion.md)
- [Referencia de la CLI](referencia.md)
````

La plantilla no es un formulario rígido. Su valor está en recordar las partes que suelen olvidarse: requisitos, verificación y errores.

## 9.5 Procedimientos y runbooks

Un runbook se escribe para ejecutarse bajo presión. Debe ser:

- **Específico:** comandos completos, rutas exactas, nombres reales.
- **Ordenado:** pasos numerados y dependencias explícitas.
- **Verificable:** después de cada paso, una señal de que salió bien.
- **Reversible:** cómo deshacer o a quién avisar si algo falla.
- **Actualizado:** probado tras cada incidente o cambio de infraestructura.

```markdown
## Reiniciar el servicio de ingestas

1. Comprueba el estado: `systemctl status ingest`.
2. Si hay trabajos en curso, espera a que la cola baje de 100 mensajes.
3. Reinicia: `sudo systemctl restart ingest`.
4. Verifica: `curl -fsS http://localhost:8080/health`.
5. Si falla, revisa `journalctl -u ingest -n 100` y escala al equipo de guardia.
```

Un runbook que no se ha ejecutado nunca es una hipótesis. Conviene probarlo en un entorno de pruebas y anotar la fecha de la última prueba.

## 9.6 Referencia, arquitectura y decisiones

La **referencia** describe datos, no procesos: parámetros, tipos, valores por defecto, errores y ejemplos. Debe ser exhaustiva y fácil de consultar; las tablas y los bloques de código son sus herramientas naturales.

La **arquitectura** explica componentes, límites y flujos. Un diagrama Mermaid (capítulos [14](14-mermaid.md) y [16](16-uml-y-markdown.md)) suele comunicar más que varios párrafos, siempre que tenga una leyenda y un texto alternativo.

Las **decisiones** se registran en ADR: contexto, opciones, decisión y consecuencias. Un ADR no se reescribe cuando la decisión cambia; se marca como reemplazado y se enlaza el nuevo. Así se conserva el razonamiento histórico.

## 9.7 Documentación de API

Una referencia de API debe permitir integrar sin leer el código fuente:

- Autenticación y permisos.
- URL base y versionado.
- Endpoints, métodos y parámetros.
- Cuerpo de solicitud y respuesta, con ejemplos reales.
- Códigos de error y qué hacer con cada uno.
- Límites de uso, paginación y reintentos.
- OpenAPI si el proyecto lo mantiene.

OpenAPI 3.1 permite describir la API en YAML o JSON y generar documentación interactiva con Swagger UI o Redoc. El contrato debe versionarse junto al código y validarse en CI; una especificación desactualizada es peor que no tenerla, porque genera confianza falsa.

## 9.8 Propiedad, revisión y frescura

Una página sin propietario envejece sin que nadie lo note. Como mínimo:

- Un responsable identificable en el Front Matter o en `CODEOWNERS`.
- Una fecha de última revisión real.
- Un estado editorial (`draft`, `published`, `deprecated`, `archived`).
- Un criterio para retirar o reemplazar la página.

El capítulo [62](62-gobierno-frescura-y-metricas.md) desarrolla el ciclo de vida completo, las revisiones programadas y las métricas.

## 9.9 Estilo, accesibilidad y validación

- **Voz activa y frases cortas.** «Ejecuta el comando» es mejor que «el comando debe ser ejecutado».
- **Segunda persona o impersonal, pero constante.** No mezcles registros en la misma página.
- **Términos definidos una vez.** Si un concepto aparece en varios capítulos, enlaza al glosario ([56](56-glosario.md)).
- **Texto alternativo en imágenes y diagramas.** No describas «imagen»; describe lo que muestra.
- **Tablas con encabezados claros.** No uses tablas para maquetar.
- **Enlaces descriptivos.** El texto del enlace debe tener sentido fuera de contexto.

La validación automatizada ayuda, pero no sustituye la lectura:

| Comprobación | Herramienta habitual |
|---|---|
| Estructura y estilo de Markdown | markdownlint |
| Prosa y terminología | Vale, cspell |
| Enlaces y anclas | lychee, markdown-link-check |
| Accesibilidad | pa11y, Lighthouse, revisión manual |
| Render final | Prueba en el generador y en el navegador |

El capítulo [46](46-linting-y-validacion.md) explica cómo integrar estas comprobaciones en CI.

## 9.10 Lista de comprobación

- [ ] La página tiene un propósito único y un público identificado.
- [ ] Los requisitos y el resultado esperado están explícitos.
- [ ] Los pasos se pueden seguir en orden y tienen verificación.
- [ ] Los errores frecuentes incluyen causa y solución.
- [ ] Los ejemplos son ejecutables o están marcados como ilustrativos.
- [ ] La página tiene propietario y fecha de revisión.
- [ ] Los enlaces internos y externos funcionan.
- [ ] Las imágenes y diagramas tienen texto alternativo.
- [ ] La página se ha probado en el render final, no solo en el editor.
- [ ] Está enlazada desde el índice o desde una página relacionada.

---

[← 8. README.md](08-readme-md.md) · [Índice general](README.md) · [10. GitHub Flavored Markdown (GFM) →](10-github-flavored-markdown-gfm.md)
