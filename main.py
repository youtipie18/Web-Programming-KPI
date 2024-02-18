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


if __name__ == '__main__':
    # Запуск локального веб-серверу
    # Параметр debug встановлено на True,
    # щоб при зміні коду не прийшлось перезавантажувати веб-сервер,
    # а зміни відразу вступали в дію
    app.run(host="0.0.0.0", port=80, debug=True)
