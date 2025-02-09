"""user = {"name": "Gordon", "species": "human"}

# print(user)

users = [user]
users.append(dict(name="Peter", species="human"))
users.append(dict(name="Toffee", species="tortoise"))
#print(users[-2:])

for user in users:
    print(f'Hello {user["name"]} you are a {user["species"]}')
print("end of loop")"""

def adder(number_1, number_2):
    result =  number_1 + number_2
    return result

if __name__ == "__main__":    
    print(__name__)
    # test 1
    number_1 = 1
    number_2 = 3
    correct_answer = 4
    result = adder(number_1, number_2)
    if result == correct_answer:
        print("test passed")
    else:
        print("test failed")

    # test 2
    number_1 = "1"
    number_2 = "3"
    correct_answer = "13"
    result = adder(number_1, number_2)
    if result == correct_answer:
        print("test passed")
    else:
        print("test failed")