# 20. Documentación de APIs

> [← Índice general](README.md) · Capítulo 20 de 63

La documentación de una API es parte del contrato. Si un parámetro no está descrito, alguien lo adivinará; si un código de error no aparece, se interpretará como una caída. Markdown sirve para las guías y los ejemplos, pero la referencia exhaustiva se mantiene mejor con una especificación formal.

Este capítulo distingue ambos artefactos y muestra qué debe contener una referencia que permita integrar sin leer el código fuente.

## 20.1 Qué debe responder la referencia

Para cada endpoint:

- **Método HTTP y ruta**, incluida la versión.
- **Propósito**: qué hace y cuándo usarlo.
- **Autenticación y permisos** necesarios.
- **Parámetros** de ruta, consulta y cabecera, con tipo, obligatoriedad y valores admitidos.
- **Cuerpo** de la petición, con esquema y ejemplo.
- **Respuestas** correctas, con códigos y cuerpo.
- **Errores** posibles y qué hacer con cada uno.
- **Límites**: paginación, cuotas, reintentos e idempotencia.
- **Ejemplo ejecutable** (`curl`, SDK o ambos).

Una referencia que solo enumera campos obliga a prueba y error. Una guía que solo cuenta una historia no permite consultar un parámetro concreto. Lo ideal es separar **referencia** (exhaustiva, generada si es posible) y **guías** (tareas, contexto, decisiones).

## 20.2 Anatomía de una página de endpoint

| Parte | Contenido | Error frecuente |
|---|---|---|
| Título | Método y ruta | Título genérico («Crear») sin ruta |
| Resumen | Una frase de propósito | Repetir el título |
| Autenticación | Esquema y permisos | Omitir permisos por rol |
| Petición | Tabla de campos + ejemplo | Ejemplo sin campos obligatorios |
| Respuesta | Código, esquema y ejemplo | Solo el caso feliz |
| Errores | Tabla código → causa → acción | Listar códigos sin explicar |
| Límites | Paginación, cuota, reintentos | Omitirlos hasta que aparecen |

## 20.3 Autenticación y errores

La autenticación se documenta una vez, en una página común, y se enlaza desde cada endpoint. Debe indicar:

- Esquema (`Bearer`, clave de API, OAuth 2.0, mTLS).
- Dónde se envía (cabecera, consulta, cuerpo).
- Cómo se obtiene y se renueva el token.
- Qué permisos o *scopes* hacen falta para cada operación.
- Qué hacer si el token caduca o se revoca.

Para los errores, una tabla con **código HTTP**, **código interno**, **significado** y **acción recomendada** evita interpretaciones. Un `429` sin `Retry-After` documentado genera reintentos agresivos; un `409` sin explicación se confunde con un error de validación.

## 20.4 OpenAPI: el contrato

OpenAPI 3.1 describe la API en YAML o JSON: rutas, operaciones, esquemas, seguridad, ejemplos y servidores. A partir del contrato se puede generar:

- Documentación interactiva con Swagger UI o Redoc.
- Clientes y servidores en varios lenguajes.
- Pruebas de contrato y validación de respuestas.
- Verificación de que la implementación cumple lo documentado.

Ventajas: una sola fuente, cambios revisables y ejemplos validables. Riesgos: el contrato se desactualiza si no se genera desde el código o si no se valida en CI; una especificación incompleta da una falsa sensación de cobertura.

Recomendaciones:

1. Versiona el contrato junto al código.
2. Valídalo con un linter (Spectral u otro) en CI.
3. Comprueba que los ejemplos son válidos contra el esquema.
4. Publica la referencia generada y enlázala desde las guías.
5. Documenta aparte lo que el contrato no expresa bien: flujos, reintentos, límites y decisiones.

## 20.5 Ejemplo completo

````markdown
# API de Tareas v1

**Base URL:** `https://api.example.com/v1`

## Autenticación

Todas las peticiones requieren un token *Bearer* en la cabecera `Authorization`.

```http
Authorization: Bearer <TOKEN>
```

## Crear una tarea

`POST /tareas`

Crea una tarea para el usuario autenticado. La operación es idempotente si se envía
la cabecera `Idempotency-Key`.

### Cabeceras

| Cabecera | Valor | Obligatoria |
|---|---|---|
| `Authorization` | `Bearer <TOKEN>` | Sí |
| `Content-Type` | `application/json` | Sí |
| `Idempotency-Key` | UUID único por intento | No |

### Cuerpo de la petición

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `titulo` | string | Sí | Título (1-120 caracteres) |
| `descripcion` | string | No | Descripción libre |
| `vence` | string (fecha ISO 8601) | No | Fecha de vencimiento |

