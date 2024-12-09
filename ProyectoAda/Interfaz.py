import customtkinter as ctk
from SubastaDinamica import generar_combinacionesDP
from SubastaFuerzaBruta import generar_combinaciones
from SubastaVoraz import asignar_acciones, calcular_valor
from TerInteligenteBruta import calcular_mejor_coste, tupla_con_menor_suma
from TerInteligenteVoraz import interfaz_voraz
from TerInteligenteDinamica import costo_min_din
import time


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Asignación de Acciones")
        self.geometry("600x700")
        self.resizable(True, True)

        # Variables para las entradas
        self.total_acciones = ctk.StringVar(value="")
        self.precio_minimo = ctk.StringVar(value="")
        self.resultado_texto = ctk.StringVar()

        # Configuración inicial
        self.create_tab_view()

    # Configuración de pestañas
    def create_tab_view(self):
        """Crea las pestañas principales de la aplicación."""
        self.tabview = ctk.CTkTabview(self, width=600, height=600)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.subasta_tab = self.tabview.add("Subasta")
        self.terminal_tab = self.tabview.add("Terminal Inteligente")

        self.build_subasta_tab()
        self.build_terminal_tab()

    # Construcción de la pestaña "Subasta"
    def build_subasta_tab(self):
        """Configura el contenido de la pestaña Subasta."""
        container = ctk.CTkFrame(self.subasta_tab)
        container.pack(padx=20, pady=20, fill="both", expand=True)

        self.create_inputs(container)
        self.create_method_selector(container)
        self.create_result_display(container)

    # Construcción de la pestaña "Terminal Inteligente"
    def build_terminal_tab(self):
        """Configura el contenido de la pestaña Terminal Inteligente."""
        terminal_container = ctk.CTkFrame(self.terminal_tab)
        terminal_container.pack(padx=20, pady=20, fill="both", expand=True)

        self.create_terminal_inputs(terminal_container)
        self.create_terminal_buttons(terminal_container)
        self.create_terminal_results(terminal_container)

    # Entradas de la pestaña Terminal
    def create_terminal_inputs(self, parent):
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(pady=10, fill="x")

        # Campos de entrada para terminal inteligente
        labels = [
            "Palabra Inicial:", "Palabra a Convertir:", "Costo Advance:", 
            "Costo Delete:", "Costo Replace:", "Costo Insert:", "Costo Kill:"
        ]
        default_values = ["", "", "", "", "", "", ""]
        self.terminal_vars = [ctk.StringVar(value=val) for val in default_values]

        for i, label in enumerate(labels):
            ctk.CTkLabel(input_frame, text=label).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkEntry(input_frame, textvariable=self.terminal_vars[i]).grid(row=i, column=1, padx=10, pady=5)

    # Botones de la pestaña Terminal
    def create_terminal_buttons(self, parent):
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(pady=20)

        ctk.CTkButton(button_frame, text="Fuerza Bruta", command=self.run_fuerza_bruta_terminal).grid(row=0, column=0, padx=10)
        ctk.CTkButton(button_frame, text="Dinámica", command=self.run_dinamica_terminal).grid(row=0, column=1, padx=10)
        ctk.CTkButton(button_frame, text="Voraz", command=self.run_voraz_terminal).grid(row=0, column=2, padx=10)

    # Resultados de la pestaña Terminal
    def create_terminal_results(self, parent):
        result_frame = ctk.CTkFrame(parent)
        result_frame.pack(pady=10, fill="x")

        self.resultado_terminal = ctk.StringVar()
        ctk.CTkLabel(result_frame, text="Resultado:").pack(pady=5)
        ctk.CTkLabel(result_frame, textvariable=self.resultado_terminal).pack(pady=5)

    # Entradas de datos en la pestaña Subasta
    def create_inputs(self, parent):
        """Crea las entradas de datos en el contenedor."""
        input_frame = ctk.CTkFrame(parent)
        input_frame.pack(pady=10, fill="x")

        labels = ["Total de Acciones (A):", "Precio Mínimo por Acción (B):", "Cantidad de Oferentes:"]
        variables = [self.total_acciones, self.precio_minimo, ctk.StringVar(value="")]

        for i, label in enumerate(labels):
            ctk.CTkLabel(input_frame, text=label).grid(row=i, column=0, padx=10, pady=5)
            ctk.CTkEntry(input_frame, textvariable=variables[i]).grid(row=i, column=1, padx=10, pady=5)

        self.num_oferentes_var = variables[2]
        ctk.CTkButton(input_frame, text="Añadir Oferentes", command=self.add_oferentes).grid(row=3, column=1, pady=10)
        self.oferentes_frame = ctk.CTkFrame(input_frame)
        self.oferentes_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

    def add_oferentes(self):
        """Añade entradas dinámicas para los oferentes."""
        for widget in self.oferentes_frame.winfo_children():
            widget.destroy()

        try:
            num_oferentes = int(self.num_oferentes_var.get())
            if num_oferentes <= 0:
                raise ValueError("El número de oferentes debe ser mayor que cero.")
        except ValueError:
            self.resultado_texto.set("Error: Ingrese un número válido de oferentes.")
            return

        self.oferentes_list = []
        for i in range(num_oferentes):
            oferente_frame = ctk.CTkFrame(self.oferentes_frame)
            oferente_frame.pack(pady=5, fill="x")

            pi_var, mi_var, Mi_var = ctk.StringVar(), ctk.StringVar(), ctk.StringVar()
            ctk.CTkLabel(oferente_frame, text="Costo acción:").grid(row=0, column=0, padx=5)
            ctk.CTkEntry(oferente_frame, textvariable=pi_var, width=50).grid(row=0, column=1, padx=5)
            ctk.CTkLabel(oferente_frame, text="Mínimo:").grid(row=0, column=2, padx=5)
            ctk.CTkEntry(oferente_frame, textvariable=mi_var, width=50).grid(row=0, column=3, padx=5)
            ctk.CTkLabel(oferente_frame, text="Máximo:").grid(row=0, column=4, padx=5)
            ctk.CTkEntry(oferente_frame, textvariable=Mi_var, width=50).grid(row=0, column=5, padx=5)

            self.oferentes_list.append((pi_var, mi_var, Mi_var))

    # Botones para los métodos
    def create_method_selector(self, parent):
        """Crea los botones de selección de método."""
        selector_frame = ctk.CTkFrame(parent)
        selector_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(selector_frame, text="Seleccione el Método:").pack(pady=5, anchor="center")
        buttons_frame = ctk.CTkFrame(selector_frame)
        buttons_frame.pack(pady=5)

        ctk.CTkButton(buttons_frame, text="Dinámica", command=self.run_dinamica).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Fuerza Bruta", command=self.run_fuerza_bruta).pack(side="left", padx=5)
        ctk.CTkButton(buttons_frame, text="Voraz", command=self.run_voraz).pack(side="left", padx=5)

    # Mostrar resultados
    def create_result_display(self, parent):
        """Muestra el resultado de la operación."""
        result_frame = ctk.CTkFrame(parent)
        result_frame.pack(pady=10, fill="x")

        ctk.CTkLabel(result_frame, text="Resultado:").pack(pady=5)
        ctk.CTkLabel(result_frame, textvariable=self.resultado_texto).pack(pady=5)

    # Métodos de subasta
    def run_dinamica(self):
        A = int(self.total_acciones.get())
        B = int(self.precio_minimo.get())
        oferentes = [(int(pi.get()), int(mi.get()), int(Mi.get())) for pi, mi, Mi in self.oferentes_list]
        
        combinacion, acciones_gob, max_ingreso = generar_combinacionesDP(A, oferentes, B)
        self.resultado_texto.set(f"Dinámica:\nCombinación: {combinacion}\nIngreso Máximo: {max_ingreso}")

    def run_fuerza_bruta(self):
        A, B, oferentes = self.get_input_data()
        gobierno = (B, 0, A)
        combinacion, max_ingreso = generar_combinaciones(A, oferentes, B, gobierno)
        self.resultado_texto.set(f"Fuerza Bruta:\nCombinación: {combinacion}\nIngreso Máximo: {max_ingreso}")

    def run_voraz(self):
        A, B, oferentes = self.get_input_data()
        gobierno = (B, 0, A)
        asignacion = asignar_acciones(A, oferentes)
        valor = calcular_valor(asignacion, oferentes, gobierno, A)
        self.resultado_texto.set(f"Voraz:\nCombinación: {asignacion}\nIngreso Máximo: {valor}")

    def get_input_data(self):
        """Obtiene y valida los datos ingresados."""
        A = int(self.total_acciones.get())
        B = int(self.precio_minimo.get())
        oferentes = [(int(pi.get()), int(mi.get()), int(Mi.get())) for pi, mi, Mi in self.oferentes_list]
        return A, B, oferentes

    # Métodos del terminal inteligente
    def run_fuerza_bruta_terminal(self):
        start_time = time.time()
        
        try:
            # Obtén las palabras inicial y objetivo
            word1 = list(self.terminal_vars[0].get())
            word2 = list(self.terminal_vars[1].get())

            # Obtén los costos de las operaciones
            try:
                advance_Cost = int(self.terminal_vars[2].get())
                delete_Cost = int(self.terminal_vars[3].get())
                replace_Cost = int(self.terminal_vars[4].get())
                insert_Cost = int(self.terminal_vars[5].get())
                kill_Cost = int(self.terminal_vars[6].get())
            except ValueError:
                self.resultado_terminal.set("Error: Verifica que todos los costos sean números enteros válidos.")
                return

            # Ejecuta la transformación de fuerza bruta
            resultados = calcular_mejor_coste(word1, word2, 0, 0, advance_Cost, delete_Cost, replace_Cost, insert_Cost, kill_Cost, [], [])
            mejor_resultado = tupla_con_menor_suma(resultados)

            # Muestra el resultado en el campo de texto de la terminal
            resultado = f"Mejor Coste: {sum(mejor_resultado[0])}\nOperaciones: {' -> '.join(mejor_resultado[1])}"
            self.resultado_terminal.set(resultado)
        except Exception as e:
            self.resultado_terminal.set(f"Error: {str(e)}")
        # Código cuya duración quieres medir
        for i in range(1000000):
            _ = i * i  # Operación de ejemplo
        end_time = time.time()
    	# Calcula el tiempo transcurrido
        execution_time = end_time - start_time
        print(f"El código tomó {execution_time:.6f} segundos en ejecutarse.")
            



    def run_dinamica_terminal(self):
        try:
            # Obtén las palabras inicial y objetivo
            cadena_inicial = self.terminal_vars[0].get()
            cadena_destino = self.terminal_vars[1].get()
    
            # Obtén los costos de las operaciones
            costo_avanzar = int(self.terminal_vars[2].get())
            costo_borrar = int(self.terminal_vars[3].get())
            costo_reemplazar = int(self.terminal_vars[4].get())
            costo_insertar = int(self.terminal_vars[5].get())
            costo_reemplazo_total = int(self.terminal_vars[6].get())
    
            # Llama a la función dinámica para calcular el costo mínimo
            costo_final, pasos_transformacion = costo_min_din(
                cadena_inicial, cadena_destino,
                costo_insertar, costo_borrar,
                costo_reemplazar, costo_avanzar,
                costo_reemplazo_total
            )
    
            # Prepara el resultado para mostrar
            resultado = f"Costo mínimo: {costo_final}\nSecuencia de operaciones:\n"
            for paso in pasos_transformacion:
                estado, operacion = paso
                resultado += f"{estado:<15} -> {operacion}\n"
    
            # Mostrar el resultado en la interfaz
            self.resultado_terminal.set(resultado)
    
        except ValueError:
            self.resultado_terminal.set("Error: Verifica que todos los costos sean números válidos.")
        except Exception as e:
            self.resultado_terminal.set(f"Error inesperado: {str(e)}")
    


    def run_voraz_terminal(self):
        # Obtén las palabras inicial y objetivo
        source = self.terminal_vars[0].get()
        objetivo = self.terminal_vars[1].get()

        # Obtén los costos de las operaciones
        try:
            costos = {
                'advance': int(self.terminal_vars[2].get()),
                'delete': int(self.terminal_vars[3].get()),
                'replace': int(self.terminal_vars[4].get()),
                'insert': int(self.terminal_vars[5].get()),
                'kill': int(self.terminal_vars[6].get())
            }
        except ValueError:
            self.resultado_terminal.set("Error: Verifica que todos los costos sean números enteros válidos.")
            return
        # Ejecuta la transformación voraz
        try:
            transformer = interfaz_voraz(source, objetivo, costos)
            min_cost, steps = transformer.transform()
            resultado = f"Costo mínimo: {min_cost}\nPasos:\n" + "\n".join(
                f"{estado:<15} -> {operacion}" for estado, operacion in steps
            )
            self.resultado_terminal.set(resultado)
        except Exception as e:
            self.resultado_terminal.set(f"Error en el cálculo: {e}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    
