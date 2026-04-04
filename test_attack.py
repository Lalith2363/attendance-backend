import requests

url = "http://127.0.0.1:8000/employees"

# for i in range(50):
#     r = requests.get(url)
#     print(i, r.status_code, r.text)

# headers_list = [
#     {"X-Forwarded-For": "1.1.1.1"},
#     {"X-Forwarded-For": "2.2.2.2"},
#     {"X-Forwarded-For": "3.3.3.3"},
# ]

# for i in range(60):
#     headers = headers_list[i % len(headers_list)]
#     r = requests.get(url, headers=headers)
#     print(i, r.status_code)



headers = {
    "Authorization": "Bearer YOUR_TOKEN"
}

for i in range(50):
    r = requests.get("http://127.0.0.1:8000/employees", headers=headers)
    print(i, r.status_code, r.text)