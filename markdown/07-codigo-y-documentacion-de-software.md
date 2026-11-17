# 7. Código y documentación de software

> [← Índice general](README.md) · Capítulo 7 de 63

## 7.1 Principios

- Usa **siempre** bloque con valla y **especifica el lenguaje**.
- Separa **comandos** (lo que escribe el usuario) de **salida** (lo que imprime el sistema).
- Muestra ejemplos **mínimos, ejecutables y probados**.
- No incluyas prompts (`$`) si el usuario va a copiar el bloque; si los incluyes, hazlo de forma consistente.
- Indica versión de lenguaje/herramienta cuando importe.
- Resalta los **valores a sustituir** con una convención clara (`<TU_TOKEN>`, `USUARIO`).
- Mantén líneas razonablemente cortas para evitar el desplazamiento horizontal.
- Indica el **nombre del archivo** en una línea anterior (`**config.yaml**`) cuando sea relevante.
- Comenta lo no evidente, no lo obvio.
- Nunca incluyas secretos reales (tokens, contraseñas): usa valores de ejemplo.

## 7.2 Ejemplos por lenguaje

**Terminal / Bash**

```bash
git clone https://github.com/usuario/proyecto.git
cd proyecto
./gradlew build
```

**PowerShell**

```powershell
Get-ChildItem -Path . -Filter *.md | Select-Object Name, Length
```

**JSON** (no admite comentarios; usa `jsonc` si los necesitas)

```json
{
  "nombre": "demo",
  "version": "1.0.0",
  "scripts": { "build": "tsc" }
}
```

**YAML**

```yaml
servidor:
  puerto: 8080
  tls: false
```

**XML**

```xml
<configuracion>
  <modo>produccion</modo>
</configuracion>
```

**Java**

```java
public class Hola {
    public static void main(String[] args) {
        System.out.println("Hola, Markdown!");
    }
}
```

**JavaScript**

```javascript
const saludar = (nombre) => `Hola, ${nombre}`;
console.log(saludar("Markdown"));
```

**Python**

```python
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

print(saludar("Markdown"))
```

**SQL**

```sql
SELECT id, nombre
FROM usuarios
WHERE activo = TRUE
ORDER BY nombre;
```

**Salida de un comando** (usa `text` o `console`)

```text
BUILD SUCCESSFUL in 3s
```

## 7.3 Resaltado de sintaxis

El identificador tras la valla (`python`, `rust`, `diff`, `json`…) es interpretado por el motor de resaltado, no por Markdown. Las listas de lenguajes soportados varían (en GitHub se usa la lista de *Linguist*). Útil: `diff` para mostrar cambios.

```diff
- let x = 1;
+ let x = 2;
```

