class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")  # Cambié esto

        # Inicializa carrito vacío si no existe
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
        else:
            self.carrito = carrito

    def obtener_cantidad(self, producto):
        # Devuelve la cantidad actual de un producto en el carrito
        producto_id = str(producto.id)
        if producto_id in self.carrito:
            return self.carrito[producto_id]['cantidad']
        return 0


    def agregar_carrito(self, producto):
        id = str(producto.id)
        if id not in self.carrito.keys():
            if producto.stock > 0:
                self.carrito[id] = {
                    "producto_id": producto.id,
                    "nombre": producto.nombre,
                    "categoria": producto.categoria,
                    "descripcion": producto.descripcion,
                    "precio": str(producto.precio),
                    "imagen": producto.imagen.url,
                    "cantidad": 1,
                }
                self.guardar_carrito()
            else:
                print("El producto está agotado.")
        else:
            if producto.stock > self.carrito[id]['cantidad']:
                self.carrito[id]['cantidad'] += 1
                self.guardar_carrito()
            else:
                print("No hay suficiente stock para agregar más.")

    # Asegúrate de definir estos métodos correctamente en tu Carrito
    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True



    def eliminar(self, producto):
        id = str(producto.id)
        if id in self.carrito:
            del self.carrito[id]
            self.guardar_carrito()

    def restar(self, producto):
        for key, value in self.carrito.items():
            if key ==str(producto.id):
                value["cantidad"] = value["cantidad"] - 1
                if value["cantidad"] < 1:
                    self.eliminar(producto)
                else:
                    self.guardar_carrito()
                break
            else:
                print("El Producto no existe en el carrito.")

    def obtener_total(self):
        total = 0
        for key, value in self.carrito.items():
            total += float(value["precio"]) * value["cantidad"]
        return total

    def sumar(self, producto):
        for key, value in self.carrito.items():
            if key == str(producto.id):
                value["cantidad"] += 1  # Incrementar la cantidad en 1
                self.guardar_carrito()  # Guardar los cambios en la sesión
                break
        else:
            print("El Producto no existe en el carrito.")
            

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True


   

    