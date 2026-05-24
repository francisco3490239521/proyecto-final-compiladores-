import tkinter as tk
from tkinter import filedialog, messagebox

# =====================================================
# FUNCIONES DEL COMPILADOR (ejemplo con errores detallados)
# =====================================================

# =====================================================
# FUNCIONES DEL COMPILADOR (ejemplo con errores detallados)
# =====================================================

def lexer(codigo):
    tokens = []
    for num_linea, linea in enumerate(codigo.splitlines(), start=1):
        for num_col, palabra in enumerate(linea.split(), start=1):
            if "@" in palabra:
                raise Exception(f"Error léxico en línea {num_linea}, columna {num_col}: símbolo inválido '@'")
            tokens.append((palabra, f"L{num_linea}:C{num_col}"))
    return tokens

def parse(tokens):
    mensajes = []
    valido = True

    # Recorre los tokens buscando declaraciones
    for i, (palabra, pos) in enumerate(tokens):
        if palabra in ["entero", "decimal", "cadena", "booleano"]:
            # Busca ';' en los siguientes tokens hasta 6 posiciones adelante
            tiene_punto_y_coma = any(t[0].endswith(";") or t[0] == ";" for t in tokens[i+1:i+6])
            if not tiene_punto_y_coma:
                mensajes.append(f"Error sintáctico: falta ';' en {pos}")
                valido = False

    # Si no hay errores, muestra confirmación
    if valido:
        mensajes.append("Análisis sintáctico correcto ✅")

    return valido, mensajes




# Máquina virtual básica que interpreta asignaciones e imprimir()
def ejecutar():
    codigo = entrada_text.get("1.0", tk.END).strip()
    salida = []
    memoria = {}

    for num_linea, linea in enumerate(codigo.splitlines(), start=1):
        linea = linea.strip()
        if not linea or linea.startswith("//"):
            continue

        # Asignaciones
        if "=" in linea and not linea.startswith("imprimir"):
            try:
                var, expr = linea.split("=")
                var = var.strip().replace("entero ", "").replace("decimal ", "").replace("cadena ", "")
                expr = expr.strip().rstrip(";")

                # Si la expresión es una suma de variables
                if "+" in expr:
                    partes = expr.split("+")
                    valores = []
                    for p in partes:
                        p = p.strip()
                        if p in memoria:
                            valores.append(memoria[p])
                        else:
                            valores.append(int(p))
                    memoria[var] = sum(valores)
                else:
                    # Caso simple: número directo
                    memoria[var] = int(expr)
            except Exception as e:
                salida.append(f"Error en línea {num_linea}: {e}")

        # Imprimir
        if "imprimir" in linea:
            contenido = linea[linea.find("(")+1:linea.find(")")].strip()
            if contenido.startswith('"') and contenido.endswith('"'):
                salida.append(contenido.strip('"'))
            elif contenido in memoria:
                salida.append(str(memoria[contenido]))
            else:
                salida.append(contenido)

    salida.append("REPORTE: Ejecución completada correctamente")
    return "\n".join(salida)


def cargar_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("RadarScript files", "*.rdr")])
    if ruta:
        with open(ruta, "r", encoding="utf-8") as f:
            codigo = f.read()
        entrada_text.delete("1.0", tk.END)
        entrada_text.insert(tk.END, codigo)

def guardar_reporte():
    contenido = salida_text.get("1.0", tk.END).strip()
    if not contenido:
        messagebox.showwarning("Guardar reporte", "No hay contenido para guardar.")
        return
    archivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Archivo de texto", "*.txt"), ("Log file", "*.log")]
    )
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        messagebox.showinfo("Guardar reporte", f"Reporte guardado en:\n{archivo}")

def compilar():
    codigo = entrada_text.get("1.0", tk.END)
    try:
        tokens_generados = lexer(codigo)
        valido, mensajes = parse(tokens_generados)

        salida_text.delete("1.0", tk.END)
        salida_text.insert(tk.END, "Tokens:\n")
        for t in tokens_generados:
            salida_text.insert(tk.END, f"{t}\n")

        salida_text.insert(tk.END, "\nParser:\n")
        for m in mensajes:
            salida_text.insert(tk.END, f"{m}\n")

        if valido:
            messagebox.showinfo("Compilación", "Compilación exitosa ✅")
        else:
            salida_text.insert(tk.END, "\n❌ Errores detectados:\n")
            for m in mensajes:
                salida_text.insert(tk.END, f"{m}\n")
            messagebox.showerror("Errores sintácticos", "\n".join(mensajes))

        # Guardar salida automática
        with open("salida_compilacion.log", "w", encoding="utf-8") as f:
            f.write(salida_text.get("1.0", tk.END))

    except Exception as e:
        salida_text.insert(tk.END, f"\n❌ Error: {str(e)}\n")
        messagebox.showerror("Error", str(e))

def ejecutar_vm():
    salida_text.insert(tk.END, "\nEjecutando VM...\n")
    resultado = ejecutar()
    salida_text.insert(tk.END, resultado)


# =====================================================
# INTERFAZ GRÁFICA MODERNA
# =====================================================

ventana = tk.Tk()
ventana.title("RadarScript Compiler")
ventana.geometry("1200x750")
ventana.configure(bg="#0f172a")
ventana.resizable(False, False)

