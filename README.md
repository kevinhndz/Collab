# API de Biblioteca

Este proyecto es una API hecha con **FastAPI**, **SQLAlchemy** y una base de datos **SQLite**. Permite trabajar con usuarios, libros y préstamos. También incluye la consulta de aulas. La idea del repositorio es aprender a construir la API **y** a colaborar sin que el trabajo de una persona rompa el de las demás.

## Cómo está organizado el código

- `main.py` crea la aplicación y conecta sus rutas.
- `modulos/` separa usuarios, libros, préstamos y aulas. En cada módulo, `router.py` recibe las peticiones, `service.py` contiene las reglas de negocio y `repository.py` habla con la base de datos.
- `database/almacen.py` configura la conexión a la base de datos.
- `tests/` contiene las pruebas de los endpoints.
- `.github/workflows/config.yml` define la revisión automática de GitHub Actions.

Por ejemplo, cuando alguien envía `POST /libros/`, la petición entra por el *router*, pasa por el *service* y termina en el *repository*, que guarda el libro. Separar esas tareas hace más fácil encontrar un error y repartir el trabajo entre colaboradores.

## Ejecutarlo en tu computadora

Desde la carpeta del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Crea un archivo `.env` con esta línea:

```text
DATABASE_URL=sqlite:///./biblioteca.db
```

Después inicia la API:

```bash
python -m uvicorn main:app --reload
```

Abre `http://127.0.0.1:8000/docs` para probar sus rutas desde el navegador. El archivo `.env` y la base de datos local están excluidos de Git.

## ¿Qué es GitHub Projects y por qué nos ayuda?

**GitHub Projects** es un tablero para organizar el trabajo. Cada tarea puede ser un *Issue* (una descripción concreta de algo por hacer) y el tablero puede mostrarla como **Pendiente**, **En progreso** o **Terminada**. Un *Pull Request* (PR) también puede aparecer allí. Esto permite ver quién se encarga de cada tarea y qué falta, sin tener que adivinarlo por los archivos modificados.

En esta API, una tarea podría ser: “Agregar `GET /prestamos/{id}`”. Otra podría ser: “Probar qué ocurre al borrar un libro inexistente”. Si ambas están descritas y asignadas, dos personas pueden trabajar en paralelo con menos confusión. Projects **organiza** el trabajo; Git y los PR son los que guardan y revisan el código.

Un tablero sencillo para el equipo podría tener estas columnas:

| Pendiente | En progreso | En revisión | Terminado |
| --- | --- | --- | --- |
| Tarea definida | Alguien trabaja en su rama | PR abierto y CI en marcha | PR integrado en `main` |

## El camino de una tarea hasta `main`

1. Crear un Issue y ponerlo en Projects para que todos sepan qué se hará.
2. Crear una rama desde una versión reciente de `main`, por ejemplo `feature/prestamos-get-id`.
3. Hacer el cambio y agregar una prueba que compruebe el comportamiento esperado.
4. Ejecutar las pruebas en la computadora, guardar el trabajo con `git commit` y subir la rama con `git push`.
5. Abrir un PR hacia `main`, explicar el cambio y vincular el Issue.
6. Revisar los comentarios de los compañeros y el resultado del CI. Corregir lo que falle.
7. Integrar el PR cuando esté listo y mover la tarea a **Terminado**.

Ejemplo de comandos para comenzar una tarea:

```bash
git switch main
git pull origin main
git switch -c feature/prestamos-get-id
```

En equipos de desarrollo se suele trabajar así porque cada cambio queda visible, se puede discutir antes de integrarlo y tiene un responsable. La rama `main` representa el trabajo compartido; por eso conviene llevar los cambios mediante PR en lugar de subirlos directamente a ella.

## ¿Por qué el CI va de la mano con el PR?

**CI** significa *integración continua*. Es una revisión automática que se ejecuta cuando subimos cambios. En este repositorio, el archivo `.github/workflows/config.yml` hace que GitHub Actions instale Python 3.11 y las dependencias, y ejecute `python -m pytest -v` cuando se abre o actualiza un PR hacia `main` y cuando hay un `push` a `main`.

