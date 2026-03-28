
from abc import ABC, abstractmethod
from enum import Enum


#Excepciones que se lanzan despues en el codigo

class RepuestoNoEncontradoError(Exception):
    pass

class StockInsuficienteError(Exception):
    pass




class MiImperio:
    """Aqui esta la 'interfaz' del programa"""

    def __init__(self):
        self.unidades = []
        self.almacenes = []

    def registrar_almacen(self, almacen):
        self.almacenes.append(almacen)

    def registrar_unidad(self, unidad):
        self.unidades.append(unidad)

    #los siguientes dos métodos son para los comandantes

    def consultar_repuesto(self, nombre_repuesto: str):
        """Busca un repuesto por nombre en todos los almacenes."""
        resultados = []
        
        for almacen in self.almacenes:
            for repuesto in almacen.catalogo_repuestos:
                if repuesto.nombre.lower() == nombre_repuesto.lower():#por si se cometiera algun error al escribir:
                    resultados.append((almacen.nombre, repuesto))
        return resultados

    def adquirir_repuesto(self, nave, nombre_repuesto: str, cantidad_solicitada: int):
        """Permite a un comandante adquirir un repuesto para su nave."""
        resultados = self.consultar_repuesto(nombre_repuesto)

        if not resultados:#lanzamos la excepcion si no hay repuesto
            raise RepuestoNoEncontradoError(f"El repuesto '{nombre_repuesto}' no existe.")

        nombre_almacen, repuesto = resultados[0]#ponemos el primero para no calentarnos la cabeza

        if repuesto.get_cantidad() < cantidad_solicitada:#lanzamos la excepcion si no hay stock
            raise StockInsuficienteError(f"Stock de '{nombre_repuesto}' insuficiente. "
                f"Solicitado: {cantidad_solicitada}, Disponible: {repuesto.get_cantidad()}")

        repuesto.set_cantidad(repuesto.get_cantidad() - cantidad_solicitada)
        print(f"La nave '{nave.nombre}' ha adquirido {cantidad_solicitada} unidades de '{nombre_repuesto}' del almacén '{nombre_almacen}'.")

    #el siguiente metodo es para los operarios de almacen
    def actualizar_stock(self, nombre_almacen: str, nombre_repuesto: str, cantidad_a_sumar: int):
        """Permite a un operario modificar el stock de un repuesto."""
        for almacen in self.almacenes:
            if almacen.nombre == nombre_almacen:
                for repuesto in almacen.catalogo_repuestos:
                    if repuesto.nombre == nombre_repuesto:
                        repuesto.set_cantidad(repuesto.get_cantidad() + cantidad_a_sumar)
                        print(f"[OPERARIO] Stock actualizado: '{nombre_repuesto}' ahora tiene "
                              f"{repuesto.get_cantidad()} unidades en '{nombre_almacen}'.")
                        return

        raise RepuestoNoEncontradoError("Almacen o repuesto no encontrado")


#definimos las enumeraciones

class Clase(Enum):
    """Clases posibles para una Nave Estelar."""
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"


class Ubicacion(Enum):
    """Posibles ubicaciones para una Estacion Espacial."""
    ENDOR = "Endor"
    CUMULO_RAIMOS = "Cumulo Raimos"
    NEBULOSA_KALIIDA = "Nebulosa Kaliida"


#la unidad de combate es una clase abstracta porque no se va a usar directamente, sino que usaremos la nave estelar y las demás..
#implemento el metodo __str__ para poder comprobar luego que las naves están bien añadidas y demás
class UnidadCombate(ABC):
    
    def __init__(self, identificador_combate: str, clave_transmision: int):
        self.identificador_combate = identificador_combate
        self.clave_transmision = clave_transmision

    @abstractmethod
    def __str__(self):
        """ Ya lo haran las subclases"""
        pass


#tambien es abstracta

class Nave(UnidadCombate, ABC):
    def __init__(self, identificador_combate: str, clave_transmision: int,
                 nombre: str, catalogo_piezas: list):
        
        super().__init__(identificador_combate, clave_transmision)
        
        self.nombre = nombre
        self.catalogo_piezas = catalogo_piezas



#naves
class NaveEstelar(Nave):
    def __init__(self, identificador_combate: str, clave_transmision: int,nombre: str, catalogo_piezas: list,
                 tripulacion: int, pasaje: int, clase: Clase):
        super().__init__(identificador_combate, clave_transmision, nombre, catalogo_piezas)
        
        if not isinstance(clase, Clase):#error si no esta en la enumeracion
            raise ValueError(f"La clase debe ser un valor de Clase: {[c.value for c in Clase]}")
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def __str__(self):
        return (f"Nave Estelar '{self.nombre}' | Clase: {self.clase.value} | "
                f"Tripulación: {self.tripulacion} | Pasaje: {self.pasaje} | "
                f"ID: {self.identificador_combate}")


