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
      def muestraLista(id):
        #Accedo al documento que se ha clickado
        doc = bdd[id]
        #Quito el frame superior para poder listar las tareas de la lista en la que estoy
        top.destroy()
        bot.destroy()
        new_top = Frame(tk)
        new_bot = Frame(tk)

        def atras():
          new_top.destroy()
          new_bot.destroy()
          init()

        #Para cada tarea imprimirla con los botones e implementacion de los botones
        for counter,t in enumerate(doc["tasks"]):
          top3 = Frame(new_top)

          var2 = StringVar()
          label2 = Label(top3, textvariable=var2)

          if(t["status"] == "1"):
           var2.set("✅ "+t["name"])
           b3 = Button(top3, text ="Deshacer", command = lambda c=doc,d=counter:deshacer_tarea(c,d))
          else:
            var2.set("❌ "+t["name"])
            b3 = Button(top3, text ="Hacer", command = lambda c=doc,d=counter:hacer_tarea(c,d))
          
          label2.pack(side = LEFT)

          def eliminar_tarea(doc1,t1):
            doc1["tasks"].remove(t1)
            doc1.save()
            new_top.destroy()
            new_bot.destroy()
            muestraLista(doc1["_id"])
          
          def hacer_tarea(doc1,t1):
            doc1["tasks"][t1]["status"] = "1"
            doc1.save()
            new_top.destroy()
            new_bot.destroy()
            muestraLista(doc1["_id"])
          def deshacer_tarea(doc1,t1):
            doc1["tasks"][t1]["status"] = "0"
            doc1.save()
            new_top.destroy()
            new_bot.destroy()
            muestraLista(doc1["_id"])

          b4 = Button(top3, text ="Eliminar", command = lambda c=doc,d=t:eliminar_tarea(c,d))
          b3.pack(side=LEFT)
          b4.pack(side=RIGHT)
          top3.pack()
  
        atras = Button(new_top, text ="Atrás", command = atras)
        atras.pack()
        new_top.pack()

        #Parte de abajo para añadir tasks
        #Input para crear una nueva task
        nueva_task = Entry(new_bot)
        def añadir_task():
          if(nueva_task.get()!=""):
            diccionario_task = {"name":nueva_task.get(),"status":"0"}
            doc["tasks"].append(diccionario_task)
            doc.save()
            new_top.destroy()
            new_bot.destroy()
            muestraLista(doc["_id"])

        crear_task = Button(new_bot, text ="Crear", command = añadir_task)
        var_task = StringVar()
        label_task = Label(new_bot, textvariable=var_task)
        var_task.set("Nueva Tarea")
        label_task.pack()
        nueva_task.pack(side = LEFT)
        crear_task.pack(side = RIGHT)
        new_bot.pack(side = BOTTOM)

      top2 = Frame(top)
      top2.pack()
      var1 = StringVar()
      label1 = Label(top2, textvariable=var1)
      var1.set(i["value"])
      label1.pack(side = LEFT)
      b = Button(top2, text ="Ver", command = lambda c=i["key"]: muestraLista(c))
      def eliminaLista(id):
        doc = bdd[id]
        doc.delete()
        top.destroy()
        bot.destroy()
        init()
      b2 = Button(top2, text ="Eliminar", command = lambda c=i["key"]: eliminaLista(c))
      b2.pack(side=RIGHT)
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

