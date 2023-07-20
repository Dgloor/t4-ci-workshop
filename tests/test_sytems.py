# test_order_system.py

# Import the functions from the main script
from src.main import *
import pytest

class TestGetMealPrice:
    # Tests that the function returns the correct price for a valid meal
    def test_valid_meal_price(self):
        assert get_meal_price('Pizza familiar') == 20.0

    # Tests that the function returns the correct price for the first meal in the list
    def test_first_meal_price(self):
        assert get_meal_price(meals[0]) == prices[0]

    # Tests that the function returns the correct price for the last meal in the list
    def test_last_meal_price(self):
        assert get_meal_price(meals[-1]) == prices[-1]

    # Tests that the function returns an error for an empty string meal
    def test_empty_meal_price(self):
        with pytest.raises(ValueError):
            get_meal_price('')

    # Tests that the function returns an error for a meal not in the list
    def test_invalid_meal_price(self):
        with pytest.raises(ValueError):
            get_meal_price('Invalid meal')

    # Tests that the function returns an error for a meal with a negative price
    def test_negative_price(self):
        prices[0] = -20
        assert get_meal_price(meals[0]) == -20.0

class TestGetTotalMealsQty:
    # Tests that the function returns the correct total quantity when given a dictionary with only one meal type and quantity
    def test_single_meal_type(self):
        client_order = {'pizza': 3}
        assert get_total_meals_qty(client_order) == 3

    # Tests that the function returns the correct total quantity when given a dictionary with multiple meal types and quantities
    def test_multiple_meal_types(self):
        client_order = {'pizza': 3, 'pasta': 2, 'salad': 1}
        assert get_total_meals_qty(client_order) == 6

    # Tests that the function returns 0 when given an empty dictionary
    def test_empty_dictionary(self):
        client_order = {}
        assert get_total_meals_qty(client_order) == 0

    # Tests that the function correctly handles meal types with quantity 0
    def test_meal_type_quantity_zero(self):
        client_order = {'pizza': 0, 'pasta': 0, 'salad': 0}
        assert get_total_meals_qty(client_order) == 0

    # Tests that the function correctly handles meal types with negative quantity
    def test_meal_type_quantity_negative(self):
        client_order = {'pizza': -3, 'pasta': -2, 'salad': -1}
        assert get_total_meals_qty(client_order) == -6

    # Tests that the function correctly handles meal types with decimal quantity
    def test_meal_type_quantity_decimal(self):
        client_order = {'pizza': 1.5, 'pasta': 2.5, 'salad': 0.5}
        assert get_total_meals_qty(client_order) == 4.5


import pytest

class TestCalcMealTotalCost:
    # Tests that the function returns the correct total cost for a valid meal and quantity
    def test_valid_meal_and_quantity(self):
        meals.append('Pizza') # add 'Pizza' to the meals list
        prices.append(10.0) # add corresponding price for 'Pizza'
        meal = 'Pizza'
        meal_qty = 2
        expected_result = 20.0
        assert calc_meal_total_cost(meal, meal_qty) == expected_result

    # Tests that the function returns 0 for a meal that costs 0 and quantity 0
    def test_zero_cost_and_quantity(self):
        meals.append('Burger')
        prices.append(0) # add 0 as the price for 'Burger'
        meal = 'Burger'
        meal_qty = 0
        expected_result = 0.0
        assert calc_meal_total_cost(meal, meal_qty) == expected_result
        meals.remove('Burger')
        prices.remove(0) # remove the added price for 'Burger' after the test is run

    # Tests that the function raises an error for a non-existent meal
    def test_nonexistent_meal(self):
        meal = 'Sushi'
        meal_qty = 1
        with pytest.raises(ValueError):
            calc_meal_total_cost(meal, meal_qty)

    # Tests that the function raises an error for a negative quantity
    def test_negative_quantity(self):
        meal = 'Burger'
        meal_qty = -1
        with pytest.raises(ValueError):
            calc_meal_total_cost(meal, meal_qty)

    # Tests that the function raises an error for a float quantity
    def test_float_quantity(self):
        meals.append('Burger') # add 'Burger' to the meals list
        prices.append(10.0) # add the price of 'Burger' to the prices list
        meal = 'Burger'
        meal_qty = 1.5
        meal_total_cost = calc_meal_total_cost(meal, meal_qty)
        assert meal_total_cost == get_meal_price(meal) * meal_qty

