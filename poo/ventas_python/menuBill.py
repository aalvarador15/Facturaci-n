from components import Menu,Valida
from utilities import borrarPantalla,gotoxy
from utilities import reset_color,red_color,green_color,yellow_color,blue_color,purple_color,cyan_color
from clsJson import JsonFile
from company  import Company
from customer import RegularClient,VipClient
from sales import Sale
from product  import Product
from iCrud import ICrud
import datetime
import time,os
from functools import reduce

path, _ = os.path.split(os.path.abspath(__file__))
# Procesos de las Opciones del Menu Facturacion
class CrudClients(ICrud):
    def create(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2 );print(purple_color+"Registro de Cliente")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,6);print(purple_color+"Seleccione el tipo de cliente:")
        gotoxy(5,7);print(red_color+"1) Cliente Regular")
        gotoxy(5,8);print(red_color+"2) Cliente VIP")
        gotoxy(5,9);tipo_cliente = input("Seleccione una opción: ")
        
        if tipo_cliente == "1":
            gotoxy(10,10);print(cyan_color+"Cliente Regular")
            gotoxy(10,14);nombre =Valida.validar_letras("Ingresa el nombre ")
            gotoxy(10,15);apellido =Valida.validar_letras("Ingresa el apellido ")
            gotoxy(10,16);dni =Valida.validar_dni("Ingrese su Dni ")
            gotoxy(10,17);card = input("¿El cliente tiene tarjeta de descuento? (s/n): ").lower() == "s"
            new_client = RegularClient(nombre, apellido, dni, card)
        elif tipo_cliente == "2":
            gotoxy(10,10);print(cyan_color+"Cliente VIP")
            gotoxy(10,14);nombre =Valida.validar_letras("Ingrese su nombre ")
            gotoxy(10,15);apellido =Valida.validar_letras("Ingrese su apellido ")
            gotoxy(10,16);dni =Valida.validar_dni("Ingrese su Dni ")
            new_client = VipClient(nombre, apellido, dni)
        else:
            gotoxy(6,7);print("Opción inválida")
            return
        
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        clients.append(new_client.getJson())
        json_file.save(clients)
        gotoxy(50,25);print(red_color+"Cliente registrado exitosamente! 😎")
        time.sleep(2)
    def update(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color + "*" * 90 + reset_color)
        gotoxy(30,2);print(purple_color + "Actualización de Cliente")
        gotoxy(17,3);print(blue_color + Company.get_business_name())
        dni = Valida.validar_dni("Ingrese el DNI del cliente que desea actualizar ")
        json_file = JsonFile(path + '/archivos/clients.json')
        
        # Cargar todos los clientes del archivo JSON
        clients = json_file.read()
        
        # Buscar el cliente por su DNI
        client_found = False
        for client in clients:
            if client["dni"] == dni:
                client_found = True
                print("Cliente encontrado:")
                print(f"Nombre: {client['nombre']}")
                print(f"Apellido: {client['apellido']}")
                print(f"DNI: {client['dni']}")
                print()
                # Solicitar nueva información para el cliente
                new_nombre =Valida.validar_letras("Ingrese el nuevo nombre (De enter si desea mantener el mismo) ")
                new_apellido =Valida.validar_letras("Ingrese el nuevo apellido (De enter si desea mantener el mismo) ")
                
                # Actualizar la información si se proporcionó
                if new_nombre:
                    client['nombre'] = new_nombre
                if new_apellido:
                    client['apellido'] = new_apellido
                break  # Salir del bucle después de encontrar el cliente
                
        if client_found:
            # Guardar todos los clientes nuevamente en el archivo JSON
            json_file.save(clients)
            gotoxy(50,25);print(red_color+"Cliente actualizado exitosamente! 😎")
        else:
            gotoxy(50,25);print(red_color+"Cliente no encontrado. 😢")
        time.sleep(2)
  
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(purple_color+"Eliminación de Cliente")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        dni =Valida.validar_dni("Ingrese el DNI del cliente que desea eliminar ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.read()
        
        filtered_clients = [client for client in clients if client['dni'] != dni]
        
        if len(filtered_clients) < len(clients):
            json_file.save(filtered_clients)
            gotoxy(50,25);print(red_color+"Cliente eliminado exitosamente! 😎")
        else:
            gotoxy(50,25);print(red_color+"Cliente no encontrado.😢")
        time.sleep(2)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(30,2);print(purple_color+"Consulta de Cliente")
        # gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(2,4);dni =Valida.validar_dni("Ingrese DNI del cliente ")
        json_file = JsonFile(path+'/archivos/clients.json')
        clients = json_file.find("dni", dni)
        
        if clients:
            client = clients[0]
            print(f"Nombre: {client['nombre']}")
            print(f"Apellido: {client['apellido']}")
            print(f"DNI: {client['dni']}")
        else:
            gotoxy(50,25);print(red_color+"Cliente no encontrado.😢")
        input("Presione una tecla para continuar...")    

        
class CrudProducts(ICrud):
    def create(self):
        borrarPantalla()
        gotoxy(2, 1);print(green_color + "=" * 90 + reset_color)
        gotoxy(30,2);print(purple_color + "Registro de Producto")
        gotoxy(5,6);description = Valida.validar_letras("Ingrese la descripción del producto ")
        gotoxy(5,8);price = float(Valida.validar_decimales("Ingrese el precio del producto "))
        gotoxy(5,10);stock = int(Valida.validar_numeros("Ingrese el stock inicial del producto "))
        
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()
        
        # Obtener el último ID utilizado
        last_id = max([product['id'] for product in products]) if products else 0
        
        # Verificar si el producto ya existe
        existing_product = next((product for product in products if product['descripcion'] == description), None)
        
        if existing_product:
            print(red_color+"El producto ya existe 😉")
            print(f"ID: {existing_product['id']}, Descripción: {existing_product['descripcion']}, Precio: {existing_product['precio']}, Stock: {existing_product['stock']}")
            actualizar = input("¿Desea actualizar este producto? (s/n): ").lower()
            if actualizar == 's':
                # Actualizar el producto existente
                id_producto = existing_product['id']
                description = input(f"Ingrese la nueva descripción del producto (actual: {existing_product['descripcion']}): ")
                price = float(input(f"Ingrese el nuevo precio del producto (actual: {existing_product['precio']}): "))
                stock = int(input(f"Ingrese el nuevo stock del producto (actual: {existing_product['stock']}): "))
                
                existing_product['descripcion'] = description if description else existing_product['descripcion']
                existing_product['precio'] = price if price else existing_product['precio']
                existing_product['stock'] = stock if stock else existing_product['stock']
                
                # Guardar los cambios en el archivo JSON
                json_file.save(products)
                gotoxy(50,25);print(red_color+"Producto actualizado exitosamente! 😎")
            else:
                gotoxy(50,25);print(red_color+"Registro cancelado.")
        else:
            # Crear un nuevo producto con un nuevo ID único
            new_id = last_id + 1
            new_product = Product(id=new_id, descrip=description, preci=price, stock=stock)
            products.append(new_product.getJson())
            json_file.save(products)
            gotoxy(50,25);print(red_color+"Producto registrado exitosamente! 😎")
        time.sleep(2)


    def update(self):
        borrarPantalla()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2 );print(purple_color+"Registro de Cliente")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        id_producto = Valida.validar_numeros(int("Ingrese el ID del producto que desea actualizar "))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        # Buscar el producto por su ID
        found = False
        updated_products = []
        for product in products:
            if product['id'] == id_producto:
                found = True
                # Si se encuentra el producto, solicitar nueva información
                description = Valida.validar_letras(f"Ingrese la nueva descripción del producto (actual: {product['descripcion']}): ")
                price = float(Valida.validar_decimales(f"Ingrese el nuevo precio del producto (actual: {product['precio']}): "))
                stock = int(Valida.solo_numeros(f"Ingrese el nuevo stock del producto (actual: {product['stock']}): "))
                # Actualizar la información si se proporcionó
                product['descripcion'] = description if description else product['descripcion']
                product['precio'] = price if price else product['precio']
                product['stock'] = stock if stock else product['stock']
            updated_products.append(product)

        if found:
            # Guardar los cambios en el archivo JSON
            json_file.save(updated_products)
            gotoxy(50,25);print(red_color+"Producto actualizado exitosamente 😎!")
        else:
            gotoxy(50,25);print(red_color+"Producto no encontrado.😥")
        time.sleep(2)

    def delete(self):
        borrarPantalla()
        gotoxy(2, 1)
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2 );print(purple_color+"Eliminación del producto")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        id_producto = Valida.validar_numeros(int("Ingrese el ID del producto que desea eliminar "))
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        filtered_products = [product for product in products if product['id'] != id_producto]

        if len(filtered_products) < len(products):
            json_file.save(filtered_products)
            gotoxy(50,25);print(red_color+"Producto eliminado exitosamente!😎")
        else:
            gotoxy(50,25);print(red_color+"Producto no encontrado.😥")
        time.sleep(2)

    def consult(self):
        borrarPantalla()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(purple_color+"Consulta del producto")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        json_file = JsonFile(path + '/archivos/products.json')
        products = json_file.read()

        if products:
            print("""ID   Descripción   Precio   Stock""")
            for product in products:
                print(f"""{product['id']} {product['descripcion']} {product['precio']} {product['stock']}""")

            # Opción de búsqueda por descripción
            search_term = Valida.validar_letras("Ingrese la descripción del producto a buscar (o dejar en blanco para omitir )").strip()
            if search_term:
                found = False
                for product in products:
                    if search_term.lower() in product['descripcion'].lower():
                        found = True
                        print(f"ID: {product['id']}, Descripción: {product['descripcion']}, Precio: {product['precio']}, Stock: {product['stock']}")
                if not found:
                    gotoxy(30,2);print(red_color+"No se encontraron productos con esa descripción.")
        else:
            gotoxy(50,25);print(red_color+"No hay productos registrados. 😢")

        input("Presione una tecla para continuar...")