Identificadores habituales (los reconocidos dependen de la herramienta; en GitHub, consulta la lista de lenguajes de [Linguist](https://github.com/github-linguist/linguist)):

| Lenguaje | Identificadores comunes |
|---|---|
| Bash / shell | `bash`, `sh`, `shell` |
| PowerShell | `powershell`, `ps1` |
| JSON | `json`, `jsonc` |
| YAML | `yaml`, `yml` |
| XML | `xml` |
| SQL | `sql` |
| Java | `java` |
| JavaScript | `javascript`, `js` |
| TypeScript | `typescript`, `ts` |
| Python | `python`, `py` |
| Rust | `rust`, `rs` |
| Salida de consola sin resaltado | `text`, `console` |
| Diferencias (diff) | `diff` |

## 7.4 Rust

### 7.4.1 Mostrar código Rust

Usa un bloque con el identificador `rust`:

````markdown
```rust
fn main() {
    println!("Hola, Markdown!");
}
```
````

Resultado:

```rust
fn main() {
    println!("Hola, Markdown!");
}
```

Ejemplo algo más completo:

```rust
#[derive(Debug)]
struct Punto {
    x: f64,
    y: f64,
}

impl Punto {
    fn distancia_al_origen(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

fn main() {
    let p = Punto { x: 3.0, y: 4.0 };
    println!("{:?} -> {}", p, p.distancia_al_origen());
}
```

### 7.4.2 README de proyectos Rust

Un README de un *crate* suele incluir: nombre, descripción, badges (crates.io, docs.rs, CI), instalación con `cargo add`, ejemplo mínimo, características (*features*), MSRV (versión mínima de Rust), licencia. En `Cargo.toml` el campo `readme = "README.md"` indica el archivo que se muestra en crates.io.

````markdown
# mi_crate

[![Crates.io](https://img.shields.io/crates/v/mi_crate)](https://crates.io/crates/mi_crate)
[![Docs.rs](https://img.shields.io/docsrs/mi_crate)](https://docs.rs/mi_crate)

Una biblioteca Rust para hacer X.

## Instalación

```bash
cargo add mi_crate
```

## Uso

```rust
use mi_crate::sumar;

fn main() {
    assert_eq!(sumar(2, 3), 5);
}
```
````

### 7.4.3 Rustdoc y Markdown

**Rustdoc** es la herramienta oficial que genera documentación HTML a partir de comentarios de documentación del código fuente Rust. Esos comentarios se escriben en **Markdown** (Rustdoc usa un procesador compatible con CommonMark, `pulldown-cmark`, con algunas extensiones activadas). 

> **Importante:** las funciones concretas disponibles (tablas, notas al pie, tachado, listas de tareas, enlaces intradoc, atributos de bloques de código como `ignore`, `no_run`, `should_panic`) **dependen de Rustdoc** y no forman parte del Markdown estándar.

| Comentario | Documenta |
|---|---|
| `///` | El **elemento siguiente** (función, struct, enum, trait, campo, variante…) |
| `//!` | El **elemento contenedor** (módulo o *crate*; típico al inicio de `lib.rs`) |
| `/** … */` y `/*! … */` | Equivalentes en bloque (menos habituales) |
| `#[doc = "..."]` y `#![doc = ...]` | Forma programática; permite `#![doc = include_str!("../README.md")]` |

Ejemplo de documentación de API:

````rust
//! # mi_crate
//!
//! Biblioteca de utilidades matemáticas.
//!
//! Consulta [`Figura`] y [`area`] para empezar.

/// Una figura geométrica.
///
/// # Ejemplos
///
/// ```
/// use mi_crate::Figura;
/// let f = Figura::Cuadrado(2.0);
/// assert_eq!(mi_crate::area(&f), 4.0);
/// ```
pub enum Figura {
    /// Cuadrado con la longitud de su lado.
    Cuadrado(f64),
    /// Círculo con su radio.
    Circulo(f64),
}

/// Calcula el área de una [`Figura`].
///
/// # Panics
///
/// No entra en pánico.
///
/// # Errores
///
/// Esta función no devuelve errores.
pub fn area(f: &Figura) -> f64 {
    match f {
        Figura::Cuadrado(l) => l * l,
        Figura::Circulo(r) => std::f64::consts::PI * r * r,
    }
}
````

Puntos clave:

- Los bloques de código en la documentación **se compilan y ejecutan como *doctests*** con `cargo test` (`cargo test --doc` ejecuta solo esos ejemplos).
- Secciones convencionales: `# Examples`, `# Panics`, `# Errors`, `# Safety`.
- Se documentan módulos, funciones, *structs*, *enums*, *traits*, *crates*, constantes y campos.

### 7.4.4 Atributos de bloque y ejemplos verificables

Rustdoc reconoce atributos en el *info string* de los bloques de código. **Son propios de Rustdoc**, no de Markdown:

| Atributo | Efecto |
|---|---|
| `no_run` | Se compila pero no se ejecuta |
| `ignore` | No se compila ni se ejecuta |
| `should_panic` | El ejemplo debe entrar en pánico para pasar |
| `compile_fail` | El ejemplo debe fallar al compilar |
| `edition2018`, `edition2021` | Fija la edición del ejemplo |
| (sin atributo) | Se compila y ejecuta como test |

````rust
/// ```no_run
/// // Se compila pero no se ejecuta
/// std::fs::remove_file("datos.tmp").unwrap();
/// ```
///
/// ```ignore
/// // No se compila ni se ejecuta
/// codigo_pseudocodigo();
/// ```
///
/// ```should_panic
/// panic!("esto debe fallar");
/// ```
///
/// ```compile_fail
/// let x: i32 = "texto";
/// ```
///
/// ```
/// # // Las líneas que empiezan con `# ` se ocultan en la documentación
/// # fn preparar() {}
/// preparar();
/// ```
fn ejemplo_atributos() {}
````

La línea que empieza por `# ` (con espacio) se oculta en la documentación generada, pero se compila: sirve para preparar el contexto del ejemplo sin mostrarlo.

### 7.4.5 Structs, enums, traits y módulos

```rust
//! # Mi crate
//!
//! `mi_crate` ofrece utilidades para gestionar **usuarios**.
//!
//! ## Inicio rápido
//!
//! ```
//! use mi_crate::Usuario;
//! let u = Usuario::nuevo("Ana");
//! assert_eq!(u.nombre(), "Ana");
//! ```

/// Representa a un usuario del sistema.
///
/// Se crea con [`Usuario::nuevo`].
#[derive(Debug, Clone)]
pub struct Usuario {
    /// Nombre visible del usuario.
    nombre: String,
}

impl Usuario {
    /// Crea un usuario nuevo.
    pub fn nuevo(nombre: &str) -> Self {
        Self { nombre: nombre.to_string() }
    }

    /// Devuelve el nombre.
    pub fn nombre(&self) -> &str {
        &self.nombre
    }
}

/// Niveles de permiso.
pub enum Rol {
    /// Acceso completo.
    Admin,
    /// Solo lectura.
    Lector,
}

/// Comportamiento común de los elementos exportables.
pub trait Exportable {
    /// Exporta el elemento a formato JSON.
    ///
    /// # Errors
    ///
    /// Devuelve un error si la serialización falla.
    fn a_json(&self) -> Result<String, std::fmt::Error>;
}
```

### 7.4.6 Enlaces entre elementos y documentación de crates

Rustdoc permite **enlaces intra-documentación** escribiendo la ruta del elemento entre corchetes; se resuelven al generar la documentación y avisan si el destino no existe:

```rust
/// Ver también [`Usuario`], [`crate::Rol`] y [`Vec`].
/// Método relacionado: [`Usuario::nombre`].
pub fn relacionado() {}
```

- `cargo doc --open` genera la documentación local y la abre en el navegador.
- Al publicar en **crates.io**, la documentación se compila y aloja en [docs.rs](https://docs.rs/).
- La portada del crate se escribe con `//!` al inicio de `src/lib.rs`; para reutilizar el README: `#![doc = include_str!("../README.md")]`.
- Enlaces oficiales: [Linking to items by name](https://doc.rust-lang.org/rustdoc/write-documentation/linking-to-items-by-name.html) y [The rustdoc book](https://doc.rust-lang.org/rustdoc/).

### 7.4.7 Ejemplo de API documentada

```rust
//! Cliente mínimo para una API de tareas.

use std::fmt;

/// Error devuelto por el cliente.
#[derive(Debug)]
pub enum ErrorApi {
    /// La red no está disponible.
    Red,
    /// El servidor respondió con un código HTTP distinto de 2xx.
    Http(u16),
}

impl fmt::Display for ErrorApi {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ErrorApi::Red => write!(f, "error de red"),
            ErrorApi::Http(c) => write!(f, "HTTP {c}"),
        }
    }
}

/// Cliente de la API.
///
/// # Ejemplos
///
/// ```no_run
/// # use api_tareas::Cliente;
/// let cliente = Cliente::nuevo("https://api.example.com");
/// let tareas = cliente.listar()?;
/// # Ok::<(), api_tareas::ErrorApi>(())
/// ```
pub struct Cliente {
    base: String,
}

impl Cliente {
    /// Crea un cliente apuntando a `base`.
    pub fn nuevo(base: &str) -> Self {
        Self { base: base.to_string() }
    }

    /// Lista las tareas.
    ///
    /// # Errors
    ///
    /// Devuelve [`ErrorApi::Red`] si no hay conexión o
    /// [`ErrorApi::Http`] si el servidor rechaza la petición.
    pub fn listar(&self) -> Result<Vec<String>, ErrorApi> {
        let _ = &self.base;
        Ok(vec![])
    }
}
```

### 7.4.8 Buenas prácticas para documentar Rust

1. Documenta todo elemento `pub` (activa `#![warn(missing_docs)]`).
2. Primera línea: resumen corto en una frase.
3. Incluye siempre un ejemplo ejecutable (*doctest*).
4. Usa `# Panics`, `# Errors` y `# Safety` cuando proceda.
5. Enlaza con *intra-doc links* en lugar de URLs.
6. Mantén README y documentación del crate sincronizados; si usas `include_str!`, el README es la única fuente.
7. Oculta con `#` solo el contexto imprescindible.
8. Ejecuta `cargo doc` y `cargo test --doc` en CI.
9. Sigue las [Rust API Guidelines – Documentation](https://rust-lang.github.io/api-guidelines/documentation.html).

---

[← 6. Listas de tareas](06-listas-de-tareas.md) · [Índice general](README.md) · [8. README.md →](08-readme-md.md)
