
comidas = ["Pizza familiar",
           "Hamburguesa doble", "Hamburguesa triple",  "Pizza personal", "Pollo frito", "Papas fritas", "Papas fritas", "Arroz con menestra y carne",  "Taco de pollo"
           "Salchipapa", "Papipollo"]
precios = [20, 8.50, 11, 9, 7, 3, 5, 8, 3, 4]


comidas_cliente = []
cantidades_cliente = []


def obtener_precio_comida(comida):
    pos_precio = comidas.index(comida)
    return precios[pos_precio]


def calcular_costo_inicial(comidas_cliente, cantidades_cliente) -> float:
    costo_total = 0
    for i in range(len(comidas_cliente)):
        costo_total += cantidades_cliente[i] * \
            obtener_precio_comida(comidas_cliente[i])

    return costo_total


def calcular_costo(comidas_cliente, cantidades_cliente) -> float:
    cantidad_total = sum(cantidades_cliente)
    costo_inicial = calcular_costo_inicial(comidas_cliente, cantidades_cliente)
    costo_final = costo_inicial

    if cantidad_total > 5 and cantidad_total < 10:
        costo_final = costo_final * 0, 90
    elif cantidad_total >= 10:
        costo_final = costo_final * 0, 80

    return costo_final

def calcular_descuento_especial(costo_total):
    if costo_total > 50 and costo_total <= 100:
        costo_total -= 10
    elif costo_total > 100:
        costo_total -= 25
        
    return costo_total
        
def validar_cantidad(cantidad):
    if cantidad < 0:
        raise ValueError("ERROR: La cantidad debe ser positiva!")


if __name__ == '__main__':
    pos_comida = 0

    while pos_comida != -1:
        print(
            """
=====================
MENU
=====================
"""
        )
        for i in range(len(comidas)):
            print(f"{i}. {comidas[i]}: ${precios[i]}")
        print("-1. Salir")

        pos_comida = int(input("\nSelecione su comida: "))

        while True:
            try:
                if (pos_comida != -1):
                    cantidad = int(
                        input("Ingrese cantidad deseada (max. 100): "))
                validar_cantidad(cantidad)
            except ValueError as e:
                print(e)
            else:
                break

        if comidas[pos_comida] not in comidas_cliente:
            comidas_cliente.append(comidas[pos_comida])
            cantidades_cliente.append(0)

        i_cantidad = comidas_cliente.index(comidas[pos_comida])
        cantidades_cliente[i_cantidad] += cantidad

       
        print(comidas_cliente)
        print(cantidades_cliente)
        print(
            f"Costo final: {calcular_costo(comidas_cliente, cantidades_cliente)}")