# Estilos
COLOR_FONDO = "#0f172a"
COLOR_PANEL = "#1e293b"
COLOR_ENTRADA = "#111827"
COLOR_BOTON_1 = "#06b6d4"
COLOR_BOTON_2 = "#22c55e"
COLOR_BOTON_3 = "#f59e0b"
COLOR_BOTON_4 = "#3b82f6"
COLOR_BORDE = "#334155"

FONT_TITLE = ("Segoe UI Black", 24)
FONT_SUB = ("Segoe UI", 12, "bold")
FONT_TEXT = ("Consolas", 11)
FONT_BUTTON = ("Segoe UI", 11, "bold")

# Header
titulo = tk.Label(ventana, text="⚡ RADARSCRIPT COMPILER",
                  font=FONT_TITLE, bg=COLOR_FONDO, fg="white")
titulo.pack(pady=(15, 5))

subtitulo = tk.Label(ventana,
    text="Compilador Léxico • Sintáctico • Semántico • Máquina Virtual",
    font=("Segoe UI", 10), bg=COLOR_FONDO, fg="#94a3b8")
subtitulo.pack(pady=(0, 15))

# =====================================================
# BOTONES (centrados debajo del título)
# =====================================================

frame_botones = tk.Frame(ventana, bg=COLOR_FONDO)
frame_botones.pack(pady=(10, 10))

btn_cargar = tk.Button(frame_botones, text="📂 Cargar archivo", command=cargar_archivo,
                       bg=COLOR_BOTON_1, fg="white", font=FONT_BUTTON,
                       width=18, height=2, bd=0, cursor="hand2", activebackground="#0891b2")
btn_cargar.grid(row=0, column=0, padx=10)

btn_compilar = tk.Button(frame_botones, text="⚙ Compilar", command=compilar,
                         bg=COLOR_BOTON_2, fg="white", font=FONT_BUTTON,
                         width=18, height=2, bd=0, cursor="hand2", activebackground="#16a34a")
btn_compilar.grid(row=0, column=1, padx=10)

btn_ejecutar = tk.Button(frame_botones, text="▶ Ejecutar VM", command=ejecutar_vm,
                         bg=COLOR_BOTON_3, fg="white", font=FONT_BUTTON,
                         width=18, height=2, bd=0, cursor="hand2", activebackground="#d97706")
btn_ejecutar.grid(row=0, column=2, padx=10)

btn_guardar = tk.Button(frame_botones, text="💾 Guardar reporte", command=guardar_reporte,
                        bg=COLOR_BOTON_4, fg="white", font=FONT_BUTTON,
                        width=18, height=2, bd=0, cursor="hand2", activebackground="#2563eb")
btn_guardar.grid(row=0, column=3, padx=10)

# =====================================================
# PANEL PRINCIPAL
# =====================================================

frame_main = tk.Frame(ventana, bg=COLOR_FONDO)
frame_main.pack(fill="both", expand=True, padx=20)

# Panel izquierdo
panel_izq = tk.Frame(frame_main, bg=COLOR_PANEL,
                     highlightbackground=COLOR_BORDE, highlightthickness=2)
panel_izq.pack(side="left", fill="both", expand=True, padx=10)

# Panel derecho
panel_der = tk.Frame(frame_main, bg=COLOR_PANEL,
                     highlightbackground=COLOR_BORDE, highlightthickness=2)
panel_der.pack(side="right", fill="both", expand=True, padx=10)

# Entrada
label_entrada = tk.Label(panel_izq, text="📝 Código Fuente RadarScript",
                         font=FONT_SUB, bg=COLOR_PANEL, fg="white")
label_entrada.pack(pady=10)

entrada_text = tk.Text(panel_izq, height=28, width=58, bg=COLOR_ENTRADA,
                       fg="#22c55e", insertbackground="white",
                       font=FONT_TEXT, relief="flat", padx=10, pady=10)
entrada_text.pack(padx=15, pady=10)

nombre_izq = tk.Label(panel_izq, text="Panel de Código Fuente", font=("Segoe UI", 10),
                      bg=COLOR_PANEL, fg="#94a3b8")
nombre_izq.pack(pady=(0, 10))

# Salida
label_salida = tk.Label(panel_der, text="📊 Resultado de Compilación",
                        font=FONT_SUB, bg=COLOR_PANEL, fg="white")
label_salida.pack(pady=10)

salida_text = tk.Text(panel_der, height=28, width=58, bg=COLOR_ENTRADA,
                      fg="#e2e8f0", insertbackground="white",
                      font=FONT_TEXT, relief="flat", padx=10, pady=10)
salida_text.pack(padx=15, pady=10)

nombre_der = tk.Label(panel_der, text="Panel de Resultados", font=("Segoe UI", 10),
                      bg=COLOR_PANEL, fg="#94a3b8")
nombre_der.pack(pady=(0, 10))


# =====================================================
# FOOTER
# =====================================================

footer = tk.Label(ventana, text="RadarScript IDE v1.0",
                  bg=COLOR_FONDO, fg="#64748b", font=("Segoe UI", 9))
footer.pack(pady=8)

# =====================================================
# INICIAR APLICACIÓN
# =====================================================

ventana.mainloop()
