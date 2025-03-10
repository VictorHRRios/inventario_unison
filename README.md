# Inventario UNISON

Este aplicación de sistema de inventario fue un proyecto en la clase de Ingeniería de Software II, donde los integrantes desarrollamos un prototipo para resolver una problemática en el departamento de matemáticas de la Universidad de Sonora. 

### Que puedes hacer en esta aplicación

* El sistema maneja dos tipos de usuarios `admin` y `empleado`. El `admin` será el encargado de gestionar los `empleados` y el `inventario` mediante CRUD, además de tener una pestaña de movimientos y reportes.
* Ambos usuarios tienen acceso a las pestañas del dashboard principal, el carrito de compras, y el perfil del usuario.
* El funcionamiento principal de la aplicación es en el dashboard donde puedes agregar al carrito los diferentes artículos. Una vez agregados al carrito, puedes ver los artículos en la pestaña del carrito, además de otros atributos como la descripción del producto, una imágen, descripción y la cantidad.
* La pestaña del carrito tiene diferentes funcionalidades como eliminar, agregar una justificación y una vista detallada del artículo. 

---

## Instalación

Instala en tu sistema la versión 3.10.4 de python. Después de clonar el proyecto, y estar en un ambiente de python, ejecuta el siguiente comando `pip install -r requirements.txt`, este comando instalará todos los paquetes necesarios para ejecutar satisfactoriamente el proyecto.

## Modo de uso

Ejecuta el comando `python manage.py runserver` para inicializar la aplicación en un servidor local. Para agregar un superusuario para poder acceder a la aplicación ejecuta el comando `python manage.py createsuperuser`, para más información de los comandos de django puedes checar la documentación de [django-admin](https://docs.djangoproject.com/en/5.1/ref/django-admin/).

## Desarrollo

Este proyecto fue realizado por Víctor Hugo Ramírez Ríos, Gustavo Gutierrez Navarro y Ángel David Durazo Bartollini en un plazo de tres meses para la materia de Ingeniería de Software II.