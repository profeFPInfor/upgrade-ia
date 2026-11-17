# 49. Buenas prácticas

> [← Índice general](README.md) · Capítulo 49 de 63

No existe una única forma correcta de escribir Markdown, pero sí un conjunto de prácticas que mejoran la legibilidad, la portabilidad, el mantenimiento y la accesibilidad. La regla general es: **el contenido primero, la herramienta después**.

## 49.1 Estructura y organización

1. **Usa un solo H1** por documento y encabezados jerárquicos.
2. **Divide documentos largos** en archivos con un propósito claro.
3. **Mantén una estructura consistente** en todos los documentos.
4. **Incluye un índice** en documentos extensos.
5. **Usa nombres descriptivos** para archivos y carpetas (`guia-instalacion.md`, no `doc2.md`).
6. **Enlaza documentos relacionados** con rutas relativas.
7. **Mantén el README actualizado** y con enlaces a la documentación completa.
8. **Versiona la documentación** junto al código.
9. **Archiva o marca como obsoleta** la documentación que ya no aplica.

## 49.2 Escritura y estilo

10. **Escribe para el lector**: explica el qué, el porqué y el cómo.
11. **Usa ejemplos reales** y verificables.
12. **Sé conciso**, pero no omitas información necesaria.
13. **Define siglas** la primera vez que aparecen.
14. **Mantén una terminología consistente**.
15. **Revisa ortografía y gramática**.
16. **Evita dobles negaciones** y frases ambiguas.
17. **Usa voz activa** cuando sea posible.
18. **Incluye advertencias y requisitos previos** antes de los pasos peligrosos.

## 49.3 Sintaxis y formato

19. **Deja una línea en blanco** antes y después de títulos, listas, tablas, citas y bloques de código.
20. **No uses HTML innecesario**; si lo necesitas, justifícalo.
21. **Especifica el lenguaje** en los bloques de código.
22. **Usa tablas con encabezado** y columnas claras.
23. **Evita líneas excesivamente largas** si el proyecto tiene una regla de estilo.
24. **Escapa los caracteres especiales** cuando deban mostrarse literalmente.
25. **Usa listas de tareas** solo cuando aporten seguimiento real.
26. **No abuses de negritas y mayúsculas** para enfatizar.
27. **Mantén las tablas simples**; si son muy complejas, divide o usa otro formato.
28. **Usa bloques de código con fences**, no indentación, salvo que el renderizador lo requiera.

## 49.4 Enlaces, imágenes y multimedia

29. **Usa enlaces descriptivos**, no "haz clic aquí".
30. **Comprueba los enlaces** de forma automática.
31. **Usa rutas relativas** dentro del repositorio.
32. **Incluye texto alternativo** en todas las imágenes informativas.
33. **Optimiza las imágenes** y usa formatos adecuados.
34. **Evita imágenes de texto**.
35. **Añade pies de figura** cuando aporten contexto.
36. **Incluye subtítulos y transcripciones** para vídeo y audio.
37. **No enlaces a recursos que puedan desaparecer** sin indicar una alternativa.

## 49.5 Código y ejemplos

38. **Muestra código completo y ejecutable** cuando sea posible.
39. **Indica el lenguaje y la versión** si afecta al ejemplo.
40. **Evita secretos, tokens y datos personales** en los ejemplos.
41. **Marca las líneas que cambian** con comentarios, no solo con color.
42. **Explica el resultado esperado** después del ejemplo.
43. **Mantén los ejemplos sincronizados** con el código real; si es posible, genéralos o pruébalos en CI.

## 49.6 Documentación de proyectos

44. **README claro** con descripción, instalación, uso, requisitos y licencia.
45. **CONTRIBUTING.md** con el flujo de contribución.
46. **CHANGELOG.md** siguiendo Keep a Changelog y SemVer cuando aplique.
47. **LICENSE** explícita.
48. **ADR** para decisiones arquitectónicas importantes.
49. **Documentación de API** con endpoints, parámetros, errores y ejemplos.
50. **Plantillas** para issues, pull requests y documentos repetidos.
51. **Guía de estilo** para el equipo.
52. **Fecha de última revisión** o versión en documentos críticos.

## 49.7 Calidad automatizada

53. **Linting** en local y en CI.
54. **Formateo** consistente con Prettier u otra herramienta.
55. **Comprobación de enlaces**.
56. **Corrección ortográfica**.
57. **Validación de Front Matter**.
58. **Compilación de MDX y Mermaid** en CI.
59. **Previsualización** del sitio antes de publicar.
60. **Revisión por pares** de los cambios de documentación.

## 49.8 Seguridad y accesibilidad

61. **Sanitiza** el HTML si el contenido no es de confianza.
62. **No compiles MDX no confiable**.
63. **Revisa dependencias y plugins**.
64. **Aplica accesibilidad** desde el principio, no como una corrección final.
65. **Prueba con teclado y lector de pantalla**.
66. **Mantén el contraste** y no dependas solo del color.
67. **Usa lenguaje claro** y estructura predecible.

## 49.9 Checklist final

- [ ] Título y jerarquía correctos.
- [ ] Introducción y propósito claros.
- [ ] Ejemplos verificados.
- [ ] Enlaces y anclas funcionales.
- [ ] Imágenes con `alt`.
- [ ] Tablas con encabezado.
- [ ] Código con lenguaje.
- [ ] Sin HTML innecesario.
- [ ] Sin secretos ni datos personales.
- [ ] Linting y enlaces comprobados.
- [ ] Documento revisado por otra persona.
- [ ] Publicado en el formato correcto.

---

[← 48. Seguridad](48-seguridad.md) · [Índice general](README.md) · [50. Errores frecuentes →](50-errores-frecuentes.md)
