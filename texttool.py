t = input("text: ")
i = int(input("id: "))
last = 0
f = "%" + str(i)

for c in t:
    c = ord(c)
    char = "+" if c > last else "-"
    
    if last != c:
        f += " " + char + str(abs(c - last))
    f += " ("
    last = c

print(f)