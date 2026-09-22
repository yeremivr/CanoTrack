import os
from abc import ABC, abstractmethod
import random
import pandas as pd
import matplotlib.pyplot as plt

# Colores terminal
VERDE = "\033[92m"
ROJO = "\033[91m"
AZUL = "\033[94m"
CIAN = "\033[0;36m"
MORADO = "\033[0;35m"
AMARILLO = "\033[0;33m"
GRISOSCURO = "\033[1;30m"
ROJOCLARO = "\033[1;31m"
RESET = "\033[0m"

class Perro(ABC):
    def __init__(self,nombre,pista,raza,velocidad_base):
        self.__nombre=nombre
        self.__pista=pista 
        self.__raza=raza
        self.__velocidad_base=velocidad_base
        self.__cantidad_victorias=0
        self.__velocidades=[]
        self.__carreras_participadas=0
        self.__velocidad_promedio=0

    @property
    def nombre(self):return self.__nombre
    @property
    def pista(self):return self.__pista
    @property
    def raza(self):return self.__raza
    @property
    def velocidad_base(self):return self.__velocidad_base
    @property
    def cantidad_victorias(self):return self.__cantidad_victorias
    @property
    def velocidades(self):return self.__velocidades
    @property
    def carreras_participadas(self):return self.__carreras_participadas
    @property
    def velocidad_promedio(self):return self.__velocidad_promedio
    
    @cantidad_victorias.setter
    def cantidad_victorias(self,cantidad_victorias):
        self.__cantidad_victorias=cantidad_victorias
    @carreras_participadas.setter
    def carreras_participadas(self,carreras_participadas):
        self.__carreras_participadas=carreras_participadas
    @velocidad_promedio.setter
    def velocidad_promedio(self,velocidad_promedio):
        self.__velocidad_promedio=velocidad_promedio
    
    @abstractmethod
    def calcular_velocidad_final(self):
        pass

    def sumar_victoria(self):
        self.__cantidad_victorias += 1

    def calcular_velocidad_promedio(self):
        if len(self.velocidades) == 0:
            return 0
        return round(sum(self.velocidades) / len(self.velocidades),2)
    
    def __str__(self):
        return f"{self.__nombre}"

class Perro_Mediano(Perro):
    def __init__(self,nombre,pista,raza,velocidad_base):
        super().__init__(nombre,pista,raza,velocidad_base)

    def calcular_velocidad_final(self):
        velocidad_extra=random.randint(1,15+1)
        velocidad_final= self.velocidad_base + velocidad_extra
        self.velocidades.append(velocidad_final)
        self.carreras_participadas += 1
        return velocidad_final
    
    def sumar_victoria(self):
        return super().sumar_victoria()
    
    def calcular_velocidad_promedio(self):
        return super().calcular_velocidad_promedio()
    
    def __str__(self):
        return super().__str__()

class Perro_Grande(Perro):
    def __init__(self,nombre,pista,raza,velocidad_base):
        super().__init__(nombre,pista,raza,velocidad_base)

    def calcular_velocidad_final(self):
        velocidad_extra=random.randint(1,20+1)
        velocidad_final= self.velocidad_base + velocidad_extra
        self.velocidades.append(velocidad_final)
        self.carreras_participadas += 1
        return velocidad_final
    
    def sumar_victoria(self):
        return super().sumar_victoria()
    
    def calcular_velocidad_promedio(self):
        return super().calcular_velocidad_promedio()
    
    def __str__(self):
        return super().__str__()

