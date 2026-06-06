import pynput as pn
import random
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox

# --- VARIABLES GLOBALES DEL CORE ---
areas = []
frecuencia_segundos = 0.0
corriendo_clicks = False
teclas_presionadas = set()
chances = []
mouse_control = pn.mouse.Controller()

# --- CALLBACKS DE PYNPUT ---
presionando = False
apretado = False
xst, yst = 0, 0
xfn, yfn = 0, 0

def on_move(x, y):
    global apretado, presionando, xfn, yfn, xst, yst
    if apretado and not presionando:
        presionando = True
        xst, yst = x, y
    if presionando:
        xfn, yfn = x, y
        # Actualizamos la etiqueta de estado de la GUI de forma segura
        lbl_status.config(text=f"Seleccionando: ({xst}, {yst}) hasta ({xfn}, {yfn})")
        
def on_click(x, y, button, pressed):
    global apretado, presionando, xst, yst, xfn, yfn
    apretado = pressed
    if not pressed and presionando:
        presionando = False
        # Corregimos orden de coordenadas de forma nativa (min/max)
        x1, x2 = min(xst, xfn), max(xst, xfn)
        y1, y2 = min(yst, yfn), max(yst, yfn)
        areas.append((x1, y1, x2, y2))
        actualizar_lista_areas()

def on_press(tecla):
    global corriendo_clicks
    if tecla == pn.keyboard.Key.space and escuchador_mouse.is_alive():
        # Detener la fase de captura
        escuchador_mouse.stop()
        lbl_status.config(text="Fase de selección finalizada.")
        btn_start_clicks.config(state="normal")
        return False
        
    if tecla == pn.keyboard.Key.esc and corriendo_clicks:
        # Detener la fase de autoclicker
        corriendo_clicks = False
        lbl_status.config(text="Bot detenido por el usuario.")
        btn_setup_areas.config(state="normal")
        btn_start_clicks.config(text="Iniciar Autoclicker")
        return False

# --- LÓGICA DE PROCESAMIENTO ---
def find_idx(e, l):
    i = 0
    while l[i] < e:
        i += 1
    return i

def bucle_autoclicker():
    global corriendo_clicks, frecuencia_segundos, chances, areas
    
    # Procesar chances acumulativas una única vez
    chances = [1]*len(areas)
    chances_acum = [sum([chances[j] for j in range(i+1)]) for i in range(len(chances))]
    
    while corriendo_clicks:
        num = random.randint(1, chances_acum[-1])
        area = areas[find_idx(num, chances_acum)]
        
        x = random.randint(area[0], area[2])
        y = random.randint(area[1], area[3])
        
        mouse_control.position = (x, y)
        mouse_control.press(pn.mouse.Button.left)
        mouse_control.release(pn.mouse.Button.left)
        
        time.sleep(frecuencia_segundos)

# --- CONTROLADORES DE LA INTERFAZ ---
def iniciar_captura_areas():
    global escuchador_mouse, escuchador_teclado
    root.focus_set()
    areas.clear()
    actualizar_lista_areas()
    
    

    lbl_status.config(text="Registrando áreas... Arrastra el mouse. Presiona ESPACIO al terminar.")
    btn_start_clicks.config(state="disabled")
    
    escuchador_mouse = pn.mouse.Listener(on_click=on_click, on_move=on_move)
    escuchador_teclado = pn.keyboard.Listener(on_press=on_press)
    escuchador_mouse.start()
    escuchador_teclado.start()

def alternar_autoclicker():
    global corriendo_clicks, escuchador_global_teclado
    # Leer y validar la frecuencia del formulario antes de iniciar
    try:
        valor = float(entry_frec.get())
        unidad = combo_unidad.get()
        global frecuencia_segundos
        if unidad == "Milisegundos (ms)": frecuencia_segundos = valor * 0.001
        elif unidad == "Segundos (s)": frecuencia_segundos = valor
        elif unidad == "Minutos (m)": frecuencia_segundos = valor * 60.0
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa un número válido en la frecuencia.")
        return
    
    if not areas:
        messagebox.showwarning("Advertencia", "Primero debes configurar al menos un área.")
        return

    if not corriendo_clicks:
        # Iniciar modo Autoclicker
        corriendo_clicks = True
        btn_start_clicks.config(text="Detener Autoclicker (o presiona ESC)")
        btn_setup_areas.config(state="disabled")
        lbl_status.config(text="Autoclicker ACTIVO. Presiona ESC para frenar.")
        
        # Hilo secundario para que no se congele la ventana
        hilo_bot = threading.Thread(target=bucle_autoclicker, daemon=True)
        hilo_bot.start()
        
        # Listener para capturar el botón de escape de manera global
        escuchador_global_teclado = pn.keyboard.Listener(on_press=on_press)
        escuchador_global_teclado.start()
    else:
        # Detener modo Autoclicker de forma manual desde el botón
        corriendo_clicks = False
        escuchador_global_teclado.stop()
        btn_start_clicks.config(text="Iniciar Autoclicker")
        btn_setup_areas.config(state="normal")
        lbl_status.config(text="Autoclicker detenido.")

def actualizar_lista_areas():
    listbox_areas.delete(0, tk.END)
    for idx, area in enumerate(areas):
        listbox_areas.insert(tk.END, f"Área {idx+1}: X({area[0]} a {area[2]}) | Y({area[1]} a {area[3]})")

# --- CONSTRUCCIÓN DE LA VENTANA (GUI) ---
root = tk.Tk()
root.title("AutoClicker Personalizado")
root.geometry("480x450")
root.resizable(False, False)

# Panel de Formulario / Configuración de Frecuencia
frame_form = ttk.LabelFrame(root, text=" Configuración de Frecuencia ", padding=10)
frame_form.pack(fill="x", padx=15, pady=10)

ttk.Label(frame_form, text="Intervalo:").grid(row=0, column=0, sticky="w", padx=5)
entry_frec = ttk.Entry(frame_form, width=12)
entry_frec.insert(0, "100")  # Valor por defecto
entry_frec.grid(row=0, column=1, padx=5)

combo_unidad = ttk.Combobox(frame_form, values=["Milisegundos (ms)", "Segundos (s)", "Minutos (m)"], state="readonly", width=18)
combo_unidad.current(0)  # Selecciona milisegundos por defecto
combo_unidad.grid(row=0, column=2, padx=5)

# Panel de Control de Áreas
frame_areas = ttk.LabelFrame(root, text=" Zonas Seleccionadas ", padding=10)
frame_areas.pack(fill="both", expand=True, padx=15, pady=5)

btn_setup_areas = ttk.Button(frame_areas, text="1. Configurar Áreas de Pantalla", command=iniciar_captura_areas)
btn_setup_areas.pack(fill="x", pady=5)

listbox_areas = tk.Listbox(frame_areas, height=6)
listbox_areas.pack(fill="both", expand=True, pady=5)

# Panel de Acción Inferior
frame_action = tk.Frame(root) # Usamos empaquetado nativo para el botón de acción
btn_start_clicks = ttk.Button(root, text="2. Iniciar Autoclicker", command=alternar_autoclicker, state="disabled")
btn_start_clicks.pack(fill="x", padx=15, pady=10)

# Barra de Estado (Status Bar)
lbl_status = ttk.Label(root, text="Listo para configurar.", relief="sunken", anchor="w", padding=5)
lbl_status.pack(fill="x", side="bottom")

# Arrancar la interfaz gráfica
root.mainloop()