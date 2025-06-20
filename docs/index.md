# 🛠️ Guía del Usuario – Backoffice

## 📌 Índice

1. [Introducción](#introducción)  
2. [Inicio de Sesión](#inicio-de-sesión)  
3. [Registro de Administradores](#registro-de-administradores)  
4. [Gestión de Usuarios y Permisos](#gestión-de-usuarios-y-permisos)  
5. [Configuración de Reglas y Normativas](#configuración-de-reglas-y-normativas)  
6. [Soporte](#soporte)

---

## Introducción

El backoffice es una herramienta diseñada para que los administradores puedan gestionar usuarios, accesos, configuraciones y normativas dentro de la plataforma. Esta guía tiene como objetivo brindar una referencia clara sobre cómo utilizar las principales funcionalidades del sistema.

---

## Inicio de Sesión

### ¿Cómo acceder?

1. Ingresar a la URL del backoffice: `https://classconnect-backoffice.vercel.app/`  
2. Completar los campos de correo electrónico y contraseña.  
3. Hacer clic en **Iniciar Sesión**.

### Mensajes posibles

- ✅ **Inicio exitoso:** El sistema redirigirá al panel principal.  
- ❌ **Error en las credenciales:** Se mostrará un mensaje indicando que los datos ingresados no son válidos.

---

## Registro de Administradores

### ¿Cómo registrar a un nuevo administrador?

1. Ingresar con una cuenta de administrador.  
2. Hacer clic donde dice "Register an Admin here".  
3. Completar el formulario con los datos requeridos.  
4. Hacer clic en **Register**.

### Resultados esperados

- ✅ **Registro exitoso:** El nuevo administrador podrá acceder al sistema utilizando sus credenciales.  
- ⚠️ **Datos faltantes o inválidos:** Se indicarán los errores para su corrección.  
- ❌ **Fallo del servicio:** El sistema informará si no se puede procesar la solicitud.

---

## Gestión de Usuarios y Permisos

### Visualización del listado de usuarios

* En la página de inicio, se mostrará un listado con nombre, rol, estado (activo/bloqueado) y fecha de registro de cada usuario.

### Edición de roles y permisos

1. Para cada usuario, se visualizará la opción de modificar su rol según corresponda.  
2. Se mostrará una opción para confirmar los cambios realizados.  
3. El sistema confirmará que la actualización fue realizada con éxito.

### Bloqueo y desbloqueo de usuarios

1. Desde el listado, para cada usuario se podrá utilizar el botón correspondiente para **Block** o **Unblock**.  
2. Se mostrará una opción para confirmar los cambios realizados.  
3. El sistema confirmará que la actualización fue realizada con éxito.

### Registro de auditoría

* Toda modificación será registrada automáticamente, incluyendo:

  * Usuario afectado  
  * Acción realizada  
  * Fecha y hora  

---

## Configuración de Reglas y Normativas

### Creación y modificación de reglas

1. En la página de inicio, estará disponible un botón "Add rules" para acceder a configuración de las reglas.  
2. Para crear una nueva regla, completar el formulario con todos los datos pedidos y hacer clic en "Add rule"  
3. Para editar una existente, seleccionarla del listado, haciendo clic en "Edit".  
4. Completar o modificar los campos requeridos:

   * Título  
   * Descripción  
   * Fecha de vigencia  
   * Condiciones de aplicación  

### Validaciones

* El sistema validará la integridad de los datos. No será posible guardar reglas con información incompleta.

### Publicación y notificaciones

* Una vez guardadas, las normativas se publicarán y se notificará a los usuarios relevantes mediante correo electrónico y/o notificaciones push.

### Registro de cambios

* Todas las acciones realizadas quedarán registradas:

  * Usuario que efectuó el cambio  
  * Tipo de modificación  
  * Fecha y hora  

---

## Soporte

Para consultas técnicas o reportes de errores, contactarse con el equipo de soporte:  
📧 **[classconnect.team.uba@gmail.com](mailto:classconnect.team.uba@gmail.com)**
