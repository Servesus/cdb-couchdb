from cloudant.client import CouchDB

def init(couch):
    new_bdd = couch.create_database("prueba")
    vista = {
            "_id": "_design/listas",
            "views": {
                "nombre": {
                "map": "function (doc) {\n  emit(doc._id, doc.name);\n}"
                }
            },
            "language": "javascript"
            }
    new_bdd.create_document(vista)
    doc_tel = {
            "name": "Teledetección",
            "tasks": [
                {
                "name": "Practica 1",
                "status": "1"
                },
                {
                "name": "Practica 2",
                "status": "1"
                },
                {
                "name": "Trabajo",
                "status": "0"
                },
                {
                "name": "Examen",
                "status": "0"
                }
            ]
            }
    new_bdd.create_document(doc_tel)
    doc_cbd = {
            "name": "Complementos de Bases de Datos",
            "tasks": [
                {
                "name": "Documentación",
                "status": "0"
                },
                {
                "name": "Aplicación",
                "status": "1"
                },
                {
                "name": "Presentación",
                "status": "0"
                }
            ]
            }
    new_bdd.create_document(doc_cbd)

if __name__ == "__main__":
    couch = CouchDB('admin','admin',url='http://localhost:5984',connect=True,renew=True)
    bdd = couch['prueba']
    if(bdd.exists()):
        couch.delete_database("prueba")
        init(couch)
    else:
        init()
    couch.disconnect()

    