class Carrera():
    def __init__(self,id,duracion):
        self.__id=id
        self.__duracion=duracion
        self.__lista_participantes=[]
        self.__resultados=[]
    
    @property
    def id(self):return self.__id
    @property
    def duracion(self):return self.__duracion
    @property
    def lista_participantes(self):return self.__lista_participantes
    @property
    def resultados(self):return self.__resultados

    def agregar_perro(self,perro):
        self.__lista_participantes.append(perro)
    
    def validar_existencia_pista(self,pista):
        for perro in self.lista_participantes:     
            if perro.pista == pista:
                return True, f"Pista ocupada por {perro.nombre}"
        return False,""

    def obtener_distancia_final(self,lista):
        return lista[1]
    
    def generar_carrera(self,duracion):
        for perro in self.lista_participantes:
            distancia_recorrida=perro.calcular_velocidad_final()*duracion 
            self.resultados.append([perro,distancia_recorrida]) #guardamos todos los datos del perro y lo asociamos con su distania recorrida
        self.resultados.sort(key=self.obtener_distancia_final,reverse=True)
        self.resultados[0][0].sumar_victoria() #al estar ordenado de mayor a menos el primer item que es el perro hace q aumente su cantidad de victorias
        for perro in self.lista_participantes:
            perro.velocidad_promedio = perro.calcular_velocidad_promedio()

    def mostrar_resultados(self):
        return self.resultados[0]
    
    def __str__(self):
        return f"\t{self.id} |  {self.duracion} min  |       {len(self.lista_participantes)}       |  {self.resultados[0][0]}  | {self.resultados[1][1]} metros"
    
