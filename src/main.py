
meals = ["Pizza familiar",
         "Hamburguesa doble", "Hamburguesa triple",  "Pizza personal", "Pollo frito", "Papas fritas", "Arroz con menestra y carne",  "Taco de pollo",
         "Salchipapa", "Papipollo", "Ratatouille", "Camarón al ajillo"]
prices = [20, 8.50, 11, 9, 7, 3, 5, 8,5, 3, 40, 35]

topic = ["Italian food", "American food", "American food", "Italian food", "American food", "American food",
            "Ecuadorian food", "Mexican food", "Ecuadorian food", "Ecuadorian food", "Especial food", "Especial food"]

special_meal_ctg = ["Especial food"]

# {"papas": 12uni., "hambuerguesa": 20uni}
client_order = {}


def get_meal_price(meal: str) -> float:
    i_price = meals.index(meal)
    return prices[i_price]


def get_total_meals_qty(client_order: dict) -> int:
    total_meals_qty = 0

    for meal_qty in client_order.values():
        total_meals_qty += meal_qty

    return total_meals_qty


def calc_meal_total_cost(meal: str, meal_qty: int) -> float:
    meal_total_cost = get_meal_price(meal) * meal_qty
    return meal_total_cost


def calc_base_total_cost(client_order: dict) -> float:
    total_cost = 0

    for meal, meal_qty in client_order.items():
        total_cost += calc_meal_total_cost(meal, meal_qty)

    return total_cost


def calc_qty_discount(client_order: dict, total_cost) -> float:
    qty_discount = 0

    total_meals_qty = get_total_meals_qty(client_order)

    if total_meals_qty > 5 and total_meals_qty < 10:
        qty_discount = total_cost * 0.10
    elif total_meals_qty >= 10:
        qty_discount = total_cost * 0.20

    return qty_discount


def calc_special_discount(client_order: dict) -> float:
    special_discount = 0

    for meal, meal_qty in client_order.items():
        meal_total_cost = calc_meal_total_cost(meal, meal_qty)

        if meal_total_cost > 50 and meal_total_cost <= 100:
            special_discount += 10
        elif meal_total_cost > 100:
            special_discount += 25

    return special_discount

def calc_final_total_cost(client_order: dict) -> float:
    base_total_cost = calc_base_total_cost(client_order)
    print("Costo total base: ", base_total_cost)
    qty_discount = calc_qty_discount(client_order, base_total_cost)
    print("Descuento por cantidad: ", qty_discount)
    special_discount = calc_special_discount(client_order)
    print("Descuento especial: ", special_discount)
    final_total_cost = base_total_cost - qty_discount - special_discount

    return final_total_cost

def calc_meal_surcharge(meal):
    meal_surcharge = 0

    if meal in special_meal_ctg:
        meal_surcharge = calc_meal_total_cost * 0.05

    return meal_surcharge

def validate_meal(meal):
    if(meal > len(meals)-1 or meal < -1):
        raise ValueError("ERROR: La comida no existe!")
    
def validate_amount(client_order):
    total_amount = 0
    for amount in client_order.values():
        total_amount += amount
    if (total_amount > 100):
        client_order.popitem()
        raise ValueError("ERROR: La cantidad de las órdenes debe ser menor a 100. La cantidad que tiene es: " + str(total_amount))

def validate_qty(meal_qty):
    if meal_qty < 0:
        client_order.popitem()
        raise ValueError("ERROR: La cantidad debe ser positiva!")
    if meal_qty > 100:
        client_order.popitem()
        raise ValueError("ERROR: La cantidad de las órdenes debe ser menor a 100")

def print_order(client_order):
    print("\n-----ORDEN DEL CLIENTE-----")
    print("Cantidad | Plato")
    for meals, amount in client_order.items():
        print(amount, "\t", meals)


def print_menu():
   print("\n=== MENU ===\n")
   for i in range(len(meals)):
    print(f"{i}. {meals[i]}: ${prices[i]}")
   print("-1. Finalizar orden")
   
def confirmation_user():
    opt = ["Confirmar", "Cancelar y realizar cambios"]
    print("\n=== CONFIRMACIÓN ===\n")
    for i in range(len(opt)):
        print(f"{i+1}. {opt[i]}")
    return int(input("Seleccione una opción: "))

def handler_confirmation(option,order_client):
    if option == 1:
        print("\n¡Su pedido ha sido confirmado!\n")
        print(
            f"Total a pagar: {calc_final_total_cost(client_order)}")
    elif option == 2:
        order_client = {}
        print("\nSu pedido ha sido cancelado\n")
        print("Elija el plato que desea cambiar")
    else:
        raise ValueError("ERROR: Opción inválida")

if __name__ == '__main__':
    i_meal = 0
    while i_meal != -1:
        print_menu()
        while True:
            try:
                i_meal = int(input("\nSelecione su comida: "))
                validate_meal(i_meal)
            except ValueError as e:
                print(e)
            else:
                break
        while True:
            try:
                if (i_meal != -1):
                    selected_meal = meals[i_meal]
                    meal_qty = int(
                        input("Ingrese cantidad deseada (max. 100): "))
                    if selected_meal not in client_order:
                        client_order[selected_meal] = 0

                    client_order[selected_meal] += meal_qty
                    validate_qty(meal_qty)
                    validate_amount(client_order)
            except ValueError as e:
                print(e)
            else:
                break

        print_order(client_order)
        print(
            f"Costo final: {calc_final_total_cost(client_order)}")

    while True:
        try:
            opt = confirmation_user()
            handler_confirmation(opt,client_order)
        except ValueError as e:
            print(e)
        else:
            break
    

