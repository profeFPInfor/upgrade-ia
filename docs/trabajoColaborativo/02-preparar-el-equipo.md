# 2. Preparar el equipo

← [Anterior: Conceptos](01-conceptos.md) · [Siguiente: Carpeta de trabajo](03-primer-dia.md) →

Se hace **una sola vez**. Son cinco cosas: cuenta, invitación, Git e identidad, acceso y VS Code.

## 2.1 Crear tu cuenta de GitHub

1. Entra en [github.com](https://github.com) y pulsa *Sign up*.
2. Elige un nombre de usuario. Lo verán tus compañeros y el profesor; elige uno que no te importe que vean.
3. Verifica tu correo.
4. **Activa la autenticación en dos pasos (2FA)** en los ajustes de seguridad de tu cuenta. Protege tu cuenta si alguien consigue tu contraseña. Guía: [Configuring two-factor authentication](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication).

## 2.2 Aceptar la invitación al repositorio

El profesor te añade como **colaborador** del repositorio `upgrade-ia`, es decir, con permiso de escritura. Recibirás un correo de GitHub con la invitación.

1. Abre el correo y pulsa el enlace, o entra en la página del repositorio, donde verás un aviso para aceptar.
2. Acepta la invitación.

Sin este paso no podrás subir tus ramas. Si no te llega, avisa al profesor con tu nombre de usuario.

## 2.3 Instalar Git

| Sistema | Cómo |
|---|---|
| **Windows** | Descarga el instalador de [git-scm.com](https://git-scm.com/download/win) y acepta las opciones por defecto. |
| **macOS** | Abre la terminal y escribe `git --version`. Si no está instalado, el sistema te ofrece instalarlo. |
| **Linux** (Debian/Ubuntu) | `sudo apt install git` |

En los equipos de clase, Git ya viene instalado. Comprueba que funciona:

```bash
git --version
```

Debe mostrar algo como `git version 2.x.x`. El número exacto no importa.

## 2.4 Decirle a Git quién eres

Cada commit lleva tu nombre y un correo. Se configura una vez:

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu-correo@ejemplo.com"
```

`--global` significa que vale para **todos** los proyectos de tu usuario en este equipo (sin `--global`, solo valdría para el repositorio donde lo ejecutes).

**Ojo con la privacidad:** este repositorio es público, así que el correo de tus commits lo puede ver cualquiera. GitHub te ofrece una dirección privada para esto:

1. En GitHub, pulsa tu foto de perfil (arriba a la derecha) y entra en *Settings*.
2. En la barra lateral, sección *Access*, pulsa *Emails*.
3. Marca *Keep my email addresses private* (mantener mis direcciones de correo privadas).
4. GitHub te muestra una dirección con la forma `ID+usuario@users.noreply.github.com` (el `ID` es un número). Cópiala y úsala como correo en el comando de arriba.

Así GitHub sabe que los commits son tuyos sin enseñar tu correo real. Comprueba lo configurado:

```bash
git config --global --list
```

Fuentes: [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address) y [Email addresses reference](https://docs.github.com/en/account-and-profile/reference/email-addresses-reference).

## 2.5 Acceso desde tu ordenador

Para subir cambios, GitHub tiene que saber que eres tú. **La contraseña de tu cuenta no sirve** para esto. Hay dos caminos; elige uno.

### Opción A: Git Credential Manager (lo más fácil en Windows)

Viene con Git para Windows. La primera vez que descargues o subas algo, se abre una ventana del navegador para que inicies sesión en GitHub. No tienes que hacer nada más.

### Opción B: GitHub CLI (Windows, macOS y Linux)

1. Instala *GitHub CLI* desde [cli.github.com](https://cli.github.com).
2. En la terminal:

   ```bash
   gh auth login
   ```

   Sin opciones, inicia un asistente interactivo. Elige *GitHub.com* y la autenticación con el navegador web, y sigue los pasos.
3. Para que Git use GitHub CLI como ayudante de credenciales:

   ```bash
   gh auth setup-git
   ```

Comprueba que estás dentro:

```bash
gh auth status
```

Fuentes: [gh auth login](https://cli.github.com/manual/gh_auth_login) y [gh auth setup-git](https://cli.github.com/manual/gh_auth_setup-git).

> **Nunca** pegues una clave, un token o una contraseña en un fichero del repositorio ni en un mensaje de commit.

## 2.6 Visual Studio Code

En los equipos de clase ya está instalado **Visual Studio Code** (VS Code). No lo confundas con *Visual Studio*, que es otro programa distinto, de color morado: aquí usamos el de icono azul.

1. Ábrelo desde el menú de aplicaciones.
2. Abre la terminal integrada con el menú *Terminal → New Terminal* (*Terminal → Nueva terminal*). Aquí escribirás los comandos de Git.
3. Comprueba que ve Git: en la terminal escribe `git --version`. Si muestra una versión, VS Code ya puede usarlo; no hay que instalar nada más.

La vista de **Control de código fuente** (*Source Control*) se abre con el atajo `Ctrl+Shift+G` o con el icono del menú lateral izquierdo. Más adelante la usarás para ver tus cambios y hacer commits ([documentación](https://code.visualstudio.com/docs/sourcecontrol/overview)).

Si trabajas en tu propio portátil y no lo tienes, descárgalo de [code.visualstudio.com](https://code.visualstudio.com).

## Comprobación

- [ ] Tienes cuenta en GitHub, con 2FA activada, y has aceptado la invitación.
- [ ] VS Code abre y su terminal integrada reconoce `git --version`.
- [ ] `git config --global --list` muestra tu nombre y tu correo (el `noreply`).
- [ ] Has hecho el acceso: con la opción B, `gh auth status` te muestra como conectado. Con la opción A se comprueba en el paso siguiente, al clonar.

Siguiente: [carpeta de trabajo y descarga del proyecto](03-primer-dia.md).
