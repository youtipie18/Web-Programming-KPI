import math
import statistics
from utils import *

from flask import Flask, render_template, abort, request

app = Flask(__name__)
# Налаштування секретного ключа для забезпечення безпеки сесій
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'


# Шлях, що обробляє головну сторінку, з якої можна потрапити на усі веб калькулятори курсу
@app.route("/")
def index():
    # Використовуємо функцію render_template, для відображення html сторінок.
    # Flask використовує систему шаблонізації Jinja2, тому разом з самою html сторінок,
    # можна передати python змінні, що буде продемонстровано далі.
    return render_template("index.html")


# Шлях, що обробляє перше завдання першої практичної роботи
# Оскільки на сторінці присутня форма, для користувацього вводу,
# тому додаємо можливість обробки POST запиту у методі: methods=["POST", "GET"]
@app.route("/prac-1/task-1", methods=["POST", "GET"])
def prac_1_task_1():
    # Перевіряємо який запит було здійснено
    # Якщо GET, то просто відображаємо сторінку для введення вхідних даних
    # Якщо POST, то на цю ж сторінку передаємо результати обрахунків,
    # що будуть відображені на сторінці за допомогою Jinja2
    if request.method == "POST":
        try:
            # Отримання користувацього вводу
            # Також заміняємо ',' на '.' для коректного переведення строки у float
            Hp = float(request.form.get("Hp").replace(",", "."))
            Cp = float(request.form.get("Cp").replace(",", "."))
            Sp = float(request.form.get("Sp").replace(",", "."))
            Np = float(request.form.get("Np").replace(",", "."))
            Op = float(request.form.get("Op").replace(",", "."))
            Wp = float(request.form.get("Wp").replace(",", "."))
            Ap = float(request.form.get("Ap").replace(",", "."))

            # Обчислення результатів

            # Обчислюємо коефіцієнт переходу від робочої до сухої маси та
            # коефіцієнт переходу від робочої до горючої маси
            Kpc = 100 / (100 - Wp)
            Kpg = 100 / (100 - Wp - Ap)

            # Обчислюємо нижчу теплоту згоряння для робочої, сухої та горючої маси
            Qph = (339 * Cp + 1030 * Hp - 108.8 * (Op - Sp) - 25 * Wp) / 1000
            Qch = (Qph + 0.025 * Wp) * 100 / (100 - Wp)
            Qgh = (Qph + 0.025 * Wp) * 100 / (100 - Wp - Ap)

            # Обчислюємо склад сухої маси палива
            Hc = Hp * Kpc
            Cc = Cp * Kpc
            Sc = Sp * Kpc
            Nc = Np * Kpc
            Oc = Op * Kpc
            Ac = Ap * Kpc

            # Обчислюємо склад горючої маси палива
            Hg = Hp * Kpg
            Cg = Cp * Kpg
            Sg = Sp * Kpg
            Ng = Np * Kpg
            Og = Op * Kpg

            # Заносимо результати у словник та округлюємо їх
            results = {
                'Kpc': round(Kpc, 2),
                'Kpg': round(Kpg, 2),
                'Qph': round(Qph, 4),
                'Qch': round(Qch, 4),
                'Qgh': round(Qgh, 4),
                'Hc': round(Hc, 2),
                'Cc': round(Cc, 2),
                'Sc': round(Sc, 2),
                'Nc': round(Nc, 2),
                'Oc': round(Oc, 2),
                'Ac': round(Ac, 2),
                'Hg': round(Hg, 2),
                'Cg': round(Cg, 2),
                'Sg': round(Sg, 2),
                'Ng': round(Ng, 2),
                'Og': round(Og, 2)
            }

        # Якщо в ході обрахунків виникає помилка, то повертаємо статус 400
        # та виводимо помилку
        except Exception as e:
            return abort(400, f"Bad values: {e}")

        # Рендеримо сторінку разом з результатами обрахунків
        return render_template("prac_1_task_1.html", results=results)

    return render_template("prac_1_task_1.html", results=None)