El **PR** es el lugar donde una persona revisa la idea y el código. El **CI** comprueba de forma repetible si pasan las pruebas. Los dos se complementan: una prueba puede detectar un error que se nos escapó al leer el código; una persona puede detectar un problema de diseño que las pruebas no cubren.

Si CI aparece en rojo, se abre el detalle del trabajo `build`, se lee el error, se corrige en la misma rama y se vuelve a subir. GitHub ejecutará la revisión otra vez. Para que un PR **no pueda integrarse** cuando CI falla, también hay que configurar una regla de protección o un *ruleset* para `main` que exija el check `build`. Tener el YAML por sí solo no bloquea el botón de *merge*.

## ¿Por qué son importantes las pruebas?

Una prueba ejecuta una acción y compara el resultado con lo que esperamos. Por ejemplo, `tests/test_libros.py` crea un libro con `POST /libros/` y comprueba que la API devuelve `201`. También prueba que, después de borrar un libro, buscarlo devuelve `404`. Otras pruebas revisan actualizaciones y datos inválidos.

Si alguien cambia el código de préstamos y por accidente afecta la creación de libros, las pruebas de libros pueden avisar antes de que ese cambio llegue a `main`. Eso nos da confianza para modificar la API, aunque **ninguna suite garantiza que sea imposible romperla**: solo comprueba los casos escritos.

Las pruebas de `tests/` usan `TestClient` para llamar a la API y una base SQLite de prueba que se crea para cada caso. Así no dependen de los datos de `biblioteca.db`. Aunque solemos llamarles “pruebas unitarias”, estas pruebas de endpoints comprueban varias capas juntas: ruta, servicio y base de datos. Por eso también son **pruebas de integración pequeñas**.

Para ejecutarlas:

```bash
python -m pytest -v
```

Cuando se agrega una ruta nueva, conviene probar al menos un caso que funcione y los errores que esa ruta promete manejar. Un resultado verde significa que **esos casos** pasaron; no reemplaza la revisión del PR ni probar manualmente lo que todavía no está cubierto.

## Cómo resolver conflictos entre ramas

Un conflicto aparece cuando Git no puede decidir cómo unir cambios, normalmente porque dos personas editaron la misma parte de un archivo. No es culpa de nadie: Git nos está pidiendo que decidamos cuál debe ser el resultado final.

Desde tu rama de trabajo:

```bash
git fetch origin
git merge origin/main
```

Si Git avisa de un conflicto, abre cada archivo señalado. Verás marcas como estas:

```text
mi cambio
cambio que llegó de main
```

Lee **ambos** cambios y deja el código final que de verdad debe funcionar. A veces hay que combinar las dos ideas. Borra también las tres líneas de marcas. Después:

```bash
git status
git add ruta/del/archivo.py
git commit
python -m pytest -v
git push
```

Git también puede considerar terminado un conflicto aunque alguien haya dejado las marcas como texto normal. Antes del commit, busca `<<<<<<<`, `=======` y `>>>>>>>` en los archivos editados y revisa que el código tenga sentido. Si no sabes qué comportamiento conservar, habla con la persona que hizo el otro cambio; no elijas una versión al azar. Si todavía no quieres resolver el conflicto, `git merge --abort` devuelve la rama al estado anterior al intento de unión.

## En resumen

**Projects** nos dice qué hay que hacer y quién lo está haciendo. **Las ramas** aíslan el trabajo. **Las pruebas** comprueban casos concretos de la API. **El PR** permite que otras personas revisen el cambio. **CI** ejecuta las pruebas automáticamente antes de compartirlo con `main`. El resultado es un proceso más ordenado y con menos sorpresas para el equipo.

Más información: [GitHub Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects), [checks de los PR](https://docs.github.com/en/pull-requests/reference/status-checks) y [resolución de conflictos](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/resolving-a-merge-conflict-using-the-command-line).
