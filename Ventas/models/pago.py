class Pago:
    def __init__(self, id_pago=None, id_venta=None, fecha="", monto=0.0, metodo_pago=""):
        self.id_pago = id_pago
        self.id_venta = id_venta
        self.fecha = fecha
        self.monto = monto
        self.metodo_pago = metodo_pago