# Шлях, що обробляє друге завдання першої практичної роботи
@app.route("/prac-1/task-2", methods=["POST", "GET"])
def prac_1_task_2():
    if request.method == "POST":
        try:
            # Код для другого завдання схожий:
            # Отримання користувацього вводу
            # Також заміняємо ',' на '.' для коректного переведення строки у float
            Hg = float(request.form.get("Hg").replace(",", "."))
            Cg = float(request.form.get("Cg").replace(",", "."))
            Sg = float(request.form.get("Sg").replace(",", "."))
            Vg = float(request.form.get("Vg").replace(",", "."))
            Og = float(request.form.get("Og").replace(",", "."))
            Wg = float(request.form.get("Wg").replace(",", "."))
            Ag = float(request.form.get("Ag").replace(",", "."))
            Qi = float(request.form.get("Qi").replace(",", "."))

            # Обчислення результатів

            # Обчислюємо склад робочої маси мазуту
            Hp = Hg * (100 - Wg - Ag) / 100
            Cp = Cg * (100 - Wg - Ag) / 100
            Sp = Sg * (100 - Wg - Ag) / 100
            Op = Og * (100 - Wg - Ag) / 100
            Ap = Ag * (100 - Wg) / 100
            Vp = Vg * (100 - Wg) / 100

            # Обчислюємо нижчу теплоту згоряння мазуту на робочу масу
            Qri = Qi * (100 - Wg - Ag) / 100 - 0.025 * Wg

            # Заносимо результати у словник та округлюємо їх
            results = {
                'Hp': round(Hp, 2),
                'Cp': round(Cp, 2),
                'Sp': round(Sp, 2),
                'Op': round(Op, 2),
                'Ap': round(Ap, 2),
                'Vp': round(Vp, 2),
                'Qri': round(Qri, 4)
            }

            # Якщо в ході обрахунків виникає помилка, то повертаємо статус 400
            # та виводимо помилку
        except Exception as e:
            return abort(400, f"Bad values: {e}")

        # Рендеримо сторінку разом з результатами обрахунків
        return render_template("prac_1_task_2.html", results=results)

    return render_template("prac_1_task_2.html", results=None)


@app.route("/prac-2/task-1", methods=["GET", "POST"])
def prac_2_task_1():
    if request.method == "POST":
        try:
            # Отримання користувацього вводу
            # Також заміняємо ',' на '.' для коректного переведення строки у float
            coal = float(request.form.get("coal").replace(",", "."))
            oil = float(request.form.get("oil").replace(",", "."))
            # gas = float(request.form.get("gas").replace(",", "."))

            # Також отримуємо константи, які може задати користувач
            Ap_coal = float(request.form.get("Ap").replace(",", "."))
            Qpi_coal = float(request.form.get("Qpi").replace(",", "."))
            Qgi_oil = float(request.form.get("Qgi_oil").replace(",", "."))
            Wp_oil = float(request.form.get("Wp_oil").replace(",", "."))
            Gvun = float(request.form.get("Gvun").replace(",", "."))
            nzu = float(request.form.get("nzu").replace(",", "."))

            # Значення частки леткої золи для вугілля та мазуту, взяті з таблиці 2.1
            avun_coal = 0.8
            avun_oil = 1

            # Шукаємо нижчу теплоту згоряння робочї маси для мазуту
            Qri_oil = Qgi_oil * (100 - Wp_oil - 0.15) / 100 - 0.025 * Wp_oil

            # Обчислюємо показник емісії твердих частинок при спалюванні вугілля
            # та валовий викид при спалюванні вугілля
            ktv_coal = math.pow(10, 6) / Qpi_coal * avun_coal * Ap_coal / (100 - Gvun) * (1 - nzu)
            Etv_coal = math.pow(10, -6) * ktv_coal * Qpi_coal * coal

            # Обчислюємо показник емісії твердих частинок при спалюванні мазуту
            # та валовий викид при спалюванні мазуту
            ktv_oil = math.pow(10, 6) / Qri_oil * avun_oil * 0.15 / 100 * (1 - nzu)
            Etv_oil = math.pow(10, -6) * ktv_oil * Qri_oil * oil

            # Оскільки при спалюванні природного газу тверді частинки відсутні,
            # то показник емісії та валовий викид = 0
            ktv_gas = 0
            Etv_gas = 0

            # Заносимо результати у словник та округлюємо їх
            results = {
                'ktv_coal': round(ktv_coal, 2),
                'Etv_coal': round(Etv_coal, 2),
                'ktv_oil': round(ktv_oil, 2),
                'Etv_oil': round(Etv_oil, 2),
                'ktv_gas': ktv_gas,
                'Etv_gas': Etv_gas
            }

        # Якщо в ході обрахунків виникає помилка, то повертаємо статус 400
        # та виводимо помилку
        except Exception as e:
            return abort(400, f"Bad values: {e}")

        # Рендеримо сторінку разом з результатами обрахунків
        return render_template("prac_2_task_1.html", results=results)

    return render_template("prac_2_task_1.html", results=None)