class Canodromo():
    def __init__(self,nombre):
        self.__nombre=nombre
        self.__lista_perros=[]
        self.__lista_carreras=[]
        self.cargar_perros()
        self.cargar_carreras()
    
    @property
    def nombre(self):return self.__nombre
    @property
    def lista_perros(self):return self.__lista_perros
    @property
    def lista_carreras(self):return self.__lista_carreras
    
    def cargar_perros(self):
        #Carga los perros existentes desde el CSV
        try:
            df_perros = pd.read_csv("archivo_perros.csv",sep=",")
            for _, fila in df_perros.iterrows():
                if fila["raza"] == "mediano":
                    perro = Perro_Mediano(fila["nombre"], fila["pista"], fila["raza"], 
                                        fila["velocidad_base"])
                else:
                    perro = Perro_Grande(fila["nombre"], fila["pista"], fila["raza"], 
                                       fila["velocidad_base"])
                self.lista_perros.append(perro)
                perro.cantidad_victorias= fila["cantidad_victorias"]
                perro.velocidad_promedio= fila["promedio_velocidad"]
                perro.carreras_participadas= fila["carreras_participadas"]
            print(f"✅ {len(self.__lista_perros)} perros cargados desde CSV")
        except Exception as e:
            print(f"❌ Error cargando perros: {e} ❌")
    
    def actualizar_perros_csv(self):
        #Actualiza el CSV con los perros existentes
        datos_perros = []
        for perro in self.__lista_perros:
            datos_perros.append({
                "nombre": perro.nombre,
                "pista": perro.pista,
                "raza": perro.raza,
                "velocidad_base": perro.velocidad_base,
                "promedio_velocidad": perro.calcular_velocidad_promedio(),
                "cantidad_victorias": perro.cantidad_victorias,
                "carreras_participadas": perro.carreras_participadas
            })
        
        df_perros = pd.DataFrame(datos_perros)
        df_perros.to_csv("archivo_perros.csv", index=False)
   
    def registrar_perro(self,nombre,pista,raza,velocidad_base):
        if raza == "mediano":
            perro=Perro_Mediano(nombre,pista,raza,velocidad_base)
            self.lista_perros.append(perro)
        else:
            perro=Perro_Grande(nombre,pista,raza,velocidad_base)
            self.lista_perros.append(perro)
        self.actualizar_perros_csv()
    
    def cargar_carreras(self):
        try:  
            df_carreras = pd.read_csv("archivo_carreras.csv", sep=",")
            carreras_agrupadas = df_carreras.groupby("id")
            for id_carrera, grupo in carreras_agrupadas:
                duracion = grupo.iloc[0]["duracion"]
                carrera = Carrera(id_carrera, duracion)
                for _, fila in grupo.iterrows():
                    nombre = fila["nombre_perro"]
                    perro_encontrado = None 
                    for perro in self.lista_perros:
                        if perro.nombre == nombre:
                            perro_encontrado = perro
                            break
                        
                    if perro_encontrado:
                        carrera.agregar_perro(perro_encontrado)
                        velocidad = fila["velocidad"]
                        distancia = fila["distancia"]
                        perro_encontrado.velocidades.append(velocidad)
                        carrera.resultados.append([perro_encontrado, distancia])
                    else:
                        print(f"  ⚠️Perro {nombre} no encontrado en el sistema⚠️")
                
                carrera.resultados.sort(key=carrera.obtener_distancia_final, reverse=True)
                self.lista_carreras.append(carrera)
            print(f"✅ {len(self.lista_carreras)} carreras cargadas desde CSV")
            
        except FileNotFoundError:
            print("📁 Archivo 'archivo_carreras.csv' no encontrado. Se iniciará sin carreras previas.")
        except Exception as e:
            print(f"❌ Error cargando carreras: {e}")

    def actualizar_carreras_csv(self):
        datos_carreras = []
        for carrera in self.lista_carreras:
            if carrera.resultados: 
                for i, (perro, distancia) in enumerate(carrera.resultados, 1): 
                    #calcula la velocidad basada del perro en la carrera puesto que si bien es random, nosotros ya le asignamos en los datos del
                    #archivo_carrera csv
                    velocidad = round(distancia / carrera.duracion, 2)
                    datos_carreras.append({
                        "id": carrera.id,
                        "duracion": carrera.duracion,
                        "cantidad_participantes": len(carrera.lista_participantes),
                        "nombre_perro": perro.nombre,
                        "raza": perro.raza,
                        "velocidad": velocidad,
                        "distancia": distancia,
                        "puesto": i
                    })
        df_carreras = pd.DataFrame(datos_carreras)
        df_carreras.to_csv("archivo_carreras.csv", index=False)
     
    def retornar_df_perros(self): #creamos esta funcion para poder utilizar los datos del dataframe en otras funciones
        df_perros = pd.read_csv("archivo_perros.csv",sep=",")
        return df_perros
    
    def retornar_df_carreras(self):
        df_carreras = pd.read_csv("archivo_carreras.csv",sep=",")
        return df_carreras
    
    def mostrar_estadisticas_generales(self):
        try:
            df_perros = pd.read_csv("archivo_perros.csv")
            if len(df_perros) == 0:
                print("\tNo hay perros registrados para mostrar estadísticas")
                return
        except FileNotFoundError:
            print("\t❌ Error: No se encontró el archivo 'perros_registrados.csv'")
            return
        except Exception as e:
            print(f"\t❌ Error leyendo perros: {e}")
            return
        # Cargar datos de carreras desde CSV externo
        try:
            df_carreras = pd.read_csv("archivo_carreras.csv",sep=",")
            # Calcular distancias máximas desde CSV
            distancias_por_perro = {}
            for _, fila in df_carreras.iterrows():
                nombre = fila["nombre_perro"]
                distancia = fila["distancia"]
                if nombre not in distancias_por_perro:
                    distancias_por_perro[nombre] = []
                distancias_por_perro[nombre].append(distancia)
        except FileNotFoundError:
            print("\t⚠️ Advertencia: No se encontró 'archivo_carreras.csv', algunas estadísticas pueden estar incompletas")
            distancias_por_perro = {}
        except Exception as e:
            print(f"\t⚠️ Advertencia: Error leyendo carreras: {e}")
            distancias_por_perro = {}

        # EXTRAER DATOS DIRECTAMENTE DEL CSV
        nombres = df_perros['nombre'].tolist()
        velocidades_prom = df_perros['promedio_velocidad'].tolist()
        victorias = df_perros['cantidad_victorias'].tolist()
        
        # Distancias máximas desde CSV de carreras
        distancias_max = []
        for nombre in nombres:
            if nombre in distancias_por_perro:
                distancias_max.append(max(distancias_por_perro[nombre]))
            else:
                distancias_max.append(0)

        #crea los gráficos
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        #velocidad promedio por perro
        ax1.bar(nombres, velocidades_prom, color='skyblue')
        ax1.set_title('Velocidad Promedio por Perro')
        ax1.set_ylabel('Velocidad (m/s)')
        ax1.tick_params(axis='x', rotation=45)

        #distancia máxima por perro
        ax2.bar(nombres, distancias_max, color='lightgreen')
        ax2.set_title('Distancia Máxima Alcanzada por Perro')
        ax2.set_ylabel('Distancia (m)')
        ax2.tick_params(axis='x', rotation=45)

        #Victorias por perro
        ax3.bar(nombres, victorias, color='orange')
        ax3.set_title('Victorias por Perro')
        ax3.set_ylabel('Número de Victorias')
        ax3.tick_params(axis='x', rotation=45)

        #Porcentaje de victorias
        total_victorias = sum(victorias)
        if total_victorias > 0:
            nombres_con_victorias = []
            victorias_con_victorias = []
            for i, victoria in enumerate(victorias):
                if victoria > 0:
                    nombres_con_victorias.append(nombres[i])
                    victorias_con_victorias.append(victoria)
            if nombres_con_victorias:
                ax4.pie(victorias_con_victorias, labels=nombres_con_victorias, autopct='%1.1f%%')
                ax4.set_title('Porcentaje de Victorias')
            else:
                ax4.text(0.5, 0.5, 'No hay victorias aún', ha='center', va='center')
                ax4.set_title('Porcentaje de Victorias')
        else:
            ax4.text(0.5, 0.5, 'No hay victorias aún', ha='center', va='center')
            ax4.set_title('Porcentaje de Victorias')

        plt.tight_layout()
        plt.show()

    def eliminar_carrera(self,id):
        for carrera in self.lista_carreras:
            if carrera.id==id:
                self.lista_carreras.remove(carrera)
                self.actualizar_carreras_csv()

    def registrar_carrera(self,id,duracion):
        carrera=Carrera(id,duracion)
        self.__lista_carreras.append(carrera)
        return carrera
    
    def validar_existencia_nombre(self,nombre):
        if not nombre.isalpha():
            return 1,False,f"{ROJO}Dato inválido{RESET}❌"
        else:
            for perro in self.lista_perros:
                if perro.nombre == nombre:
                     return 3,True,perro
            return 2,False,f"{ROJO}¡El perro no existe!{RESET}"

    def validar_ingreso_pista(self,pista):
        if 1<=pista<=7:
           return True,pista
        else:
           return False,f"{ROJO}Pista invalida{RESET}❗"
    
    def validar_raza(self,raza):
        if raza.isalpha():
            if raza in ["mediano","grande"]:
                return 3,True,""
            else:
                return 1,False,f"{ROJO}Raza invalida{RESET}"
        else:
            return 2,False,f"{ROJO}Dato inválido{RESET}"
    
    def validar_velocidad(self,velocidad_base):
        if 1<=velocidad_base<=10:
            return True
        else:
            return False
    
    def validar_duracion(self,duracion):
        if 1<=duracion<=120:
            return True
        else:
            return False
        
    def buscar_carrera(self,id):
        if id>0:
             for carrera in self.__lista_carreras:
                 if carrera.id == id:
                    return 3,True,id
             else:
                return 1,False,f"\t{ROJO}Carrera no encontrada{RESET}❗"
        else:
            return 2,False,f"\t{ROJO}Id invalido{RESET}❗"
    
    def validar_existencia_carrera(self):
        if len(self.__lista_carreras)==0:
            return False,"\t{ROJO}tNo hay carreras registradas{RESET}"
        else:
            return True,""
    
    def validar_existencia_perro(self):
        if len(self.lista_perros)==0:
            return 1, False ,"\t❗Primero registre perros❗"
        elif len(self.lista_perros)==1:
            return 2, False ,"\t❗tDebe haber más de 1 perro registrado❗"
        else:
            return 3,True,""
    
    def obtener_cantidad_victorias(self,perro):
        return perro.cantidad_victorias
    
    def mostrar_perro_mayor_victorias(self):
        return max(self.lista_perros,key=self.obtener_cantidad_victorias)
    
    def validar_generar_carrera(self):
        pistas_usadas = []
        for perro in self.lista_perros:
            if perro.pista not in pistas_usadas:
                pistas_usadas.append(perro.pista)
        if len(pistas_usadas)>=2:
            return True
        else:
            return False
        
