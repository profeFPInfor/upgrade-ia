# 59. Recomendaciones finales

> [← Índice general](README.md) · Capítulo 59 de 63

Markdown funciona mejor cuando se trata como **contenido estructurado y versionado**, no como un formato mágico que se corrige al final. Estas recomendaciones están organizadas por perfil y por contexto.

## 59.1 Para principiantes

1. **Empieza con lo básico**: títulos, párrafos, listas, enlaces, imágenes y código.
2. **Deja líneas en blanco** entre bloques; es la causa más común de resultados inesperados.
3. **Usa un solo `#`** y baja de nivel de uno en uno.
4. **Previsualiza** mientras escribes, pero comprueba también en el destino final.
5. **No uses HTML** hasta que lo necesites de verdad.
6. **Aprende a escapar** caracteres especiales con `\`.
7. **Escribe enlaces descriptivos**, no "haz clic aquí".
8. **Añade texto alternativo** a las imágenes.
9. **Guarda en UTF-8** y usa una extensión `.md`.
10. **Practica con un documento real**: un README, una guía o un apunte.

## 59.2 Para desarrolladores

1. **README primero**: descripción, requisitos, instalación, uso, configuración, tests, licencia.
2. **Documenta el código y el proceso**, no solo la API.
3. **Usa bloques de código con lenguaje** y ejemplos ejecutables.
4. **Mantén los ejemplos sincronizados** con el código; si puedes, pruébalos en CI.
5. **Versiona la documentación** junto al código.
6. **Automatiza linting y enlaces** en CI.
7. **Usa Front Matter** solo si el generador lo necesita.
8. **Adopta SemVer y Keep a Changelog** para releases.
9. **Escribe ADR** para decisiones importantes.
10. **No incluyas secretos** en ejemplos ni capturas.

## 59.3 Para documentación técnica

1. **Aplica Diátaxis**: separa tutoriales, guías prácticas, referencia y explicación.
2. **Un propósito por documento**.
3. **Estructura consistente**: mismos títulos, mismo orden, mismos componentes.
4. **Navegación clara**: índice, enlaces anteriores/siguientes, búsqueda.
5. **Ejemplos reales y verificados**.
6. **Versionado del sitio** si la API cambia con frecuencia.
7. **Plantillas** para tipos repetidos.
8. **Glosario y convenciones** de terminología.
9. **Accesibilidad desde el inicio**.
10. **Métricas y feedback**: enlaces rotos, búsquedas sin resultados, páginas más visitadas.
11. **Revisión por pares** y fechas de actualización.
12. **Deprecación explícita** de contenido obsoleto.

## 59.4 Para GitHub

1. **Usa GFM** y comprueba la vista previa en el repositorio.
2. **Aprovecha tablas, listas de tareas y alertas** con moderación.
3. **Enlaza con rutas relativas** y verifica mayúsculas.
4. **Añade badges** solo si aportan información (CI, versión, licencia).
5. **Mantén el README actualizado** y enlaza a documentos más detallados.
6. **Incluye CONTRIBUTING.md, LICENSE y CODE_OF_CONDUCT.md** cuando corresponda.
7. **Usa plantillas de issues y pull requests**.
8. **No uses Mermaid como único formato** si el documento debe verse fuera de GitHub.
9. **Recuerda que GitHub sanea HTML**; no dependas de scripts.
10. **Revisa la renderización de `.mdx`**: GitHub no lo compila.

## 59.5 Para grandes proyectos

1. **Define una arquitectura de información**: secciones, dueños, ciclos de revisión.
2. **Docs-as-code**: repositorio, ramas, PR, revisión y CI.
3. **Guía de estilo** con terminología, tono y formato.
4. **Plantillas** para ADR, runbooks, APIs y guías.
5. **Linting y formateo** obligatorios en CI.
6. **Comprobación de enlaces** y de anclas.
7. **Versionado** y política de deprecación.
8. **Búsqueda** y navegación cuidadas.
9. **Internacionalización** si hay varios idiomas.
10. **Redirecciones** al mover páginas.
11. **Analítica y feedback** para detectar contenido que no funciona.
12. **Archivo** de documentación antigua, sin borrarla sin más.

## 59.6 Errores que evitar

- Convertir Markdown en una colección de HTML y CSS embebido.
- Duplicar contenido en varios archivos sin una fuente de verdad.
- Usar extensiones específicas sin documentarlas.
- Publicar sin probar el renderizador final.
- Ignorar la accesibilidad y la seguridad.
- Dejar enlaces rotos y ejemplos desactualizados.
- Escribir documentos enormes sin índice ni estructura.
- Confundir GitHub con el estándar.
- Presentar Mermaid como parte de Markdown.
- Usar MDX para contenido que nunca necesitará componentes.

## 59.7 Checklist final

- [ ] El documento tiene un propósito claro.
- [ ] La jerarquía de títulos es correcta.
- [ ] Los ejemplos son reales y están probados.
- [ ] Los enlaces funcionan.
- [ ] Las imágenes tienen `alt`.
- [ ] Las tablas tienen encabezado.
- [ ] El código indica lenguaje.
- [ ] No hay HTML innecesario.
- [ ] El documento se ve bien en el destino final.
- [ ] El linting y la ortografía están revisados.
- [ ] La seguridad y la accesibilidad están cubiertas.
- [ ] Hay una persona responsable y una fecha de revisión.

---

[← 58. Markdown vs otras tecnologías](58-markdown-vs-otras-tecnologias.md) · [Índice general](README.md) · [60. Bibliografía y referencias →](60-bibliografia-y-referencias.md)
