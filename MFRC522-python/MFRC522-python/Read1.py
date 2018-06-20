#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
from Tkinter import *

suma = 0

###### Nuestra Base de Datos ########
tienda={}
productos_id={}
lista_productos=[]
lista_precios=[]

Tarjeta1_id = "246731224974"
Tarjeta2_id = "1234165197214"
Tarjeta3_id = "198181024939"

productos_id["246731224974"]="Tarjeta_1"
productos_id["1234165197214"]="Tarjeta_2"
productos_id["198181024939"]="Tarjeta_3"

tienda[Tarjeta1_id]=3.00
tienda[Tarjeta2_id]=1.50
tienda[Tarjeta3_id]=5.00
###### Nuestra Base de Datos ########

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to the MFRC522 data read example"
print "Press Ctrl-C to stop."

#Comienzan el GUI
root = Tk()

#Color de fondo
root.configure(bg="white")

#Cambiar titulo
root.title("Mi carrito")

#Tamano
root.geometry("600x420")

#Labels
lbl_productos = Label(root, text="Tus Productos")
lbl_productos.grid(row=0, column=0)

lbl_precios = Label(root, text="Precio")
lbl_precios.grid(row=0, column=1)

lbl_suma = Label(root)
lbl_suma.grid(row=2, column=1)

#Listbox
listbox_productos = Listbox(root)
listbox_productos.config(width=40, height=20)
listbox_productos.grid(row=1, column=0, padx=10, pady=10)

listbox_precios = Listbox(root)
listbox_precios.config(width=22, height=20)
listbox_precios.grid(row=1, column=1, padx=10, pady=10)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
    # Scan for cards    
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # If a card is found
    if status == MIFAREReader.MI_OK:
        print "Card detected"
    
    # Get the UID of the card
    (status,uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        
        #Transforma el UID a string
        uid1=str(uid[0]) + str(uid[1]) + str(uid[2]) + str(uid[3]) + str(uid[4])
        print uid1
        
        # Print UID
        print "Card read UID: %s,%s,%s,%s,%s" % (uid[0], uid[1], u id[2], uid[3], uid[4])
    
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)

        # Authenticate
        status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

        # Check if authenticated
        if status == MIFAREReader.MI_OK:
            MIFAREReader.MFRC522_Read(8)
            MIFAREReader.MFRC522_StopCrypto1()
        
        #Mete los UID a listas
            if uid1 in tienda:
                lista_productos.append(productos_id[uid1])
                lista_precios.append(tienda[uid1])
                print "Productos: ",
                print lista_productos,

                print "Precios: ",
                print lista_precios,
            else:
                print "Producto no identificado"
        else:
            print "Authentication error"

        #Update Function
        def update_listbox_productos():
            listbox_productos.delete(0, END)
            for item in lista_productos:
                listbox_productos.insert(END, item)

        def update_listbox_precios():
            listbox_precios.delete(0, END)
            for item in lista_precios:
                listbox_precios.insert(END, item)
        
        #Delete Function
        def delete_func():
            producto = listbox_productos.get("active")
            #print(precio, producto)
            index = lista_productos.index(producto) #ANDREA

            if producto in lista_productos:
                lista_precios.pop(index) #ANDREA
                lista_productos.pop(index) #ANDREA

            update_listbox_productos()
            update_listbox_precios()

        ###### LISTA PRODUCTOS #######

        #Displays elements on list
        for item in lista_productos:
            listbox_productos.insert(END, item)

        update_listbox_productos()
        #####-------------##########

        ##### Lista Precios #########
        #Displays elements on list
        for item in lista_precios:
            listbox_precios.insert(END, item)

        update_listbox_precios()
        #####-------------##########
        
        #Hace la SUMA
        suma=0
        for x in lista_precios:
            suma+=x
        lbl_suma.config(text="Suma: " + str(suma))
        #############

        #Comienza los eventos
        root.update()
        
        #Espera un rato antes de leer las tarjetas
        time.sleep(2)

#Termina el GUI
root.mainloop()