admin=Canodromo("LasFijas")

#FUNCIONES VALIDACIONES

def validar_nombre(mensaje):
    while True:
        nombre=input(mensaje).capitalize()
        i,estado,dato=admin.validar_existencia_nombre(nombre)
        if estado==True:
            print(f"\t   El perro {dato.nombre} ya existe❗")
        else:
            if i==1:
                print("\t  ",dato)
            elif i==2:
                return nombre

def validar_pista(mensaje):
    while True:
        try:
            pista=int(input(mensaje))     
            estado,alerta=admin.validar_ingreso_pista(pista)  
            if estado==True:
                return pista
            else:
                print("\t",alerta)
        except ValueError:
            print(f"\t{ROJO}El dato debe ser numero entero{RESET}")
                
def validar_raza(mensaje):
    while True:
        raza=input(mensaje).lower()
        i,estado,alerta=admin.validar_raza(raza)
        if estado==True:
            return raza
        else:
            if i==1:
                print("\t",alerta)
            elif i==2:
                print("\t",alerta)

def validar_velocidad(mensaje):
    while True:
        try:
            velocidad_base=int(input(mensaje))
            if admin.validar_velocidad(velocidad_base) == True:
                return velocidad_base
            else:
                print(f"\t{ROJO}Velocidad fuera de rango❗{RESET}")
        except ValueError:
            print(f"\t{ROJO}El dato debe ser numero entero{RESET}")