class CrudSales(ICrud):
    def create(self):
        # cabecera de la venta
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(purple_color+"Registro de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,4);print(f"Factura#:F0999999 {' '*3} Fecha:{datetime.datetime.now()}")
        gotoxy(66,4);print("Subtotal:")
        gotoxy(66,5);print("Decuento:")
        gotoxy(66,6);print("Iva     :")
        gotoxy(66,7);print("Total   :")
        gotoxy(15,6);print("Cedula:")
        dni=validar.solo_numeros("Error: Solo numeros",23,6)
        json_file = JsonFile(path+'/archivos/clients.json')
        client = json_file.find("dni",dni)
        if not client:
            gotoxy(35,6);print(red_color+"Cliente no existe")
            return
        client = client[0]
        cli = RegularClient(client["nombre"],client["apellido"], client["dni"], card=True) 
        sale = Sale(cli)
        gotoxy(35,6);print(cli.fullName())
        gotoxy(2,8);print(green_color+"*"*90+reset_color) 
        gotoxy(5,9);print(purple_color+"Linea") 
        gotoxy(12,9);print("Id_Articulo") 
        gotoxy(24,9);print("Descripcion") 
        gotoxy(38,9);print("Precio") 
        gotoxy(48,9);print("Cantidad") 
        gotoxy(58,9);print("Subtotal") 
        gotoxy(70,9);print("n->Terminar Venta)"+reset_color)
        # detalle de la venta
        follow ="s"
        line=1
        while follow.lower()=="s":
            gotoxy(7,9+line);print(line)
            gotoxy(15,9+line);
            id=int(validar.solo_numeros("Error: Solo numeros",15,9+line))
            json_file = JsonFile(path+'/archivos/products.json')
            prods = json_file.find("id",id)
            if not prods:
                gotoxy(24,9+line);print(red_color+"Producto no existe")
                time.sleep(1)
                gotoxy(24,9+line);print(" "*20)
            else:    
                prods = prods[0]
                product = Product(prods["id"],prods["descripcion"],prods["precio"],prods["stock"])
                gotoxy(24,9+line);print(product.descrip)
                gotoxy(38,9+line);print(product.preci)
                gotoxy(49,9+line);qyt=int(validar.solo_numeros("Error:Solo numeros",49,9+line))
                gotoxy(59,9+line);print(product.preci*qyt)
                sale.add_detail(product,qyt)
                gotoxy(76,4);print(round(sale.subtotal,2))
                gotoxy(76,5);print(round(sale.discount,2))
                gotoxy(76,6);print(round(sale.iva,2))
                gotoxy(76,7);print(round(sale.total,2))
                gotoxy(74,9+line);follow=input() or "s"  
                gotoxy(76,9+line);print(green_color+"✔"+reset_color)  
                line += 1
        gotoxy(15,9+line);print(red_color+"Esta seguro de grabar la venta(s/n):")
        gotoxy(54,9+line);procesar = input().lower()
        if procesar == "s":
            gotoxy(15,10+line);print("😊 Venta Grabada satisfactoriamente 😊"+reset_color)
            # print(sale.getJson())  
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            ult_invoices = invoices[-1]["factura"]+1
            data = sale.getJson()
            data["factura"]=ult_invoices
            invoices.append(data)
            json_file = JsonFile(path+'/archivos/invoices.json')
            json_file.save(invoices)
        else:
            gotoxy(20,10+line);print(red_color+"🤣 Venta Cancelada 🤣"+reset_color)    
        time.sleep(2)    
    
    def update(self):
        borrarPantalla()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(purple_color+"Actualizacion de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        gotoxy(5,7);invoice_number = Valida.validar_numeros("Ingrese el número de factura que desea actualizar ")
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        if invoices:
            # Buscar la factura específica
            for invoice in invoices:
                if invoice["factura"] == int(invoice_number):
                    cliente = invoice["cliente"]
                    gotoxy(2,5);print(f"Número de Factura: {invoice['factura']}")
                    gotoxy(2,6);print(f"Fecha: {invoice['Fecha']}")
                    gotoxy(2,7);print(f"Cliente: {cliente}")
                    gotoxy(2,8);print(f"Total: {invoice['total']}")
                    gotoxy(2,9);print("\nDetalle de la Venta:")
                    detalles = invoice['detalle']
                    for i, detalle in enumerate(detalles, start=1):
                        print(f"{detalle['poducto']}: {detalle['cantidad']} x {detalle['precio']}")
                    print(green_color + "=" * 90 + reset_color)

                    # Opciones para modificar la factura
                    while True:
                        print(purple_color+"\nOpciones:")
                        print(red_color+"1. Modificar cantidad de un producto")
                        print(purple_color+"2. Eliminar un producto")
                        print(red_color+"3. Agregar un nuevo producto")
                        print(purple_color+"4. Terminar actualización")
                        option = input("Seleccione una opción: ")

                        if option == "1":
                            # Modificar cantidad de un producto en la factura
                            detalle_index = int(Valida.validar_numeros(green_color+"Ingrese el número de línea del detalle que desea modificar ")) - 1
                            if 0 <= detalle_index < len(detalles):
                                new_quantity = Valida.validar_numeros(green_color+"Ingrese la nueva cantidad ")
                                detalles[detalle_index]['cantidad'] = new_quantity
                                gotoxy(50,25);print("Cantidad modificada correctamente.😊")
                            else:
                                print("Número de línea inválido.")
                        elif option == "2":
                            # Eliminar un producto de la factura
                            detalle_index = int(Valida.validar_numeros(green_color+"Ingrese el número de línea del detalle que desea eliminar ")) - 1
                            if 0 <= detalle_index < len(detalles):
                                del detalles[detalle_index]
                                gotoxy(50,25);print(red_color+"Producto eliminado correctamente 😎.")
                            else:
                                print("Número de línea inválido.")
                        elif option == "3":
                            # Agregar un nuevo producto a la factura
                            product_id = Valida.validar_numeros(green_color+"Ingrese el ID del nuevo producto ")
                            product_quantity = Valida.validar_numeros(green_color+"Ingrese la cantidad del nuevo producto ")
                            json_file_products = JsonFile(path + '/archivos/products.json')
                            products = json_file_products.find("id", product_id)
                            if products:
                                product = products[0]
                                new_product = {
                                    'poducto': product['descripcion'],
                                    'precio': product['precio'],
                                    'cantidad': product_quantity
                                }
                                detalles.append(new_product)
                                gotoxy(50,25);print(red_color+"Producto agregado correctamente 😎.")
                            else:
                                gotoxy(50,25);print(red_color+"Producto no encontrado 😥.")
                        elif option == "4":
                            print(red_color+"Actualización de factura terminada.😉")
                            # Guardar los cambios en el archivo JSON
                            invoice['detalle'] = detalles
                            json_file.save(invoices)
                            break
                        else:
                            gotoxy(50,25);print("Opción inválida. Intente nuevamente.")
                    break
            else:
                gotoxy(50,25);print(red_color+"Factura no encontrada.😥")
        else:
            gotoxy(50,25);print(red_color+"No hay facturas disponibles.")
        input("Presione una tecla para continuar...")
    
    def delete(self):
        borrarPantalla()
        borrarPantalla()
        gotoxy(2,1);print(green_color+"*"*90+reset_color)
        gotoxy(30,2);print(purple_color+"Eliminacion de Venta")
        gotoxy(17,3);print(blue_color+Company.get_business_name())
        invoice_number =Valida.validar_numeros("Ingrese el número de factura que desea eliminar ")
        json_file = JsonFile(path + '/archivos/invoices.json')
        invoices = json_file.read()

        # Buscar la factura específica
        found = False
        updated_invoices = []
        for invoice in invoices:
            if invoice["factura"] == int(invoice_number):
                found = True
                # Mostrar la factura antes de eliminarla
                print(f"Factura encontrada:")
                print(f"Número de Factura: {invoice['factura']}")
                print(f"Fecha: {invoice['Fecha']}")
                print(f"Cliente: {invoice['cliente']}")
                print(f"Total: {invoice['total']}")
                print("\nDetalle de la Venta:")
                for detalle in invoice['detalle']:
                    print(f"{detalle['poducto']}: {detalle['cantidad']} x {detalle['precio']}")
                print(green_color + "=" * 90 + reset_color)

                # Confirmar la eliminación
                confirmacion = input("¿Está seguro que desea eliminar esta factura? (s/n): ").lower()
                if confirmacion == "s":
                    print(red_color+"Factura eliminada exitosamente.😎")
                else:
                    print(red_color+"Eliminación cancelada.😥")
            else:
                updated_invoices.append(invoice)

        if not found:
            print(red_color+"Factura no encontrada. 😥")

        # Guardar los cambios en el archivo JSON
        json_file.save(updated_invoices)
        time.sleep(2)
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Venta"+" "*35+"██")
        gotoxy(2,4);invoice= input(red_color+"Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.find("factura",invoice)
            print(blue_color+f"Impresion de la Factura#{invoice}")
            print(invoices)
        else:    
            json_file = JsonFile(path+'/archivos/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")
            
            suma = reduce(lambda total, invoice: round(total+ invoice["total"],2), 
            invoices,0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ",total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x=input("presione una tecla para continuar...")    

#Menu Proceso Principal
opc=''
while opc !='4':  
    borrarPantalla()      
    menu_main = Menu(blue_color+"Menu Facturacion",[green_color+"1) Clientes","2) Productos","3) Ventas","4) Salir"],20,10)
    opc = menu_main.menu()
    if opc == "1":
        opc1 = ''
        while opc1 !='5':
            borrarPantalla()    
            menu_clients = Menu(blue_color+"Menu Cientes",[green_color+"1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc1 = menu_clients.menu()
            if opc1 == "1":
                crud_clients = CrudClients()
                crud_clients.create()
            elif opc1 == "2":
                crud_clients = CrudClients()
                crud_clients.update()
            elif opc1 == "3":
                crud_clients = CrudClients()
                crud_clients.delete()
            elif opc1 == "4":
                crud_clients = CrudClients()
                crud_clients.consult()
            print("Regresando al menu Clientes...")
            # time.sleep(2)            
    elif opc == "2":
        opc2 = ''
        while opc2 !='5':
            borrarPantalla()    
            menu_products = Menu(blue_color+"Menu Productos",[green_color+"1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],20,10)
            opc2 = menu_products.menu()
            if opc2 == "1":
                crudProducts = CrudProducts()
                crudProducts.create()
            elif opc2 == "2":
                crudProducts = CrudProducts()
                crudProducts.update()
            elif opc2 == "3":
                crudProducts = CrudProducts()
                crudProducts.delete()
            elif opc2 == "4":
                crudProducts = CrudProducts()
                crudProducts.consult()
    elif opc == "3":
        opc3 =''
        while opc3 !='5':
            borrarPantalla()
            sales = CrudSales()
            menu_sales = Menu(blue_color+"Menu Ventas",[green_color+"1) Registro Venta","2) Consultar","3) Modificar","4) Eliminar","5) Salir"],20,10)
            opc3 = menu_sales.menu()
            if opc3 == "1":
                sales.create()   
            elif opc3 == "2":
                sales.consult()
            elif opc3 == "3":
                sales.update()
            elif opc3 == "4":
                sales.delete()
                time.sleep(2)
     
    print("Regresando al menu Principal...")
    # time.sleep(2)            

borrarPantalla()
input("Presione una tecla para salir...")
borrarPantalla()

