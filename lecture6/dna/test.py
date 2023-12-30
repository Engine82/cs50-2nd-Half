database = [
      {"Alice": 23},
      {"Bob": 45}
]


for person in database:
    for name in person:
        print(f"{person[name]}")


diction = {
    "Hi": 5,
    "Hello": 4
}

print(f"{diction}")

dictio = list(diction.values())

print(f"{dictio}")

dictio = list(diction.keys())

print(f"{dictio}")