class EstacionEspacial(Nave):
    def __init__(self, identificador_combate: str, clave_transmision: int,
                 nombre: str, catalogo_piezas: list,
                 tripulacion: int, pasaje: int, ubicacion: Ubicacion):
        super().__init__(identificador_combate, clave_transmision, nombre, catalogo_piezas)
        
        if not isinstance(ubicacion, Ubicacion):#error si no esta en la enumeracion
            raise ValueError(f"La ubicación debe ser un valor de Ubicacion: {[u.value for u in Ubicacion]}")
        
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def __str__(self):
        return (f"Estación Espacial '{self.nombre}' | Ubicación: {self.ubicacion.value} | "
                f"Tripulación: {self.tripulacion} | Pasaje: {self.pasaje} | "
                f"ID: {self.identificador_combate}")


class CazaEstelar(Nave):
    def __init__(self, identificador_combate: str, clave_transmision: int,
                 nombre: str, catalogo_piezas: list, dotacion: int):
        super().__init__(identificador_combate, clave_transmision, nombre, catalogo_piezas)
        self.dotacion = dotacion

    def __str__(self):
        return (f"Caza Estelar '{self.nombre}' | Dotación: {self.dotacion} | "
                f"ID: {self.identificador_combate}")

#Almacen
class Almacen:
    def __init__(self, nombre: str, localizacion: str):
        self.nombre = nombre
        self.localizacion = localizacion
        self.catalogo_repuestos = []

    def agregar_repuesto(self, repuesto):
        self.catalogo_repuestos.append(repuesto)

    def __str__(self):
        return f"Almacén '{self.nombre}' en {self.localizacion} con {len(self.catalogo_repuestos)} repuestos."


#Repuesto
class Repuesto:
    def __init__(self, nombre: str, proveedor: str, cantidad: int, precio: float):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad
        self.precio = precio
    #como el atributo era privado en el diagrama que hemos hecho, para obtenerlo usammos un get
    def get_cantidad(self):
        return self.__cantidad

    def set_cantidad(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.__cantidad = nueva_cantidad

    def __str__(self):
        return (f"Repuesto(Nombre: {self.nombre}, Proveedor: {self.proveedor}, "
                f"Cantidad: {self.__cantidad}, Precio: {self.precio})")




# CÓDIGO DE PRUEBA Y GESTIÓN DE EXCEPCIONES


if __name__ == "__main__":
    # Instanciamos el sistema principal
    imperio = MiImperio()

    # 1. Instanciacion de clases
    print("Creando almacenes y repuestos")
    almacen_principal = Almacen("Base Starkiller", "Sistemas Desconocidos")
    motor = Repuesto("Motor Hiperimpulsor", "Kuat Drive Yards", 5, 25000.0)
    escudo = Repuesto("Generador Deflector", "Sienar Fleet Systems", 2, 15000.0)

    almacen_principal.agregar_repuesto(motor)
    almacen_principal.agregar_repuesto(escudo)
    imperio.registrar_almacen(almacen_principal)
    print(f"  -> {almacen_principal}")#probamos que vaya el__str__

    print("\nCreando unidades de la flota")
    # Naves
    destructor = NaveEstelar("ID-EXEC-01", 1138, "Vengador", ["Motor Hiperimpulsor"], 37000, 2500, Clase.EJECUTOR)
    estacion = EstacionEspacial("DS-2", 9999, "Estrella de la Muerte II", ["Panel de control"], 1200000, 50000, Ubicacion.ENDOR)
    caza = CazaEstelar("TIE-IN-01", 7777, "Interceptor TIE", ["Generador Deflector"], 1)
    imperio.registrar_unidad(destructor)
    imperio.registrar_unidad(estacion)
    imperio.registrar_unidad(caza)
    
    #imprimimos las naves
    print(f"  -> {destructor}")
    print(f"  -> {estacion}")
    print(f"  -> {caza}")

    # 2. Prueba de flujo normal (operario y comandante)
    print("\nProbando operaciones normales de stock")
    # Operario suma stock
    imperio.actualizar_stock("Base Starkiller", "Motor Hiperimpulsor", 3) 
    # Comandante adquiere repuesto (quedaban 8, coge 2, deben quedar 6)
    imperio.adquirir_repuesto(destructor, "Motor Hiperimpulsor", 2)

    # 3. Gestión de Excepciones MUY IMPORTANTE
    print("\nProbando captura y tratamiento de excepciones")

    #Forzamos StockInsuficienteError
    try:
        print("  - Intentando adquirir más escudos de los que hay disponibles...")
        imperio.adquirir_repuesto(caza, "Generador Deflector", 10)
    except StockInsuficienteError as e:
        print(f"{e}")

    #Forzamos RepuestoNoEncontradoError
    try:
        print("  - Intentando buscar un repuesto que no existe en el catálogo...")
        imperio.adquirir_repuesto(destructor, "Cristal Kyber", 1)
    except RepuestoNoEncontradoError as e:
        print(f"{e}")

    #Ponemos una ubicacion invalida para que salte el error
    try:
        print("  - Intentando crear una Estación Espacial en una ubicación inválida...")
        estacion_erronea = EstacionEspacial("DS-ERROR", 000, "Estación Falsa", [], 10, 0, "Tatooine")
    except ValueError as e:
        print(f"{e}")

    #Intentamos poner un stock negativo
    try:
        print("  - Intentando establecer un stock negativo en un repuesto...")
        escudo.set_cantidad(-5)
    except ValueError as e:
        print(f"{e}")

    print("\n--- Pruebas finalizadas con éxito ---")