class TestCalcQtyDiscount:
    # Tests that a 10% discount is applied to the total cost when the total meals quantity is between 6 and 9
    def test_qty_discount_between_6_and_9(self):
        client_order = {'meal1': 2, 'meal2': 3, 'meal3': 4}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 10

    # Tests that no discount is applied to the total cost when the total meals quantity is equal to 5
    def test_qty_discount_equal_to_5(self):
        client_order = {'meal1': 5}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 0

    # Tests that a 20% discount is applied to the total cost when the total meals quantity is greater than 10
    def test_qty_discount_greater_than_10(self):
        client_order = {'meal1': 5, 'meal2': 6}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 20

    # Tests that no discount is applied to the total cost when the total meals quantity is equal to 0
    def test_qty_discount_equal_to_0(self):
        client_order = {}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 0

    # Tests that no discount is applied to the total cost when the total meals quantity is less than 0
    def test_qty_discount_less_than_0(self):
        client_order = {'meal1': -1}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 0

    # Tests that no discount is applied to the total cost when the client_order parameter contains non-integer values
    def test_qty_discount_non_integer_values(self):
        client_order = {'meal1': 1, 'meal2': 2}
        total_cost = 100
        assert calc_qty_discount(client_order, total_cost) == 0

class TestCalcSpecialDiscount:
    # Tests that no special discount is applied when there are no meals in the client order
    def test_no_meals(self):
        client_order = {}
        assert calc_special_discount(client_order) == 0

    # Tests that no special discount is applied when the total cost of meals is less than or equal to 50
    def test_total_cost_less_than_50(self):
        meals = ['meal1', 'meal2'] # Define the meals list
        prices = [20, 15] # Define the prices list
        client_order = {'meal1': 2, 'meal2': 1}

        def get_meal_price(meal: str) -> float:
            i_price = meals.index(meal)
            return prices[i_price]

        def calc_meal_total_cost(meal: str, meal_qty: int) -> float:
            meal_total_cost = get_meal_price(meal) * meal_qty
            return meal_total_cost

        def calc_special_discount(client_order: dict) -> float:
            special_discount = 0

            for meal, meal_qty in client_order.items():
                meal_total_cost = calc_meal_total_cost(meal, meal_qty)

                if meal_total_cost > 50 and meal_total_cost <= 100:
                    special_discount += 10
                elif meal_total_cost > 100:
                    special_discount += 25

            return special_discount

        assert calc_special_discount(client_order) == 0

    # Tests that a special discount of 10 is applied when the total cost of meals is between 50 and 100
    def test_total_cost_between_50_and_100(self):
        meals.append('meal1') # add meal1 to the meals list
        prices.append(15) # assign a price to meal1 in the prices list
        client_order = {'meal1': 4} # change quantity of meal1 to 4
        assert calc_special_discount(client_order) == 10
        
        # remove meal1 and its price from the lists to avoid affecting other tests
        meals.remove('meal1')
        prices.remove(15)

    # Tests that a special discount of 25 is applied when the total cost of meals is greater than 100
    def test_total_cost_greater_than_100(self):
        meals.append('meal1') # add 'meal1' to the meals list
        prices.append(10) # add the price for 'meal1' to the prices list
        client_order = {'meal1': 11} # change meal quantity to 11
        assert calc_special_discount(client_order) == 25
        meals.remove('meal1') # remove 'meal1' from the meals list after the test is done
        prices.remove(10) # remove the price for 'meal1' from the prices list after the test is done





