
file = open("test.txt", 'w')

i = 0
while True:
    file.write(str(i)+'\n')
    i += 1
    print(file)
    input("press enter")
    
file.close()