def validar_duracion(mensaje):
    while True:
        try:
            duracion=int(input(mensaje))
            if admin.validar_duracion(duracion)==True:
                return duracion
            else:
                print(f"\t{ROJO}Duracion fuera de rango{RESET}❗")
        except ValueError:
            print(f"\t{ROJO}El dato debe ser numero entero{RESET}")
    
def validar_id(mensaje):
    while True:
        try:
            id=int(input(mensaje))
            i,estado,dato=admin.buscar_carrera(id)
            if estado==True:
                return dato
            else:
                if i==1 or i==2:
                    print("\t",dato)
        except ValueError:
            print(f"\t{ROJO}El dato debe ser numero entero{RESET}")

#FUNCIONES MAIN

def registrar_perro():
    print(f"\t\t {MORADO}REGISTRO DE PERRO{RESET}")
    print("\t----------------------------------")
    nombre=validar_nombre("Ingrese nombre: ")
    pista=validar_pista(f"Ingrese pista {CIAN}(1-7){RESET}: ")
    raza=validar_raza(f"Ingrese raza {CIAN}(mediano/grande){RESET}: ")
    velocidad_base=validar_velocidad(f"Ingrese velocidad base {CIAN}(1-10){RESET}: ")
    admin.registrar_perro(nombre,pista,raza,velocidad_base)
    print(f"\t🐶 {VERDE}Perro {nombre} registrado exitosamente!{RESET}✅")

def mostrar_perros(lista_perros):
    if len(lista_perros)==0:
        print("\tNo hay perros registrados")
    else:
        print(f"\t\t\t\t\t🐶{AMARILLO}LISTA DE PERROS🐶{RESET}")
        df_perros=admin.retornar_df_perros()
        print(df_perros.to_string(index=False))

