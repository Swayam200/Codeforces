s = input()
words = s.split("WUB")
final_word = " ".join([w for w in words if w != ""])
print(final_word)