```json
{
  "titulo": "Escribir documentación",
  "descripcion": "Completar la guía de Markdown",
  "vence": "2026-11-15"
}
```

### Respuesta `201 Created`

```json
{
  "id": 42,
  "titulo": "Escribir documentación",
  "completada": false,
  "creada": "2026-10-28T10:00:00Z"
}
```

### Ejemplo con curl

```bash
curl -X POST https://api.example.com/v1/tareas \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: 6f1c2a9e-4b7d-4c1a-9e2f-8a3b5c7d9e01" \
  -d '{"titulo":"Escribir documentación"}'
```

### Códigos de respuesta

| Código | Significado | Acción |
|---|---|---|
| `201` | Tarea creada | Leer el `id` de la respuesta |
| `400` | JSON mal formado | Corregir el cuerpo |
| `401` | Token ausente o inválido | Renovar el token |
| `403` | Sin permiso para el recurso | Revisar el rol |
| `422` | Validación fallida | Corregir los campos indicados |
| `429` | Demasiadas peticiones | Respetar `Retry-After` |
| `500` | Error interno | Reintentar con espera y reportar |

### Formato de error

```json
{
  "error": "validacion",
  "mensaje": "El campo 'titulo' es obligatorio",
  "detalles": [{ "campo": "titulo", "motivo": "requerido" }]
}
```
````

El ejemplo muestra una decisión importante: **un solo formato de error** para toda la API. Si cada endpoint inventa su estructura, el cliente necesita un caso especial por ruta.

## 20.6 Paginación, filtros y límites

Toda lista debe documentar:

- **Paginación:** por cursor o por página; tamaño máximo y por defecto.
- **Orden:** campo y dirección admitidos.
- **Filtros:** nombres, tipos y comportamiento con valores vacíos.
- **Total:** si se devuelve y cómo se calcula.
- **Límites de uso:** cuota por ventana, cabeceras de control y política de reintentos.

Un cliente que no conoce el tamaño máximo de página pedirá 10.000 registros y recibirá un error o una respuesta truncada. Documenta también qué ocurre en el límite: ¿error, página vacía o lista parcial?

## 20.7 Versionado y cambios incompatibles

| Cambio | ¿Compatible? | Acción |
|---|---|---|
| Añadir un campo opcional a la respuesta | Sí | Documentar y anunciar |
| Añadir un parámetro opcional | Sí | Documentar |
| Añadir un valor a un enum | Depende | Avisar; el cliente puede fallar |
| Renombrar un campo | No | Nueva versión o alias temporal |
| Cambiar el tipo de un campo | No | Nueva versión |
| Eliminar un endpoint | No | Deprecación y ventana de migración |

La versión puede ir en la ruta (`/v1/`), en una cabecera o en el medio. Elige una y sé consistente. Una versión en la URL es visible y fácil de enrutar; una cabecera mantiene URLs estables, pero es más fácil de olvidar.

Documenta la **política de deprecación**: cuánto tiempo se mantiene una versión, cómo se avisa y qué se considera un cambio incompatible.

## 20.8 Probar la documentación

Una referencia no está terminada cuando se publica, sino cuando alguien la sigue sin ayuda.

1. **Ejecuta los ejemplos** con una cuenta real o un entorno de pruebas.
2. **Valida el contrato** con un linter y con pruebas de esquema.
3. **Prueba los errores**: token inválido, campo ausente, cuota superada.
4. **Revisa la paginación** con más datos de los que caben en una página.
5. **Pide a alguien ajeno** que integre una operación sencilla y anota dónde se atascó.
6. **Automatiza** la comprobación de que los ejemplos siguen siendo válidos.

El capítulo [46](46-linting-y-validacion.md) trata la validación en CI; el [9](09-documentacion-tecnica-con-markdown.md), la estructura general de la documentación técnica.

## 20.9 Lista de comprobación

- [ ] Cada endpoint indica método, ruta y propósito.
- [ ] La autenticación y los permisos están documentados y enlazados.
- [ ] Todos los parámetros tienen tipo, obligatoriedad y valores admitidos.
- [ ] Hay ejemplos de petición y de respuesta correcta.
- [ ] Los errores incluyen causa y acción recomendada.
- [ ] Se documentan paginación, filtros, cuotas y reintentos.
- [ ] El formato de error es único y consistente.
- [ ] La política de versionado y deprecación es explícita.
- [ ] El contrato OpenAPI se valida en CI, si existe.
- [ ] Los ejemplos se ejecutaron y siguen siendo válidos.

---

[← 19. Organización de documentación](19-organizacion-de-documentacion.md) · [Índice general](README.md) · [21. Documentación de proyectos de software →](21-documentacion-de-proyectos-de-software.md)
