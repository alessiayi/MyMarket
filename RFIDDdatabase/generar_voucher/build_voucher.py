from reportlab.lib.enums import TA_JUSTIFY,TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import letter, A6,landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# encoding:utf-8

articulos = [{"id":1,"UID_Code":"22715318128211","Nombre_Producto":"Leche Evap","Precio":5,"Cantidad":1},
             {"id":2,"UID_Code": "1501592416254", "Nombre_Producto": "Chocolate", "Precio": 3, "Cantidad": 1}]

doc = SimpleDocTemplate("/home/pyxel/Escritorio/prueba.pdf", pagesize=A6,
                        rightMargin=72, leftMargin=72,
                        topMargin=72, bottomMargin=18)

estilos = getSampleStyleSheet()
estilos.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
estilos.add(ParagraphStyle(name='Center', alignment=TA_CENTER))
estilos.add(ParagraphStyle(name='Right', alignment=TA_RIGHT))


precio_final = 0
story = []

story.append(Paragraph("MyMarket",estilos["Center"]))
story.append(Paragraph("========", estilos["Center"]))
story.append(Spacer(1, 16))

for prop in articulos:
    id = prop["id"]
    uid = prop["UID_Code"]
    nombre = prop["Nombre_Producto"]+"\t"
    precio = prop["Precio"]
    precio_final += precio

    item = str(id)+ "    "+nombre+ "\t"+str(precio)
    story.append(Paragraph(item, estilos["Normal"]))
    story.append(Spacer(1, 6))
    print(id, "\t",nombre, "\t",precio)

print("\t\t","Total ","\t", precio_final)
final = "    Total: " + str(precio_final)
story.append(Paragraph(final,estilos["Right"]))
doc.build(story)