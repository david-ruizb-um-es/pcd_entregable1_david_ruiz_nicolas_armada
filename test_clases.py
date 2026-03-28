import pytest
from clases import MiImperio, Almacen, Repuesto, NaveEstelar, Clase, EstacionEspacial, CazaEstelar, Ubicacion

#Usamos el entorno que hemos creado el fichero de las clases para ahorrar tiempo
#usamos la fixture  

@pytest.fixture
def base_imperio():
    imperio = MiImperio()

    #Instanciacion de clases
    almacen_principal = Almacen("Base Starkiller", "Sistemas Desconocidos")
    motor = Repuesto("Motor Hiperimpulsor", "Kuat Drive Yards", 5, 25000.0)
    escudo = Repuesto("Generador Deflector", "Sienar Fleet Systems", 2, 15000.0)

    almacen_principal.agregar_repuesto(motor)
    almacen_principal.agregar_repuesto(escudo)
    imperio.registrar_almacen(almacen_principal)

    # Naves
    destructor = NaveEstelar("ID-EXEC-01", 1138, "Vengador", ["Motor Hiperimpulsor"], 37000, 2500, Clase.EJECUTOR)
    estacion = EstacionEspacial("DS-2", 9999, "Estrella de la Muerte II", ["Panel de control"], 1200000, 50000, Ubicacion.ENDOR)
    caza = CazaEstelar("TIE-IN-01", 7777, "Interceptor TIE", ["Generador Deflector"], 1)
    imperio.registrar_unidad(destructor)
    imperio.registrar_unidad(estacion)
    imperio.registrar_unidad(caza)
    
    #con esto podemos instancair despues para los tests
    return {
        "imperio": imperio,
        "motor": motor,
        "escudo": escudo,
        "destructor": destructor,
        "caza": caza
    }


#TESTS


def test_adquirir_repuesto_reduce_stock(base_imperio):
   #al adquirir un repuesto, el stock baja

    imperio = base_imperio["imperio"]
    destructor = base_imperio["destructor"]
    motor = base_imperio["motor"]
        
    #adquirimos 2 motores
    imperio.adquirir_repuesto(destructor, "Motor Hiperimpulsor", 2)
    
    assert motor.get_cantidad() == 3


def test_consultar_repuesto(base_imperio):
    #comprobamos que solo se devuelva un repuesto
    #hacemos esto porque el mismo repuesto podia estar en varios almacenes y queremos comprobar si la soluciom
    #que hemos implementado es correcta
    imperio = base_imperio["imperio"]
    motor = base_imperio["motor"]
    
    resultados = imperio.consultar_repuesto("Motor Hiperimpulsor")
    #Deberia de haber solo 1 resultado
    assert len(resultados) == 1
    
    #Deberia ser asi
    nombre_almacen, repuesto_encontrado = resultados[0]
    assert nombre_almacen == "Base Starkiller"
    assert repuesto_encontrado == motor


def test_registro_de_unidades(base_imperio):
    #comprobamos que las naves se registran adecuadamente
    imperio = base_imperio["imperio"]
    #Creamos y registramos una nueva deberiamos tener 4 
    nuevo_caza = CazaEstelar("TIE-BOMBER-01", 4444, "Bombardero TIE", [], 2)
    imperio.registrar_unidad(nuevo_caza)
    assert len(imperio.unidades) == 4
    assert nuevo_caza in imperio.unidades


def test_herencia_de_naves(base_imperio):
    #verificamos la herencia
    from clases import Nave, UnidadCombate
    caza = base_imperio["caza"]
    #es instancia del padre y del abuelo
    assert isinstance(caza, CazaEstelar)
    assert isinstance(caza, Nave)
    assert isinstance(caza, UnidadCombate)