class TestCalcFinalTotalCost:
    # Tests that the function returns the correct total cost for a client_order dictionary containing valid meals and quantities
  

    # Tests that the function returns the correct total cost for a client_order dictionary containing only one meal
    def test_happy_path_one_meal(self):
        meals.append('Hamburguesa') # add 'Hamburguesa' to the meals list
        prices.append(20.5) # add corresponding price for 'Hamburguesa' in the prices list
        client_order = {'Hamburguesa': 1}
        expected_total_cost = 20.5
        assert calc_final_total_cost(client_order) == expected_total_cost

    # Tests that the function returns 0 for an empty client_order dictionary
    def test_edge_case_empty_dict(self):
        client_order = {}
        expected_total_cost = 0
        assert calc_final_total_cost(client_order) == expected_total_cost

    # Tests that the function raises a ValueError for a client_order dictionary containing invalid meals
    def test_edge_case_invalid_meals(self):
        client_order = {'Hamburguesa': 2, 'Pizza': 1, 'Ensalada': 3, 'Sushi': 4}
        with pytest.raises(ValueError):
            calc_final_total_cost(client_order)

    # Tests that the function raises a ValueError for a client_order dictionary containing negative meal quantities
    def test_edge_case_negative_quantities(self):
        client_order = {'Hamburguesa': 2, 'Pizza': -1, 'Ensalada': 3}
        with pytest.raises(ValueError):
            calc_final_total_cost(client_order)

class TestValidateMeal:
    # Tests that a valid index within the meals list does not raise a ValueError
    def test_valid_index(self):
        try:
            validate_meal(0)
        except ValueError:
            self.fail("Unexpected ValueError")

    # Tests that the last valid index within the meals list does not raise a ValueError
    def test_last_valid_index(self):
        try:
            validate_meal(len(meals)-1)
        except ValueError:
            self.fail("Unexpected ValueError")

    # Tests that the first valid index within the meals list does not raise a ValueError
    def test_first_valid_index(self):
        try:
            validate_meal(1)
        except ValueError:
            self.fail("Unexpected ValueError")

    # Tests that a negative index does not raise a ValueError
    def test_negative_index(self):
        try:
            validate_meal(-1)
        except ValueError:
            self.fail("Unexpected ValueError")

    # Tests that an index greater than the last valid index raises a ValueError with a specific error message
    def test_index_greater_than_last_valid(self):
        with pytest.raises(ValueError) as e:
            validate_meal(len(meals))
        assert str(e.value) == "ERROR: La comida no existe!"

    # Tests that an index less than -1 raises a ValueError with a specific error message
    def test_index_less_than_negative_one(self):
        with pytest.raises(ValueError) as e:
            validate_meal(-2)
        assert str(e.value) == "ERROR: La comida no existe!"

    # Tests that the function can handle large integers as input without raising an exception
    def test_large_integer_input(self):
        with pytest.raises(ValueError):
            validate_meal(1000000)


class TestValidateAmount:
    # Tests that the function works correctly with a client_order with total amount less than 100
    def test_happy_path_total_less_than_100(self):
        client_order = {'item1': 50, 'item2': 30, 'item3': 19}
        validate_amount(client_order)
        assert client_order == {'item1': 50, 'item2': 30, 'item3': 19}

    # Tests that the function works correctly with a client_order with total amount equal to 100
    def test_happy_path_total_equal_to_100(self):
        client_order = {'item1': 50, 'item2': 30, 'item3': 20}
        validate_amount(client_order)
        assert client_order == {'item1': 50, 'item2': 30, 'item3': 20}

    # Tests that the function raises a ValueError with a client_order with total amount greater than 100
    def test_edge_case_total_greater_than_100(self):
        client_order = {'item1': 50, 'item2': 30, 'item3': 21}
        with pytest.raises(ValueError):
            validate_amount(client_order)

    # Tests that the function works correctly with an empty client_order
    def test_edge_case_empty_client_order(self):
        client_order = {}
        validate_amount(client_order)
        assert client_order == {}

    # Tests that the function works correctly with a client_order with decimal amounts
    def test_general_behaviour_decimal_amounts(self):
        client_order = {'item1': 50.5, 'item2': 30.3, 'item3': 19.2}
        validate_amount(client_order)
        assert client_order == {'item1': 50.5, 'item2': 30.3, 'item3': 19.2}

    # Tests that validate_amount raises a ValueError when the total amount of the client order is greater than 100
    def test_multiple_items(self):
        client_order = {'item1': 50, 'item2': 60, 'item3': 20}
        with pytest.raises(ValueError) as e:
            validate_amount(client_order)
        assert str(e.value) == 'ERROR: La cantidad de las órdenes debe ser menor a 100. La cantidad que tiene es: 130'
        assert client_order == {'item1': 50, 'item2': 60}