@app.route("/prac-3/task-1", methods=["GET", "POST"])
def prac_3_task_1():
    # Отримуємо значення по змовчуванню для таблиці (Значення з контрольного прикладу)
    with open("instance/prac_3_table_default_data.json", "r", encoding="UTF-8") as file:
        default_values = json.load(file)

    if request.method == "POST":
        try:
            # Отримуємо користувацький ввід для ЕП першого ШР
            nu_list = list(map(custom_float, request.form.getlist("nu[]")))
            cos_list = list(map(custom_float, request.form.getlist("cos[]")))
            Uh_list = list(map(custom_float, request.form.getlist("Uh[]")))
            n_list = list(map(custom_float, request.form.getlist("n[]")))
            Ph_list = list(map(custom_float, request.form.getlist("Ph[]")))
            KB_list = list(map(custom_float, request.form.getlist("KB[]")))
            tg_list = list(map(custom_float, request.form.getlist("tg[]")))

            # Шукаємо розрахункові струми на І рівні електропостачання
            nPh_list = [int(n_list[i] * Ph_list[i]) for i in range(len(nu_list))]
            # Знаходимо розрахунковий струм кожного ЕП
            Ip_list = [round(nPh_list[i] / (math.sqrt(3) * Uh_list[i] * cos_list[i] * nu_list[i]), 2) for i in
                       range(len(nu_list))]

            # Знаходимо груповий коефіцієнт використання
            nPhKB_list = [round(n_list[i] * Ph_list[i] * KB_list[i], 2) for i in range(len(nu_list))]
            group_use_coff = round(sum(nPhKB_list) / sum(nPh_list), 1)

            # Знаходимо ефективну кількість ЕП
            nPh_square_list = [round(n_list[i] * Ph_list[i] ** 2, 2) for i in range(len(nu_list))]
            ne = math.ceil(sum(nPh_list) ** 2 / sum(nPh_square_list))

            # Знаходимо розрахунковий коефіцієнт активної потужності по таблиці 3.3
            # за допомогою методу, описаного раніше в utils.py
            Kp = get_Kp_1(ne, group_use_coff)
            if not Kp:
                raise ValueError("Couldn't find corresponding values in data table.")

            # Знаходимо розрахункове активне навантаження
            Pp = round(Kp * sum(nPhKB_list), 2)

            # Знаходимо розрахункове реактивне навантаження
            nPhKBtg_list = [round(nPhKB_list[i] * tg_list[i], 2) for i in range(len(nu_list))]
            Qp = round(sum(nPhKBtg_list) * Kp, 2)

            # Знаходимо повну потужність
            Sp = round(math.sqrt(Pp ** 2 + Qp ** 2), 2)
            # Знаходимо розрахунковий груповий струм ШР1
            Ip = round(Pp / statistics.mean(Uh_list), 2)

            # Отримуємо користувацький ввід для крупних ЕП
            nu_big_list = list(map(custom_float, request.form.getlist("nu_big[]")))
            cos_big_list = list(map(custom_float, request.form.getlist("cos_big[]")))
            Uh_big_list = list(map(custom_float, request.form.getlist("Uh_big[]")))
            n_big_list = list(map(custom_float, request.form.getlist("n_big[]")))
            Ph_big_list = list(map(custom_float, request.form.getlist("Ph_big[]")))
            KB_big_list = list(map(custom_float, request.form.getlist("KB_big[]")))
            tg_big_list = list(map(custom_float, request.form.getlist("tg_big[]")))

            # Розрахунки ті ж самі, що і для звичайних ЕП
            nPh_big_list = [int(n_big_list[i] * Ph_big_list[i]) for i in range(len(nu_big_list))]
            nPhKB_big_list = [round(n_big_list[i] * Ph_big_list[i] * KB_big_list[i], 2) for i in
                              range(len(nu_big_list))]
            # Для другого ЕП відсутнє значення коефіцієнту реактивної потужності відсутнє,
            # тому замість нього пишемо 0 (Це ніяк не вплине на розрахунки, зроблено тільки для зручності
            nPhKBtg_big_list = [round(nPhKB_big_list[i] * tg_big_list[i] if i < len(tg_big_list) else 0, 2) for i in
                                range(len(nu_big_list))]
            nPh_square_big_list = [round(n_big_list[i] * Ph_big_list[i] ** 2, 2) for i in range(len(nu_big_list))]
            Ip_big_list = [
                round(nPh_big_list[i] / (math.sqrt(3) * Uh_big_list[i] * cos_big_list[i] * nu_big_list[i]), 2) for i in
                range(len(nu_big_list))]

            # Отримуємо користувацький ввід загального навантаження цеху
            n_all = float(request.form.get("n").replace(",", "."))
            nPh_all = float(request.form.get("nPh").replace(",", "."))
            nPhKB_all = float(request.form.get("nPhKB").replace(",", "."))
            nPhKBtg_all = float(request.form.get("nPhKBtg").replace(",", "."))
            nPh_square_all = float(request.form.get("nPh_square").replace(",", "."))

            # Знаходимо коефіцієнти використання цеху в цілому
            group_use_coff_all = round(nPhKB_all / nPh_all, 2)
            # Знаходимо ефективну кількість ЕП цеху в цілому
            ne_all = round(nPh_all ** 2 / nPh_square_all)
            # Знаходимо розрахунковий коефіцієнт активної потужності по таблиці 3.4
            # за допомогою методу, описаного раніше в utils.py
            Kp_all = get_Kp_2(ne_all, group_use_coff_all)
            # Знаходимо розрахункове активне навантаження на шинах 0,38 кВ ТП
            Pp_all = round(Kp_all * nPhKB_all, 2)
            # Знаходимо розрахункове реактивне навантаження на шинах 0,38 кВ ТП
            Qp_all = round(Kp_all * nPhKBtg_all, 2)
            # Знаходимо повну потужність на шинах 0,38 кВ ТП
            Sp_all = round(math.sqrt(Pp_all ** 2 + Qp_all ** 2), 2)
            # Знаходимо розрахунковий груповий струм на шинах 0,38 кВ ТП
            Ip_all = round(Pp_all / statistics.mean(Uh_big_list), 2)

            # Заносимо усі результати у список
            results = {
                "nPh_list": nPh_list,
                "Ip_list": Ip_list,
                "nPhKB_list": nPhKB_list,
                "group_use_coff": group_use_coff,
                "nPh_square_list": nPh_square_list,
                "ne": ne,
                "Kp": Kp,
                "Pp": Pp,
                "nPhKBtg_list": nPhKBtg_list,
                "Qp": Qp,
                "Sp": Sp,
                "Ip": Ip,
                "N": int(sum(n_list)),
                "nPh_sum": int(sum(nPh_list)),
                "nPhKB_sum": sum(nPhKB_list),
                "nPhKBtg_sum": round(sum(nPhKBtg_list), 2),
                "nPh_square_sum": sum(nPh_square_list),
                "nPh_big_list": nPh_big_list,
                "nPhKB_big_list": nPhKB_big_list,
                "nPhKBtg_big_list": nPhKBtg_big_list,
                "nPh_square_big_list": nPh_square_big_list,
                "Ip_big_list": Ip_big_list,
                "group_use_coff_all": group_use_coff_all,
                "ne_all": ne_all,
                "Kp_all": Kp_all,
                "Pp_all": Pp_all,
                "Qp_all": Qp_all,
                "Sp_all": Sp_all,
                "Ip_all": Ip_all
            }

            # Також створюємо список, який позначає користувацьки ввід
            # Це створено для того, щоб після розрахунків, значення введені користувачем, лишились
            user_values = {
                "normal": {
                    "naming": default_values.get("normal").get("naming"),
                    "nu[]": nu_list,
                    "cos[]": cos_list,
                    "Uh[]": Uh_list,
                    "n[]": n_list,
                    "Ph[]": Ph_list,
                    "KB[]": KB_list,
                    "tg[]": tg_list
                },
                "big": {
                    "naming": default_values.get("big").get("naming"),
                    "nu[]": nu_big_list,
                    "cos[]": cos_big_list,
                    "Uh[]": Uh_big_list,
                    "n[]": n_big_list,
                    "Ph[]": Ph_big_list,
                    "KB[]": KB_big_list,
                    "tg[]": tg_big_list
                },
                "all": {
                    "n": n_all,
                    "nPh": nPh_all,
                    "nPhKB": nPhKB_all,
                    "nPhKBtg": nPhKBtg_all,
                    "nPh_square": nPh_square_all
                }
            }
        except Exception as e:
            return abort(400, f"Bad values: {e}")

        # Рендеримо сторінку разом з результатами обрахунків
        return render_template("prac_3_task_1.html", default_values=user_values, results=results,
                               get_result_by_index=get_result_by_index)
    return render_template("prac_3_task_1.html", default_values=default_values, results={},
                           get_result_by_index=get_result_by_index)


if __name__ == '__main__':
    # Запуск локального веб-серверу
    # Параметр debug встановлено на True,
    # щоб при зміні коду не прийшлось перезавантажувати веб-сервер,
    # а зміни відразу вступали в дію
    app.run(host="0.0.0.0", port=80, debug=True)
