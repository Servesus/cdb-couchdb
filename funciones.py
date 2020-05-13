from cloudant.client import CouchDB
from cloudant.view import View
from cloudant.design_document import DesignDocument
from tkinter import *

if __name__ == "__main__":

  #Conexion a la base de datos
  couch = CouchDB('admin','admin',url='http://localhost:5984',connect=True,renew=True)
  bdd = couch['tasks-app']

  #Creo la ventana basica
  tk = Tk()
  tk.geometry("500x500")
  
  #Vista inicial
  def init():
    views = DesignDocument(bdd,'listas')
    nombres = View(views,'nombre')
    lists = nombres()['rows']
    top = Frame(tk)
    bot = Frame(tk)

    #Crea un boton por cada lista
    for i in lists:
      #Cuando se clicka una de las lista elimina lo que esta en pantalla y muestra las tareas
      def muestraLista():
        #Accedo al documento que se ha clickado
        doc = bdd[i["key"]]
        #Quito el frame superior para poder listar las tareas de la lista en la que estoy
        top.destroy()
        bot.destroy()
        new_top = Frame(tk)

        def atras():
          new_top.destroy()
          init()

        atras = Button(new_top, text ="Atrás", command = atras)

        #for t in doc["tasks"]:

        atras.pack()
        new_top.pack()


      b = Button(top, text =i["value"], command = muestraLista)
      b.pack()
    top.pack()
    bot.pack(side= BOTTOM)
    
    #Input para crear una nueva lista
    nueva_lista = Entry(bot)
    def crearLista():
      if(nueva_lista.get() != ""):
        data = {"name": nueva_lista.get(),"tasks": []}
        bdd.create_document(data)  
        top.destroy()
        bot.destroy()
        init()

    #Parte de abajo para crear nuevas listas
    crear = Button(bot, text ="Crear", command = crearLista)
    var = StringVar()
    label = Label( bot, textvariable=var)
    var.set("Nueva Lista")
    label.pack()
    nueva_lista.pack(side = LEFT)
    crear.pack(side = RIGHT)
    

    
  
  init()
  tk.mainloop()

