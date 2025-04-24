import random
import smtplib
from email.message import EmailMessage

# Чтение вопросов и ответов из файла
def loe_kusimused():
    with open('kusimused_vastused.txt.txt', 'r') as file:
        return dict(line.strip().split(':') for line in file)

# Проведение опроса
def kuula_kusimusi(kus_vas, kasutaja_nimi, num_kusimusi=5):
    print(f"Привет, {kasutaja_nimi}! Начнем опрос.")
    num_kusimusi = min(num_kusimusi, len(kus_vas))
    valitud_kusimused = random.sample(list(kus_vas.keys()), num_kusimusi)
    õiged_vastused = sum(input(f"{kysimus}: ").lower() == kus_vas[kysimus].lower() for kysimus in valitud_kusimused)
    return õiged_vastused

# Проверка, был ли пользователь уже опрошен
vastajad = {}

def salvesta_vastaja(nimi, õiged_vastused, email):
    vastajad[nimi] = {"õiged_vastused": õiged_vastused, "email": email}

def kontrolli_vastajat(nimi):
    return nimi in vastajad

# Сохранение результатов в файлы
def salvesta_failidesse():
    with open('koik.txt.txt', 'w') as f_koik, open('oiged.txt.txt', 'w') as f_oiged, open('valed.txt.txt', 'w') as f_valed:
        for nimi, info in sorted(vastajad.items(), key=lambda x: x[1]['õiged_vastused'], reverse=True):
            email = info['email']
            õiged_vastused = info['õiged_vastused']
            f_koik.write(f"{nimi}, {õiged_vastused}, {email}\n")
            if õiged_vastused > 2:  # больше половины правильных ответов
                f_oiged.write(f"{nimi} – {õiged_vastused} õigesti\n")
            else:
                f_valed.write(f"{nimi} – {õiged_vastused} õigesti\n")

# Отправка писем пользователю
def saada_email(kasutaja_email, kasutaja_nimi, õiged_vastused, is_vastaja=False):
    status = "Поздравляем, вы успешно прошли тест!" if õiged_vastused > 2 else "К сожалению, тест не был пройден."
    msg = EmailMessage()
    msg.set_content(f"Привет {kasutaja_nimi}!\n\nКоличество правильных ответов: {õiged_vastused}\n{status}")
    msg['Subject'] = 'Результаты опроса'
    msg['From'] = 'mareklukk8@gmail.com'
    msg['To'] = kasutaja_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("mareklukk8@gmail.com", "ejya cszz bjea urti")  # App Password
        server.send_message(msg)

# Отправка отчета работодателю
def saada_koondreport(kasutajate_andmed):
    report = "Сегодняшние результаты опроса:\n"
    for nimi, info in kasutajate_andmed:
        result = "ПОДХОДИТ" if info['õiged_vastused'] > 2 else "НЕ ПОДХОДИТ"
        report += f"{nimi} – {info['õiged_vastused']} правильных ответов – {info['email']} – {result}\n"
    best = max(kasutajate_andmed, key=lambda x: x[1]['õiged_vastused'])
    report += f"\nЛучший участник: {best[0]} ({best[1]['õiged_vastused']} правильных ответов)"

    msg = EmailMessage()
    msg.set_content(report)
    msg['Subject'] = 'Отчет по результатам опроса'
    msg['From'] = 'mareklukk8@gmail.com'
    msg['To'] = 'mareklukk8@gmail.com'

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login("mareklukk8@gmail.com", "ejya cszz bjea urti")
        server.send_message(msg)

# Добавление нового вопроса
def lisa_kysimus():
    kysimus = input("Введите новый вопрос: ")
    vastus = input("Введите правильный ответ: ")
    with open('kusimused_vastused.txt.txt', 'a') as file:
        file.write(f"{kysimus}:{vastus}\n")

# Вывод результатов на экран
def kuvatakse_tulemused():
    print("Успешные участники:")
    for nimi, info in sorted(vastajad.items(), key=lambda x: x[1]['õiged_vastused'], reverse=True):
        print(f"{nimi} – {info['õiged_vastused']} правильных ответов")
    print("\nРезультаты отправлены на электронные адреса.")

# Главное меню программы
def main():
    kus_vas = loe_kusimused()

    while True:
        print("\nМеню:")
        print("1. Начать опрос")
        print("2. Добавить новый вопрос")
        print("3. Выйти")
        valik = input("Выберите опцию: ")

        if valik == "1":
            kasutaja_nimi = input("Введите ваше имя: ")
            if kontrolli_vastajat(kasutaja_nimi):
                print(f"{kasutaja_nimi} уже прошел опрос.")
            else:
                õiged_vastused = kuula_kusimusi(kus_vas, kasutaja_nimi)
                kasutaja_email = input("Введите ваш email для получения результатов: ")
                salvesta_vastaja(kasutaja_nimi, õiged_vastused, kasutaja_email)
                saada_email(kasutaja_email, kasutaja_nimi, õiged_vastused)
        elif valik == "2":
            lisa_kysimus()
        elif valik == "3":
            salvesta_failidesse()
            kuvatakse_tulemused()
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
