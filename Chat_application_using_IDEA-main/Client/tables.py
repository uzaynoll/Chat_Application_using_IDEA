for i in range(256):
    print(i, end=" ")
    for j in range(256):
        x = (i+j)%256
        if x == 0:
            print(j, end=" ")
    print()
m=257
for i in range(m):
    print(i, end=" ")
    for j in range(m):
        x = (i*j)%m
        if x == 1:
            print(j, end=" ")
    print()