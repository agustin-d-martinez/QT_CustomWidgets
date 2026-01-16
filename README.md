# Qt Custom Widgets

Colección de **widgets personalizados en PySide6 / Qt**, pensados para ser **reutilizables**, **modulares** y **fáciles de integrar** en cualquier proyecto Qt.

El objetivo de este repositorio es servir como **base común** para interfaces modernas en Qt, evitando reimplementar soluciones habituales como:

* ventanas frameless
* titlebars personalizadas
* botones animados
* widgets drag & drop
* overlays y helpers visuales

---

## Contenido

El paquete principal es `CustomWidgets`, que contiene los siguientes componentes:

### Ventanas y Layout

* **`FramelessWindow`**
  Ventana sin marco nativo del sistema, con:

  * resize por bordes y esquinas
  * comportamiento similar a ventanas nativas
  * compatible con cualquier `QMainWindow`

* **`TitleBar`**
  Barra de título personalizada, pensada para usarse junto a `FramelessWindow` o por separado, con:

  * Context Menu.
  * Drag de la aplicación.
  * botones de minimizar, maximizar y cerrar.
  * Ícono y nombre de la app (eliminar de setup_ui si no se desean usar).

---

### Controles

* **`AnimatedButton`**
  Botón sencillo con animacion de hover y click. Aumenta ligeramente su tamaño. Puede usarse de base para saber cómo añadir animaciones.

* **`ModernCheckBox`**
  Checkbox animado con forma circular que se desliza de izquierda a derecha. Posee:
  * 3 Propiedades propias para modificar sus colores con un stylesheet.
  * Animación de check.
  * Compatible con texto (aunque se recomienda colocar un QLabel externo).

* **`ButtonListWidget`**
  LisWidget con el añadido de 4 botones para su manejo con mouse. Posee:
  * Botón de subir y bajar elemento.
  * Botón de eliminar elemento.
  * Botón de añadir elemento (crea un editor en la lista para escribir el valor a mano).
  * Herencia de DroppableListWidget.

---

### Drag & Drop

* **`DroppableImageLabel`**
  `QLabel` que acepta imágenes mediante drag & drop. Posee:
  * Funcionalidad drag & drop para imágenes, url, o direcciones de la PC.
  * Context menu para añadir imágenes, copiar, pegar, cortar o eliminar.

* **`DroppableList`**
  Lista con soporte para elementos arrastrables. Posee:
  * Funcionalidad drag & drop.
  * Context menu para añadir un elemento a la lista, eliminar un elemento de la lista, subir y bajar un elemento de la lista.

---

### Helpers y overlays

Estos en principio no deberían utilizarse, son archivos auxiliares de otras clases. Se pueden llegar a reutilizar para nuevos CustomWidgets.

* **`QtDragHelper`**
  Utilidades para manejo de drag en Qt.

* **`SnapOverlay`**
  Overlay visual para efectos de snapping o guía de posicionamiento.

---

## Tests

El directorio `test/` contiene el scripts para prueba de los widgets.

```bash
test/
 └── test.py
```

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/qt_customwidgets.git
cd qt_customwidgets
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

> El proyecto está pensado para usarse directamente como módulo, no requiere instalación como paquete.

---

## Uso básico

Ejemplo simple usando `FramelessWindow`:

```python
from PySide6.QtWidgets import QApplication, QLabel
from CustomWidgets.FramelessWindow import FramelessWindow

app = QApplication([])

window = FramelessWindow()
window.setCentralWidget(QLabel("Hola mundo"))
window.resize(800, 600)
window.show()

app.exec()
```

Este repositorio **no impone estilos ni layouts**, sino que ofrece **bloques reutilizables**.

---

## Requisitos

* Python 3.10+
* PySide6
* Qt 6+

---

## Licencia

Este proyecto se distribuye bajo la licencia **MIT**.
Ver el archivo `LICENSE` para más información.

---

## Estado

El proyecto está en **desarrollo activo**.
La API puede evolucionar, pero los widgets están pensados para ser estables y reutilizables.

