

# name of price files
files = ['prices_agriculture', 'prices_livestock', 'prices_luxury', 'prices_manufactured']

for f_name in files:

    type = f_name.split('_')[1]

    f_name = "./prices/" + f_name
    f = open(f_name, 'r')
    while True:
        newline = f.readline()
        if not newline:
            break

        try:
            newline = newline.split(' ')
            name = newline[0]
            price = str(newline[1]).split('/')[0]
            
        except IndexError as e:
            continue

        print(type, name, price)

    f.close()