def buscar_perro():
    if admin.lista_perros:
        while True:
         nombre=input("Ingrese nombre del perro: ").capitalize()
         i,estado,dato=admin.validar_existencia_nombre(nombre)
         if estado==True:
             return dato
         else:
             if i==1 or i==2:
                 print("\t",dato)
    else:
        print("\t❌No hay perros registrados❌")

def registrar_carrera():
    print(f"{MORADO}||REGISTRO DE CARRERA||{RESET}")
    
    if len(admin.lista_perros)>=2 and admin.validar_generar_carrera()==True :
        mostrar_perros(admin.lista_perros)
        id=len(admin.lista_carreras)+1
        print()
        duracion=validar_duracion("Ingrese duración: ")
        carrera=admin.registrar_carrera(id,duracion)
        print(f"\t\n  {AMARILLO}----Agregar participantes----{RESET}")
        perro=buscar_perro()
        print(f"\tPerro {perro.nombre} ha sido agregado✅")
        carrera.agregar_perro(perro)
        while True:
            agregar_perro_carrera(carrera)
            opcion=input("¿Desea agregar otro perro a la carrera? (S/N): ").upper()
            match opcion:
                case "S":
                    pass
                case "N":
                    break
                case _:
                    print("\t  Opción no válida❗")
                    pass
        if len(carrera.lista_participantes)<2:
            admin.eliminar_carrera(carrera.id)
            print(f"\t\t❌{ROJO}No se pudo generar la carrera{RESET}❌")
        else:
            carrera.generar_carrera(duracion)
            admin.actualizar_carreras_csv()
            admin.actualizar_perros_csv()
            os.system("cls")
            print("\tID | Duracion | Participantes | Ganador | Distancia")
            print(carrera)
            

    elif len(admin.lista_perros)>=2 and admin.validar_generar_carrera()==False:
        print("\t   Los perros registrados estan inscritos en la misma pista❗")
    else:
        print("\t  ❌No hay suficientes perros registrados❌\n")

def agregar_perro_carrera(carrera):
     while True:
             perro=buscar_perro()
             if perro in carrera.lista_participantes:
                print(f"\tEl perro {perro.nombre} ya está inscrito❗")
                break
             else:
                estado,msj=carrera.validar_existencia_pista(perro.pista)
                if estado==True:
                    print("\t  ",msj)
                else:
                    print(f"\tPerro {perro.nombre} ha sido agregado✅")
                    carrera.agregar_perro(perro)
                    break
                break

def mostrar_carrera_especifica():
    estado,msj=admin.validar_existencia_carrera()
    if estado==True:
        id=validar_id("Introduzca id de carrera a mostrar: ")
        df_carreras=admin.retornar_df_carreras()
        carrera_agrupada=df_carreras.groupby("id").get_group(id)
        id=carrera_agrupada["id"].iloc[0] #con el.iloc[0] accedo al primer valor sin importar el índice
        duracion=carrera_agrupada["duracion"].iloc[0]
        cantidad_participantes=carrera_agrupada["cantidad_participantes"].iloc[0]
        #crear DataFrame solo con los datos de los perros (sin las columnas de resumen)
        datos_perros=carrera_agrupada[["nombre_perro","raza","velocidad", "distancia", "puesto"]].copy()
        os.system("cls")
        print(f"\n\t\t{MORADO}INFORMACIÓN ESPECIFICA DE CARRERA{RESET}")
        print(f"ID de la carrera: {id}\tDuración: {duracion}\tCantidad de participantes: {cantidad_participantes}")
        print(f"\n\t\t   {AMARILLO}|PARTICIPANTES|{RESET}")
        print(datos_perros.to_string(index=False))
        print()
    else:
        print(msj)

