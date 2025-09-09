p = input()
language = ["H", "Q", "9"]

is_language = False
for char in p:
    while is_language is False:
        if char in language:
            print("YES")
            is_language = True
            break
        break

if is_language == False:
    print("NO")
    