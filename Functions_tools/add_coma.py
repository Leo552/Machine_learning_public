f = open('A-set_A_1.txt', 'r+')
something = f.read()
f.close()

Write_to_same_file = True

new_something = ''
past_i = ''

for i in something:
    if i == ' ' and not past_i == ' ':
        new_something = new_something + ','
    else:
        new_something = new_something + i
    past_i = i

print(new_something)

if Write_to_same_file == True:
    f = open('A-set_A_1.txt', 'w')
    f.write(new_something)
    f.close()