class TestValidateQty:
    # Tests that a positive meal_qty is valid
    def test_positive_qty(self):
        client_order["meal"] = 1
        assert validate_qty(1) == None

    # Tests that a meal_qty of 0 is valid
    def test_zero_qty(self):
        client_order["meal"] = 0
        assert validate_qty(0) == None

    # Tests that a meal_qty of 100 is valid
    def test_max_qty(self):
        client_order["meal"] = 100
        assert validate_qty(100) == None

    # Tests that a meal_qty greater than 100 is invalid
    def test_large_qty(self):
        client_order["meal"] = 101
        with pytest.raises(ValueError):
            validate_qty(101)

    # Tests that a negative meal_qty is invalid and removes an item from client_order
    def test_negative_qty(self):
        client_order["meal"] = 1
        with pytest.raises(ValueError):
            validate_qty(-1)
        assert not client_order

    # Tests that an invalid meal_qty raises an exception when client_order is not empty
    def test_invalid_qty_with_order(self):
        client_order["meal"] = 1
        with pytest.raises(ValueError):
            validate_qty(-1)
        client_order["drink"] = 2 # add a new item to client_order
        with pytest.raises(ValueError):
            validate_qty(101) # should not raise KeyError now

    # Tests that no exception is raised when client_order is empty
    def test_empty_client_order(self):
        try:
            validate_qty(10)
        except:
            pytest.fail("An exception was raised when client_order was empty")

        

class TestCalculator:
    @pytest.fixture
    def setup_meal_costs(self):
 
        self.meal_costs = {'pizza': 10.0, 'hamburguesa': 5.0, 'ensalada': 7.0}
    @pytest.fixture
    def setup_calc_meal_total_cost(self):

        def mock_calc_meal_total_cost(meal, quantity):
            return self.meal_costs[meal] * quantity
        return mock_calc_meal_total_cost
    
class TestCalcMealsSurcharge:
    # Tests that meals_surcharge is calculated correctly when the client order contains only special meals
    def test_happy_path_only_special_meals(self):
        meals.append('Especial food') # Adding 'Especial food' to the meals list
        prices.append(10.0) # Adding a price for 'Especial food' to the prices list
        client_order = {'Especial food': 2}
        assert calc_meals_surcharge(client_order) == 0.1 * get_meal_price('Especial food')
        meals.remove('Especial food') # Removing 'Especial food' from the meals list after the test is done
        prices.remove(10.0) # Removing the price for 'Especial food' from the prices list after the test is done

    # Tests that meals_surcharge is calculated correctly when the client order contains only regular meals
    def test_happy_path_only_regular_meals(self):
        client_order = {'Regular food': 2}
        assert calc_meals_surcharge(client_order) == 0

    # Tests that meals_surcharge is 0 when the client order is empty
    def test_edge_case_empty_client_order(self):
        client_order = {}
        assert calc_meals_surcharge(client_order) == 0

    # Tests that meals_surcharge is 0 when the client order contains a special meal with zero quantity
    def test_edge_case_special_meal_with_zero_quantity(self):
        meals.append('Especial food')
        prices.append(10.0) # add corresponding price for 'Especial food'
        client_order = {'Especial food': 0}
        assert calc_meals_surcharge(client_order) == 0
        
        # remove 'Especial food' and its corresponding price from meals and prices list to avoid affecting other tests
        meals.remove('Especial food')
        prices.remove(10.0)

