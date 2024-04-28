from utilities import borrarPantalla, gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
import time

class Menu:
    def __init__(self,titulo="",opciones=[],col=6,fil=1):
        self.titulo=titulo
        self.opciones=opciones
        self.col=col
        self.fil=fil
        
    def menu(self):
        gotoxy(self.col,self.fil);print(self.titulo)
        self.col-=5
        for opcion in self.opciones:
            self.fil +=1
            gotoxy(self.col,self.fil);print(opcion)
        gotoxy(self.col+5,self.fil+2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ") 
        return opc   

class Valida:
    def solo_numeros(self,mensajeError,col,fil):
        while True: 
            gotoxy(col,fil)            
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col,fil);print(mensajeError)
                time.sleep(1)
                gotoxy(col,fil);print(" "*20)
        return valor

    def solo_letras(self,mensaje,mensajeError): 
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            if valor.isalpha():
                break
            else:
                print("          ------><  | {} ".format(mensajeError))
        return valor

    def solo_decimales(self,mensaje,mensajeError):
        while True:
            valor = str(input("          ------>   | {} ".format(mensaje)))
            try:
                valor = float(valor)
                if valor > float(0):
                    break
            except:
                print("          ------><  | {} ".format(mensajeError))
        return valor
    
    def cedula():
        pass
    
    def validar_letras(Frase):
        while True:
            nombre = input(f"{Frase}")
            if nombre.isalpha():
                return nombre.capitalize()
            else:
                print(yellow_color+"El campo solo puede contener letras.")
                
                # print(" " * 40)
    def validar_numeros(Frase):
        while True:
            numero = input(f"{Frase}")
            if numero.isdigit():
                return numero
            else:
                print(yellow_color+"El campo solo puede contener números enteros.")
    def validar_decimales(Frase):
        while True:
            numero = input(f"{Frase}")
            if numero.replace('.', '', 1).isdigit():  # Remueve un punto decimal y luego verifica si el resto es un número
                return numero
            else:
                print(yellow_color+"El campo solo puede contener números decimales.")

    def validar_dni(Frase):
        while True:
            dni = input(yellow_color+"Ingrese el DNI del cliente (10 dígitos): ")
            if dni.isdigit() and len(dni) == 10:
                return dni
            else:
                print(yellow_color+"El DNI ingresado no es válido.")
            
                # print(" " * 40)

if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if(opciones_menu==1):
      numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
      print("Número validado:", numero_validado)
    
    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)
    
    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)
    
    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)