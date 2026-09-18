import random

def generar_codigo_facultad(faculties):
    faculty_identifi = str(random.randint(100, 999))
    while faculty_identifi in faculties:
        faculty_identifi = str(random.randint(100, 999))
    return faculty_identifi

def registrar_facultades(faculties):
    text = "REGISTRO DE FACULTADES"
    while True:
        try:
            print(text.center(40, "="))
            faculty_name = input("Digite el nombre de la facultad que deseas registrar ejm(FACULTAD DE INGENIERIA): ").strip()
            if faculty_name == "":
                print("Digite algo porfavor!!!")
                continue

            faculty_identifi = generar_codigo_facultad(faculties)
            faculties[faculty_identifi] = {"name": faculty_name}
            print(f"FACULTAD REGISTRADA CON EXITO!\n CODIGO: {faculty_identifi} | NOMBRE: {faculty_name}")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def editar_facultades(faculties):
    text = "EDITAR DATOS DE FACULTADES"
    while True:
        try:
            print(text.center(40, "="))
            faculty_identifi = input("Digite el codigo de la facultad que deseas editar ejm (324) o 'salir': ").strip()
            if faculty_identifi.lower() == 'salir':
                break

            if faculty_identifi in faculties:
                data = faculties[faculty_identifi]
                print(f"\n Los datos actuales de la facultad son --> NOMBRE: {data['name']}")
                print("(Presione ENTER si no desea hacer ningun cambio.)\n")

                new_name = input("Digite el nuevo nombre que le desea asignar a la facultad ejm (Facultad de Artes): ").strip()
                if new_name:
                    faculties[faculty_identifi]['name'] = new_name
                    print(f"¡Información actualizada correctamente: NOMBRE: {faculties[faculty_identifi]['name']}!\n")
                else:
                    print("No se realizó ningún cambio.\n")
                break
            else:
                print(f"No existe ninguna facultad con el código: {faculty_identifi}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado en el sistema porfavor intente de nuevo {e}")
            continue

def listar_facultades(faculties):
    text = "LISTAR DATOS DE FACULTADES"
    print(text.center(40, "="))
    if not faculties:
        print("No hay facultades que mostrar...")
        return
    for ident, data in faculties.items():
        print(f"""
    ID: {ident}
    Name: {data['name']}
""")

def eliminar_facultades(faculties):
    text = "ELIMINAR DATOS DE FACULTADES"
    while True:
        try:
            print(text.center(40, "="))
            for ident, data in faculties.items():
                print(f"""
                ID: {ident}
                Name: {data['name']}
            """)
            identification = input("Digite el codigo de la facultad que desea eliminar ejm(234) o 'salir': ").strip()

            if identification.lower() == 'salir':
                break

            if identification in faculties:
                deleted_faculty = faculties.pop(identification)
                print(f"La facultad con Codigo: {identification} ha sido eliminada correctamente!")
                print(f"Nombre: {deleted_faculty['name']}")
                break
            else:
                print(f"No se ha podido encontrar ninguna facultad con el codigo: {identification}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")