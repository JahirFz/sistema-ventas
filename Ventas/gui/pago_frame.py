import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox
from datetime import date

from controllers.venta_controller import listar_ventas
from controllers.pago_controller import (
    agregar_pago,
    listar_pagos_por_venta,
    eliminar_pago,
    obtener_total_pagado,
    obtener_total_venta,
    obtener_saldo_pendiente,
    obtener_estado_venta
)


class PagoFrame(tb.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.id_pago_seleccionado = None
        self.ventas_dict = {}

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.crear_formulario()
        self.crear_resumen()
        self.crear_tabla()
        self.actualizar_datos()
        self.colocar_fecha_hoy()

    def crear_formulario(self):
        contenedor = tb.Frame(self)
        contenedor.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        contenedor.grid_columnconfigure(1, weight=1)

        tb.Label(
            contenedor,
            text="Módulo de pagos",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=8, sticky=W, pady=(0, 15))

        tb.Label(contenedor, text="Venta").grid(row=1, column=0, sticky=W, padx=(0, 10))
        self.combo_ventas = ttk.Combobox(contenedor, state="readonly", width=40)
        self.combo_ventas.grid(row=1, column=1, sticky=W, padx=(0, 10))
        self.combo_ventas.bind("<<ComboboxSelected>>", self.cambio_venta)

        tb.Label(contenedor, text="Fecha").grid(row=1, column=2, sticky=W, padx=(0, 10))
        self.entry_fecha = tb.Entry(contenedor, width=15)
        self.entry_fecha.grid(row=1, column=3, sticky=W, padx=(0, 10))

        tb.Label(contenedor, text="Monto").grid(row=1, column=4, sticky=W, padx=(0, 10))
        self.entry_monto = tb.Entry(contenedor, width=15)
        self.entry_monto.grid(row=1, column=5, sticky=W, padx=(0, 10))

        tb.Label(contenedor, text="Método").grid(row=2, column=0, sticky=W, padx=(0, 10), pady=(10, 0))
        self.entry_metodo = tb.Entry(contenedor, width=20)
        self.entry_metodo.grid(row=2, column=1, sticky=W, padx=(0, 10), pady=(10, 0))

        tb.Button(
            contenedor,
            text="Guardar",
            bootstyle="success",
            command=self.guardar_pago
        ).grid(row=2, column=2, padx=5, pady=(10, 0))

        tb.Button(
            contenedor,
            text="Limpiar",
            bootstyle="secondary",
            command=self.limpiar_formulario
        ).grid(row=2, column=3, padx=5, pady=(10, 0))

    def crear_resumen(self):
        marco = tb.Labelframe(self, text="Resumen de la venta", padding=15, bootstyle="info")
        marco.grid(row=1, column=0, sticky="ew", pady=(0, 15))

        self.lbl_total_venta = tb.Label(marco, text="Total venta: $0.00", font=("Segoe UI", 11, "bold"))
        self.lbl_total_venta.grid(row=0, column=0, sticky=W, padx=10)

        self.lbl_total_pagado = tb.Label(marco, text="Total pagado: $0.00", font=("Segoe UI", 11, "bold"))
        self.lbl_total_pagado.grid(row=0, column=1, sticky=W, padx=10)

        self.lbl_saldo = tb.Label(marco, text="Saldo pendiente: $0.00", font=("Segoe UI", 11, "bold"))
        self.lbl_saldo.grid(row=0, column=2, sticky=W, padx=10)

        #self.lbl_estado = tb.Label(marco, text="Estado: PENDIENTE", font=("Segoe UI", 11, "bold"))
        #self.lbl_estado.grid(row=0, column=3, sticky=W, padx=10)
        self.lbl_estado = tb.Label(
            marco,
            text="Estado: PENDIENTE",
            font=("Segoe UI", 11, "bold"),
            bootstyle="danger"
        )
        self.lbl_estado.grid(row=0, column=3, sticky=W, padx=10)

    def crear_tabla(self):
        marco_tabla = tb.Frame(self)
        marco_tabla.grid(row=2, column=0, sticky="nsew")

        columnas = ("id_pago", "fecha", "monto", "metodo")

        self.tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            height=15
        )

        self.tabla.heading("id_pago", text="ID")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("monto", text="Monto")
        self.tabla.heading("metodo", text="Método")

        self.tabla.column("id_pago", width=80, anchor=CENTER)
        self.tabla.column("fecha", width=120, anchor=CENTER)
        self.tabla.column("monto", width=120, anchor=E)
        self.tabla.column("metodo", width=200, anchor=W)

        scrollbar = ttk.Scrollbar(marco_tabla, orient=VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        marco_tabla.grid_rowconfigure(0, weight=1)
        marco_tabla.grid_columnconfigure(0, weight=1)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_pago)

        botones = tb.Frame(self)
        botones.grid(row=3, column=0, sticky=W, pady=(10, 0))

        tb.Button(
            botones,
            text="Eliminar seleccionado",
            bootstyle="danger",
            command=self.borrar_pago
        ).pack(side=LEFT)

    def actualizar_datos(self):
        self.cargar_ventas()
        self.cargar_pagos_actuales()
        self.actualizar_resumen()

        if self.id_pago_seleccionado is None:
            self.colocar_fecha_hoy()

    def cargar_ventas(self):
        ventas = listar_ventas()

        self.ventas_dict = {}
        valores_combo = []

        seleccion_actual = self.combo_ventas.get().strip()

        for venta in ventas:
            id_venta = venta[0]
            fecha = venta[1]
            cliente = venta[3]
            texto = f"{id_venta} - {cliente} - {fecha}"
            self.ventas_dict[texto] = id_venta
            valores_combo.append(texto)

        self.combo_ventas["values"] = valores_combo

        if seleccion_actual in valores_combo:
            self.combo_ventas.set(seleccion_actual)
        elif valores_combo:
            self.combo_ventas.set(valores_combo[0])

    def obtener_id_venta_actual(self):
        venta_seleccionada = self.combo_ventas.get().strip()
        if venta_seleccionada == "":
            return None
        return self.ventas_dict.get(venta_seleccionada)

    def cargar_pagos_actuales(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        id_venta = self.obtener_id_venta_actual()
        if id_venta is None:
            return

        pagos = listar_pagos_por_venta(id_venta)

        for pago in pagos:
            self.tabla.insert(
                "",
                END,
                values=(
                    pago[0],
                    pago[2],
                    f"${pago[3]:.2f}",
                    pago[4]
                )
            )

    def actualizar_resumen(self):
        id_venta = self.obtener_id_venta_actual()

        if id_venta is None:
            self.lbl_total_venta.config(text="Total venta: $0.00")
            self.lbl_total_pagado.config(text="Total pagado: $0.00")
            self.lbl_saldo.config(text="Saldo pendiente: $0.00")
            self.aplicar_estilo_estado("PENDIENTE")
            return

        total_venta = obtener_total_venta(id_venta) or 0
        total_pagado = obtener_total_pagado(id_venta)
        saldo_pendiente = obtener_saldo_pendiente(id_venta) or 0
        estado = obtener_estado_venta(id_venta) or "PENDIENTE"

        self.lbl_total_venta.config(text=f"Total venta: ${total_venta:.2f}")
        self.lbl_total_pagado.config(text=f"Total pagado: ${total_pagado:.2f}")
        self.lbl_saldo.config(text=f"Saldo pendiente: ${saldo_pendiente:.2f}")
        self.aplicar_estilo_estado(estado)

    def cambio_venta(self, event):
        self.id_pago_seleccionado = None
        self.cargar_pagos_actuales()
        self.actualizar_resumen()

    def guardar_pago(self):
        id_venta = self.obtener_id_venta_actual()
        fecha = self.entry_fecha.get().strip()
        monto = self.entry_monto.get().strip()
        metodo = self.entry_metodo.get().strip()

        if id_venta is None:
            messagebox.showwarning("Aviso", "Selecciona una venta.")
            return

        exito, mensaje = agregar_pago(id_venta, fecha, monto, metodo)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.entry_monto.delete(0, END)
            self.entry_metodo.delete(0, END)
            self.cargar_pagos_actuales()
            self.actualizar_resumen()
        else:
            messagebox.showerror("Error", mensaje)

    def seleccionar_pago(self, event):
        item = self.tabla.selection()
        if not item:
            return

        valores = self.tabla.item(item, "values")
        self.id_pago_seleccionado = int(valores[0])

    def borrar_pago(self):
        if self.id_pago_seleccionado is None:
            messagebox.showwarning("Aviso", "Selecciona un pago primero.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Deseas eliminar este pago?")
        if not confirmar:
            return

        exito, mensaje = eliminar_pago(self.id_pago_seleccionado)

        if exito:
            messagebox.showinfo("Éxito", mensaje)
            self.id_pago_seleccionado = None
            self.cargar_pagos_actuales()
            self.actualizar_resumen()
        else:
            messagebox.showerror("Error", mensaje)

    def limpiar_formulario(self):
        self.id_pago_seleccionado = None
        self.entry_fecha.delete(0, END)
        self.entry_monto.delete(0, END)
        self.entry_metodo.delete(0, END)
        self.tabla.selection_remove(self.tabla.selection())
        self.colocar_fecha_hoy()

    def colocar_fecha_hoy(self):
        hoy = date.today().strftime("%Y-%m-%d")
        self.entry_fecha.delete(0, END)
        self.entry_fecha.insert(0, hoy)
    
    def aplicar_estilo_estado(self, estado):
        if estado == "PAGADA":
            self.lbl_estado.config(text=f"Estado: {estado}", bootstyle="success")
        elif estado == "ABONADA":
            self.lbl_estado.config(text=f"Estado: {estado}", bootstyle="warning")
        else:
            self.lbl_estado.config(text=f"Estado: {estado}", bootstyle="danger")