def mostrar_carreras(lista_carreras):
    if len(lista_carreras)==0:
        print("\tNo hay perros registrados")
    else:
        print(f"\t\t\t\t{AMARILLO}🏁LISTA DE CARRERAS🏁{RESET}")
        df_carreras=admin.retornar_df_carreras()
        carreras_agrupadas=df_carreras.groupby("id")
        for id_carrera,grupos in carreras_agrupadas:
            print(grupos.to_string(index=False))
            print("="*88)
        print()

def validar_opciones_menu():
    while True:
        try:
            opt = int(input(f"{CIAN}\t\tIngrese una opcion:{RESET} "))
            if 1 <= opt <= 7:
                return opt
            else:
                print(f"{ROJO}\t\tError, opcion fuera de rango...{RESET}\n")
        except ValueError:
            print(f"{ROJO}\t\tError, solo valores numericos..{RESET}\n")

def presentacion():
    #limpia los errores visuales q sale en la parte superior
    #os.system("cls" if os.name == "nt" else "clear")
    print(rf"{VERDE}           _________        _                   __________   _______     ________   __________              __________") 
    print(rf"          |                / \       |\      | |          | |       \   |        | |          | |\      /| |          |")            
    print(rf"          |               /   \      | \     | |          | |        \  |        | |          | | \    / | |          |")            
    print(rf"          |              /     \     |  \    | |          | |         | |________| |          | |  \  /  | |          |")            
    print(rf"          |             /_______\    |   \   | |          | |         | |     \    |          | |   \/   | |          |")                 
    print(rf"          |            /         \   |    \  | |          | |         | |      \   |          | |        | |          |")         
    print(rf"          |           /           \  |     \ | |          | |        /  |       \  |          | |        | |          |")                
    print(rf"          |_________ /             \ |      \| |__________| |_______/   |        \ |__________| |        | |__________|{RESET}")
    input(f"\n\t\t\t\t\t\t[Pulse ENTER para continuar ...]")

def menu():
    print(f"{AMARILLO}1.{RESET} Registrar perros al sistema")
    print(f"{AMARILLO}2.{RESET} Mostrar perros registrados")
    print(f"{AMARILLO}3.{RESET} Registrar y generar carrera")
    print(f"{AMARILLO}4.{RESET} Mostrar información de carrera específica")
    print(f"{AMARILLO}5.{RESET} Mostrar todos los gráfico de carreras y perros📈")
    print(f"{AMARILLO}6.{RESET} Mostrar carreras registradas")
    print(f"{AMARILLO}7.{RESET} Salir")

def opcion_seguir_registrando(mensaje):
    while True:
            opcion=input(mensaje).upper()
            if opcion in ["S","N"]:
                return opcion
            else:
                print("\tOpcion inválida")

def main():
    presentacion()
    os.system("cls")
    print(f"{ROJOCLARO}\t\t\tBIENVENIDOS AL CANÓDROMO{RESET}\n")
    while True:
        menu()
        opt = validar_opciones_menu()
        match opt:
            case 1:
                 while True:
                     os.system("cls")
                     registrar_perro()
                     opcion=opcion_seguir_registrando(f"\n{AMARILLO}Desea seguir registrando perros? (s/n):{RESET} ")
                     if opcion =="N":
                         os.system("cls")
                         break
                     else: 
                        os.system("cls")
                        pass
                     os.system("cls")
            case 2:
                 os.system("cls")
                 print("="*100)
                 mostrar_perros(admin.lista_perros)
                 print("="*100,"\n")
            case 3:
                 os.system("cls")
                 registrar_carrera()
            case 4:
                 os.system("cls")
                 mostrar_carrera_especifica()
            case 5:
                 os.system("cls")
                 admin.mostrar_estadisticas_generales()
            case 6:
                 os.system("cls")
                 mostrar_carreras(admin.lista_carreras)
            case 7:
                 os.system("cls")
                 print(f"{GRISOSCURO}\n\t\tSaliendo del programa...😞{RESET}\n")
                 break

#MAIN
main()