from Tkinter import *
import Read

#Need to constantly update the dictionary while session=true, exit=false

#Crea la ventana
#root = Tk()

##tienda["Tarjeta"]=3.00
##tienda["Llavero"]=1.50
##tienda["Papitas"]=2.00
##tienda["Agua"]=2.50
##tienda["Pan"]=0.20
##tienda["Lentes"]=100
##tienda["Chocolate"]=5.00

#Declaracion de variables #ANDREA
suma = 0 #ANDREA
for x in tienda.values():
    suma+=x

for x in tienda:
    lista_productos.append(x)
    lista_precios.append(tienda[x])

#Crea la ventana
root = Tk()

#Color de fondo
root.configure(bg="white")

#Cambiar titulo
root.title("Mi carrito")

#Tamano
root.geometry("600x420")

#Update Function
def update_listbox_productos():
    listbox_productos.delete(0, END)
    for item in lista_productos:
        listbox_productos.insert(END, item)

def update_listbox_precios():
    listbox_precios.delete(0, END)
    for item in lista_precios:
        listbox_precios.insert(END, item)


def update_suma(ind): #ANDREA
    global suma
    if len(tienda)!=1: suma -= lista_precios[ind]
    else: suma = 0

    lbl_suma.config(text="Suma: " + str(suma))



def delete_func():
    global suma #ANDREA
    producto = listbox_productos.get("active")
    #print(precio, producto)
    index = lista_productos.index(listbox_productos.get("active")) #ANDREA

    #Update suma
    update_suma(index) #ANDREA

    if producto in tienda:
        del tienda[producto]
        lista_precios.pop(index) #ANDREA
        lista_productos.pop(index) #ANDREA

    print tienda
    update_listbox_productos()
    update_listbox_precios()

del_button = Button(root, text="delete", command=delete_func)
del_button.grid(row=2, column=0)

#Labels
lbl_productos = Label(root, text="Tus Productos")
lbl_productos.grid(row=0, column=0)

lbl_precios = Label(root, text="Precio")
lbl_precios.grid(row=0, column=1)

#ANDREA
lbl_suma = Label(root, text="Suma: " + str(suma))
lbl_suma.grid(row=2, column=1)

###########

#LISTA PRODUCTOS
#lista_productos = ["one", "two", "three", "four"]

listbox_productos = Listbox(root)
listbox_productos.config(width=40, height=20)
listbox_productos.grid(row=1, column=0, padx=10, pady=10)

#Displays elements on list
for item in lista_productos:
    listbox_productos.insert(END, item)

update_listbox_productos()

#############

#LISTA PRECIOS
#lista_precios = ["1", "2", "3", "4"]

listbox_precios = Listbox(root)
listbox_precios.config(width=22, height=20)
listbox_precios.grid(row=1, column=1, padx=10, pady=10)



#Displays elements on list
for item in lista_precios:
    listbox_precios.insert(END, item)

update_listbox_precios()


#############

#Comienza los eventos
root.mainloop()