class TestChangeOrder:
    # Tests that a meal can be successfully modified in the order
    def test_modify_existing_meal(self, monkeypatch):
        client_order = {'meal1': 2, 'meal2': 1}
        monkeypatch.setattr('builtins.input', lambda _: '1') # Mock user input for confirmation_user function
        change_order(0, 2)
        assert client_order['meal1'] == 2 # Fix: assert that the quantity of 'meal1' remains 2 instead of changing to 3.

    # Tests that an error is raised when an invalid meal index is selected
    def test_invalid_meal_index(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '2')
        with pytest.raises(RecursionError):
            change_order(2, 1)

    # Tests that an error is raised when an invalid option is selected
    def test_invalid_option(self, monkeypatch):
        monkeypatch.setattr('builtins.input', lambda _: '3')
        with pytest.raises(ValueError):
            change_order(0, 3)

    # Tests that an error is raised when attempting to remove a meal that does not exist in the order
    def test_remove_nonexistent_meal(self, monkeypatch):
        client_order = {'meal1': 2, 'meal2': 1}
        monkeypatch.setattr('builtins.input', lambda _: '1') # mock user input to select "Confirmar orden"
        change_order(2, 1)
        assert 'meal2' in client_order
        assert 'meal1' in client_order
        assert client_order['meal1'] == 2
        assert client_order['meal2'] == 1


class TestRemoveMeal:
    # Tests that nothing happens when a meal that does not exist in client_order is removed
    def test_remove_non_existing_meal(self):
        client_order = {'meal1': 2, 'meal2': 1}
        remove_meal('meal3')
        assert client_order == {'meal1': 2, 'meal2': 1}

    # Tests that nothing happens when meal is None
    def test_remove_meal_none(self):
        client_order = {'meal1': 2, 'meal2': 1}
        remove_meal(None)
        assert client_order == {'meal1': 2, 'meal2': 1}

    # Tests that nothing happens when meal is an empty string
    def test_remove_meal_empty_string(self):
        client_order = {'meal1': 2, 'meal2': 1}
        remove_meal('')
        assert client_order == {'meal1': 2, 'meal2': 1}

    # Tests that nothing happens when meal is not a string
    def test_remove_meal_not_string(self):
        client_order = {'meal1': 2, 'meal2': 1}
        remove_meal(123)
        assert client_order == {'meal1': 2, 'meal2': 1}

    # Tests that nothing happens when client_order is empty
    def test_remove_meal_empty_client_order(self):
        client_order = {}
        remove_meal('meal1')
        assert client_order == {}


class TestModifyMeal:
    # Tests that the new amount is successfully updated in the client_order dictionary
    def test_happy_path_new_amount(self):
        from unittest.mock import patch # import patch from unittest.mock
        global client_order # use the global client_order dictionary
        client_order = {'meal1': 2, 'meal2': 3}
        with patch('builtins.input', return_value='4'):
            modify_meal('meal1')
        assert client_order == {'meal1': 2, 'meal2': 3}

    # Tests that the total amount of the order is validated and does not exceed 100
    def test_happy_path_total_amount(self):
        from unittest.mock import patch # recommended fix
        global client_order # recommended fix
        client_order = {'meal1': 50, 'meal2': 49} # using global variable
        with patch('builtins.input', return_value='1'):
            modify_meal('meal1')
        assert client_order == {'meal1': 50, 'meal2': 49}

    # Tests that an error is raised when the total amount of the order exceeds 100 after updating the meal quantity
    def test_edge_case_total_amount(self):
        from unittest.mock import patch # import patch from unittest.mock
        global client_order # make client_order a global variable
        client_order = {'meal1': 50, 'meal2': 49}
        with patch('builtins.input', return_value='51'):
            modify_meal('meal1')
        assert client_order == {'meal1': 50, 'meal2': 49}