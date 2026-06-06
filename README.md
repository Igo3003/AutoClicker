# 🖱️ AutoClicker Personalizado 

Un AutoClicker inteligente y con interfaz gráfica desarrollado en Python, el cual permite registrar múltiples áreas de la pantalla mediante arrastre del mouse y realiza clics automáticos distribuidos aleatoriamente dentro de esas zonas. 

Ideal para automatizar tareas repetitivas o pruebas de software sin congelar la pantalla, gracias al uso de programación multihilo (*multithreading*).

---

## ✨ Características

* **Configuración de Frecuencia:** Permite establecer el intervalo de clics en milisegundos, segundos o minutos desde un formulario amigable.
* **Múltiples Zonas de Clic:** Registra áreas personalizadas manteniendo presionado y arrastrando el mouse en cualquier parte de la pantalla.
* **Control Global por Teclado:** * Presiona `Espacio` para finalizar la captura de pantallas.
  * Presiona `Esc` en cualquier momento para detener los clics automáticos de forma segura.
* **Interfaz Fluida:** Diseñado con Tkinter y optimizado con hilos en segundo plano para evitar que la ventana se cuelgue ("No responde").

---

## 🚀 Cómo usarlo (Sin instalar Python)

Si solo querés usar la aplicación en Windows, podés descargar el ejecutable listo para usar:

1. Andá a la sección de **Releases** (Lanzamientos) en el lateral derecho de este repositorio.
2. Descargá el archivo `AutoClicker.exe`.
3. Ejecutalo. *(Nota: Si Windows SmartScreen muestra una advertencia, haz clic en "Más información" -> "Ejecutar de todas formas").*

---

## 🛠️ Requisitos para Desarrollo

Si deseas ejecutar o modificar el código fuente, necesitarás tener instalado **Python 3.10+** y ejecutar el siguiente comando en consola:

```bash
pip install -r requirements.txt
```

---

## ✨ Futuras expansiones
* **Añadir probabilidades ponderadas para cada área seleccionada
