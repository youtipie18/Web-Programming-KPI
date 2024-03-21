# Імпортуємо необхідні бібліотеки
import json


# Метод, щоб знайти найближчі межі до числа у списку(Використовуємо при пошуці Кв)
def find_nearest_neighbors(lst, target):
    closest_lower = max(filter(lambda x: x < target, lst), default=None)
    closest_higher = min(filter(lambda x: x > target, lst), default=None)
    return closest_lower, closest_higher


# Метод для пошуку значення розрахункових коефіцієнтів Кр
# для мереж живлення напругою до 1000 В (Т0 = 10 хв.)
def get_Kp_1(ne, group_use_coff):
    # Відкриваємо json файл, у якому зберігаються дані таблиці 3.3
    with open("instance/prac_3_data_1.json", "r") as file:
        data = json.load(file)
        row = data.get(str(ne), None)

        # Шукаємо найлижчий коефіцієнт використання
        coff_keys = map(float, data["1"].keys())
        closest_coff = str(max(num for num in coff_keys if num <= group_use_coff))

        # Якщо ne є у таблиці, то далі просто підставляємо
        if row:
            Kp = row.get(closest_coff)
            if Kp:
                return Kp
            else:
                return None
        # Якщо ne відсутнє у таблиці, то шукаємо числа, які межують з ним та є у таблиці
        else:
            neighbors = find_nearest_neighbors(list(map(int, data.keys())), ne)
            if neighbors:
                # Шукаємо значення в точках "сусідах"
                lower = data.get(str(neighbors[0])).get(closest_coff)
                higher = data.get(str(neighbors[1])).get(closest_coff)
                if higher and lower:
                    # За допомогою лінійної інтерполяції шукаємо значення в точці ne
                    slope = (higher - lower) / (neighbors[1] - neighbors[0])
                    value = lower + slope * (ne - neighbors[0])
                    return value
                else:
                    return None
            else:
                return None


# Допоміжний метод, для отримання результатів з списку результатів при рендері html сторінці
def get_result_by_index(key, ind, results):
    # Суть метода - вернути ???, якщо значення відсутнє, тобто,
    # якщо сторінка тільки завантажилась і користувач не натискав кнопку "розрахувати"
    result = results.get(key, "???")
    if result != "???":
        return result[ind]
    else:
        return result


# Метод для пошуку значення розрахункових коефіцієнтів Кр на шинах низької
# напруги цехових трансформаторів і магістральних шинопроводів (Т0 = 2,5 год.)
def get_Kp_2(ne, group_use_coff):
    # Відкриваємо json файл, у якому зберігаються дані таблиці 3.4
    with open("instance/prac_3_data_2.json", "r") as file:
        data = json.load(file)
        # Ітеруємся по кожному діапазоні (У таблиці є одиничні значення як для 1, 2, 3, 4,
        # так і задані у вигляді 6-9. Значення 1 та подібні вважаємо діапазоном (1; 1)
        for key in data.keys():
            # Парсимо діапазон. Наприклад записно діапазон "6;9" перетвориться у список [6; 9]
            r = list(map(int, key.split(";")))
            if r[0] <= ne <= r[1]:
                # Шукаємо найлижчий коефіцієнт використання, як і в попередній таблиці
                coff_keys = map(float, data.get(key).keys())
                closest_coff = str(max(num for num in coff_keys if num <= group_use_coff))
                return data.get(key).get(closest_coff)
        return None


# Метод, який парсить числа з плаваючою точкою
# (Зроблено для того, щоб легко можна було перетворити користувацький ввід)
def custom_float(str_float: str):
    return float(str_float.replace(",", "."))
