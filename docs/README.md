# Cómo se trabaja en esta documentación

Guía para documentar en **Upgrade IA**: desarrollo de software multiplataforma asistido con IA.

## Cómo está organizado

| Carpeta | Para qué |
|---------|----------|
| [`proceso/`](../proceso/) | La guía principal: una carpeta por fase del desarrollo, de la 01 (análisis) a la 09 (mantenimiento). |
| [`herramientas-ia/`](../herramientas-ia/) | Cada herramienta de IA, documentada una sola vez y enlazada desde las fases. |
| [`markdown/`](../markdown/) | Curso de Markdown, de consulta. |
| [`docs/trabajoColaborativo/`](trabajoColaborativo/) | Tutorial desde cero de Git y GitHub para trabajar en equipo. |
| [`docs/glosario.md`](glosario.md) | Glosario de los términos que usamos. |
| [`docs/temporalizacion.md`](temporalizacion.md) | Calendario de las unidades del módulo, curso 2026-27. |
| [`assets/img/`](../assets/img/) | Imágenes del repositorio. |

La regla de oro: **un tema vive en un solo sitio** y el resto lo enlaza. Si algo ya existe, enlázalo; no lo copies.

## Qué documentar y dónde

- **Una fase del proceso** (por ejemplo, el estado del arte): va en su carpeta de `proceso/`.
- **Una herramienta de IA** (por ejemplo, OpenCode): va en `herramientas-ia/<herramienta>/`. La fase que la use solo la enlaza y cuenta cómo la aplica.
- ¿No sabes dónde? Abre una **Issue** explicando qué quieres documentar y lo decidimos.

## Cómo hacer una aportación

> **¿Primera vez con Git y GitHub?** Sigue antes el [tutorial desde cero](trabajoColaborativo/README.md). Si te encuentras una palabra que no conoces, búscala en el [glosario](glosario.md).

1. **Elige un tema** y abre o localiza su Issue. El trabajo se reparte y se sigue ahí.
2. **Crea tu rama** desde `main` actualizada, con un nombre descriptivo (por ejemplo `docs/analisis-sota`).
3. **Escribe en Markdown** dentro de la carpeta que corresponde, siguiendo la plantilla de abajo.
4. **Haz commits pequeños** con mensajes en formato [Conventional Commits](https://www.conventionalcommits.org/es/) (`docs: añadir ...`).
5. **Abre un pull request** hacia `main` y enlaza la Issue. `main` está protegida: nada se sube directamente.
6. **Revisión:** el profesor puede pedirte cambios. Súbelos a la misma rama y el PR se actualiza.

### Comandos

```bash
# Solo la primera vez
git clone https://github.com/profeFPInfor/upgrade-ia.git
cd upgrade-ia

# Cada aportación
git checkout main && git pull
git checkout -b docs/nombre-de-tu-rama
# ...escribe tu material...
git add .
git commit -m "docs: añadir material sobre <tema>"
git push -u origin docs/nombre-de-tu-rama
```

Después abre el pull request desde GitHub (*New pull request*) hacia `main`.

## Estándar del README

El `README.md` de la raíz es la portada del repositorio. Se mantiene así:

- **Solo explica qué es el repo:** introducción, para quién es, cómo está planteado y qué contiene.
- **La introducción** dice que el repositorio es una colección de información, recursos y herramientas para alumnos de 2º de DAM que quieren aprender y mejorar como desarrolladores con asistencia de IA.
- **Máximo 2 diagramas Mermaid**, solo los necesarios para entender el proyecto.
- **No explica procesos** (Git, GitHub, ramas, PR, normas de estilo ni de seguridad). Eso vive en este documento y el README lo enlaza.
- **Es breve:** la tabla de contenido enlaza a cada carpeta, y el detalle va en el README de cada una.
- **Cuando cambia la estructura del repo**, se actualizan su tabla de contenido y sus diagramas.

## Plantilla de una fase del proceso

Cada `README.md` de fase tiene las mismas secciones, en este orden:

1. Qué se hace.
2. Entregables.
3. Cómo ayuda la IA (y qué hay que verificar a mano).
4. Herramientas que se usan, enlazadas a `herramientas-ia/`.
5. Aportaciones de la clase.
6. Errores frecuentes y fuentes.

Tu material va en **Aportaciones de la clase**: un fichero `.md` en la carpeta de la fase, enlazado desde esa sección con una línea que diga qué aporta.

## Reglas de estilo

- **Castellano claro**, pensado para compañeros de ciclo.
- **Títulos sin saltos** de nivel y un único `#` por documento.
- **Código con lenguaje** en los bloques (` ```bash `, ` ```json `…).
- **Diagramas en [Mermaid](https://mermaid.js.org/)**, no en imágenes.
- **Enlaces relativos** entre documentos del repo; comprueba que funcionan.
- **Fuentes primarias:** cita documentación oficial. No afirmes lo que no hayas probado.
- **Verifica lo que genera la IA:** comandos, versiones, cifras y citas se comprueban antes de documentarlos. Indica la versión con la que probaste algo.
- **Nombres de fichero** en minúsculas, con guiones y sin espacios ni datos personales.

## Qué no se sube nunca

- Claves de API, tokens, contraseñas ni ficheros `.env`.
- Datos personales de nadie.
- Material que no tengas derecho a compartir. El repo es público y con licencia [MIT](../LICENSE.md).

## Cuando hay varias aportaciones al mismo tema

No se fusionan ni se borran: se ordenan en la carpeta del tema y se enlazan desde su README, cada una con una nota de lo que aporta. Si una aportación contradice a otra, se señala la diferencia y se discute en la Issue.
