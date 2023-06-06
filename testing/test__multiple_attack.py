import requests
import csv
import random
import matplotlib.pyplot as plt

# Список пользователей и паролей для тестирования
users = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"},
    {"username": "user3", "password": "password3"}
]

# Список URL-адресов для тестирования
urls = [
    "http://localhost:8000/login/",
    "http://localhost:8000/register/",
    "http://localhost:8000/profile/",
    "http://localhost:8000/logout/",
    "http://localhost:8000/change-password/",
    "http://localhost:8000/reset-password/",
    "http://localhost:8000/confirm-email/",
]

# Создание CSV-файла для записи статистики
with open("statistics1.csv", "w", newline="") as csvfile:
    fieldnames = ["user", "url", "type", "status"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Функция для тестирования GET-атаки CSRF
    def test_get_csrf(url, user):
        url_with_params = f"{url}?username={user['username']}&email=attacker@example.com"
        response = requests.get(url_with_params)
        
        if response.status_code == 200: 
            writer.writerow({"user": user["username"], "url": url, "type": "GET", "status": "Success"})
        else:
            writer.writerow({"user": user["username"], "url": url, "type": "GET", "status": "Error"})

    # Функция для тестирования POST-атаки CSRF
    def test_post_csrf(url, user):
        payload = {"username": user["username"], "email": "attacker@example.com"}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            writer.writerow({"user": user["username"], "url": url, "type": "POST", "status": "Success"})
        else:
            writer.writerow({"user": user["username"], "url": url, "type": "POST", "status": "Error"})

    # Функция для тестирования AJAX-атаки CSRF
    def test_ajax_csrf(url, user):
        headers = {
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
        data = {"username": user["username"], "email": "attacker@example.com"}
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            writer.writerow({"user": user["username"], "url": url, "type": "AJAX", "status": "Success"})
        else:
            writer.writerow({"user": user["username"], "url": url, "type": "AJAX", "status": "Error"})

    # Функция для тестирования CSRF-атаки на множественные формы
    def test_multi_form_csrf(url, user):
        data1 = {"username": user["username"], "email": "attacker@example.com"}
        response1 = requests.post(url, data=data1)
        data2 = {"email": "attacker@example.com"}
        response2 = requests.post(url, data=data2)
        if response1.status_code == 200 and response2.status_code == 200:
            writer.writerow({"user": user["username"], "url": url, "type": "Multi-form", "status": "Success"})
        else:
            writer.writerow({"user": user["username"], "url": url, "type": "Multi-form", "status": "Error"})

    # Отправка HTTP-запросов с разных компьютеров
    for i in range(100):
        user = random.choice(users)
        url = random.choice(urls)

        # Имитация случайной ошибки на некоторых запросах
        if random.random() < 0.2:
            test_get_csrf(url, user)
            test_post_csrf(url, user)
            test_ajax_csrf(url, user)
            test_multi_form_csrf(url, user)
        else:
            test_get_csrf(url, user)
            test_post_csrf(url, user)
            test_ajax_csrf(url, user)
            test_multi_form_csrf(url, user)

# Создание графика статистики
data = {}
with open("statistics1.csv", "r") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row["url"] not in data:
            data[row["url"]] = {"Success": 0, "Error": 0, "GET": 0, "POST": 0, "AJAX": 0, "Multi-form": 0}
        data[row["url"]][row["status"]] += 1
        data[row["url"]][row["type"]] += 1

urls = list(data.keys())
success_counts = [data[url]["Success"] for url in urls]
error_counts = [data[url]["Error"] for url in urls]
get_counts = [data[url]["GET"] for url in urls]
post_counts = [data[url]["POST"] for url in urls]
ajax_counts = [data[url]["AJAX"] for url in urls]
multi_form_counts = [data[url]["Multi-form"] for url in urls]

plt.bar(urls, success_counts, label="Success")
plt.bar(urls, error_counts, bottom=success_counts, label="Error")
 
plt.xticks(rotation=45)
plt.legend()
plt.savefig("statistics1.png")
