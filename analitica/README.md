# Analítica del repositorio

Zona de **datos y automatización** de Upgrade IA: hojas de cálculo, dashboards y scripts de Python que analizan y automatizan el propio repositorio (por ejemplo, cuántos apartados hay por herramienta y en qué estado, o comprobar enlaces y generar índices).

Es un trabajo práctico de la optativa de Digitalización: cada aportación se entrega con Issue, rama y pull request, como el resto del repositorio ([cómo contribuir](../CONTRIBUTING.md)).

## Qué se puede aportar

| Tipo | Ejemplo | Carpeta |
|------|---------|---------|
| Hoja de cálculo | Cobertura de apartados por herramienta, con tablas dinámicas y gráficos | `hojas/` |
| Dashboard | Informe interactivo con filtros: estado por herramienta, PR por semana | `dashboards/` |
| Script de Python | Validar enlaces o formato, generar las tablas de índice, limpiar y analizar métricas | `scripts/` |

Cada aportación lleva **su propia subcarpeta** con un `README.md` que explica qué hace, qué datos usa y cómo se ejecuta o se abre.

## Reglas

- **Una Issue, una subcarpeta.** No toques la de otra persona.
- **Datos abiertos o sintéticos**, o datos públicos del propio repositorio. Nada de datos personales ni de empresas sin permiso por escrito.
- **Solo datos agregados.** No se publican métricas por persona (quién aporta cuánto).
- **Sin claves ni ficheros `.env`.** Si un script necesita una clave, se lee de una variable de entorno y no se sube.
- **Los scripts se revisan antes de fusionarse.** Indica en el README qué lee, qué escribe y si usa la red. Los scripts no modifican ficheros fuera de su subcarpeta.
- **Que se pueda reproducir:** otra persona debe poder ejecutarlo siguiendo tu README, con la versión de Python y las librerías indicadas.
- **Declara el uso de IA** en el README de tu aportación: herramienta, qué pediste y qué aceptaste o cambiaste.
- **Ficheros pequeños:** nada de binarios pesados ni exportaciones enormes.
- **Las comprobaciones automáticas ayudan, no te eximen:** el CI bloquea datos personales y secretos que reconoce, pero **no detecta nombres propios ni datos en texto libre**, y un pull request limpio no garantiza que no los haya. La responsabilidad es tuya ([qué comprueba y qué no](../CONTRIBUTING.md#comprobaciones-automáticas)).

## Plantilla del README de una aportación

1. Qué hace y para qué sirve.
2. Datos que usa y de dónde salen.
3. Cómo se ejecuta o se abre (versiones probadas).
4. Resultado esperado.
5. Uso de IA (declaración).
6. Limitaciones conocidas.
