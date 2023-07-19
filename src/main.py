
meals = ["Pizza familiar",
         "Hamburguesa doble", "Hamburguesa triple",  "Pizza personal", "Pollo frito", "Papas fritas", "Arroz con menestra y carne",  "Taco de pollo"
         "Salchipapa", "Papipollo", "Ratatouille", "Camarón al ajillo"]
prices = [20, 8.50, 11, 9, 7, 3, 5, 8, 3, 4]
category = ["Italian food", "American food", "American food", "Italian food", "American food", "American food",
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


def calc_meal_surcharge(meal):
    meal_surcharge = 0

    if meal in special_meal_ctg:
        meal_surcharge = calc_meal_total_cost * 0.05

    return meal_surcharge

def validate_amount(client_order):
    total_amount = 0
    for amount in client_order.values():
        total_amount += amount
    if total_amount < 0:
        client_order.pop_item()
        raise ValueError("ERROR: La cantidad debe ser positiva!")
    if (total_amount > 100):
        client_order.pop_item()
        raise ValueError("ERROR: La cantidad debe ser menor a 100!")


def print_order(client_order):
    print("\n-----ORDEN DEL CLIENTE-----")
    print("Cantidad | Plato")
    for meals, amount in client_order.items():
        print(amount, " ", meals)


def print_menu():
    pass


if __name__ == '_main_':
    i_meal = 0
    while i_meal != -1:
        print("=== MENU ===")

        for i in range(len(meals)):
            print(f"{i}. {meals[i]}: ${prices[i]}")
        print("-1. Salir")

        i_meal = int(input("\nSelecione su comida: "))

        while True:
            try:
                if (i_meal != -1):
                    meal_qty = int(
                        input("Ingrese cantidad deseada (max. 100): "))
                selected_meal = meals[i_meal]

                if selected_meal not in client_order:
                    client_order[selected_meal] = 0

                client_order[selected_meal] += meal_qty
                validate_amount(client_order)
            except ValueError as e:
                print(e)
            else:
                break

        # selected_meal = meals[i_meal]

        # if selected_meal not in client_order:
        #     client_order[selected_meal] = 0

        # client_order[selected_meal] += meal_qty

        # print(client_meals)
        # print(cantidades_cliente)
        print_order(client_order)
       # print(
        #  f"Costo final: {calc_cost(client_meals, cantidades_cliente)}")
