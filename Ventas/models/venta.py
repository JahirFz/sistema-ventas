class Venta:
    def __init__(self, id_venta=None, fecha="", id_cliente=None, requiere_factura=0, total=0.0):
        self.id_venta = id_venta
        self.fecha = fecha
        self.id_cliente = id_cliente
        self.requiere_factura = requiere_factura
        self.total = total