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
            faculty_name = input("Digite el nombre de la facultad que deseas registrar: ").strip()
            if faculty_name == "":
                print("Digite algo porfavor!!!")
                continue
            faculty_identifi = generar_codigo_facultad(faculties)
            faculties[faculty_identifi] = {"name": faculty_name}
            print(f"FACULTAD REGISTRADA CON EXITO! CODIGO: {faculty_identifi} | NOMBRE: {faculty_name}")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def editar_facultades(faculties):
    text = "EDITAR DATOS DE FACULTADES"
    while True:
        try:
            print(text.center(40, "="))
            faculty_identifi = input("Digite el codigo de la facultad que deseas editar (o 'salir'): ").strip()
            if faculty_identifi.lower() == 'salir':
                break
            if faculty_identifi in faculties:
                data = faculties[faculty_identifi]
                print(f"\nLos datos actuales de la facultad son --> NOMBRE: {data['name']}")
                print("(Presione ENTER si no desea hacer ningun cambio.)\n")
                new_name = input("Digite el nuevo nombre que le desea asignar a la facultad: ").strip()
                if new_name:
                    faculties[faculty_identifi]['name'] = new_name
                    print(f"Informacion actualizada correctamente: NOMBRE: {faculties[faculty_identifi]['name']}!\n")
                else:
                    print("No se realizo ningun cambio.\n")
                break
            else:
                print(f"No existe ninguna facultad con el codigo: {faculty_identifi}")
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

def eliminar_facultades(faculties, programs, students, requests):
    text = "ELIMINAR DATOS DE FACULTADES"
    while True:
        try:
            print(text.center(40, "="))
            for ident, data in faculties.items():
                print(f"""
                ID: {ident}
                Name: {data['name']}
            """)
            identification = input("Digite el codigo de la facultad que desea eliminar (o 'salir'): ").strip()
            if identification.lower() == 'salir':
                break
            if identification in faculties:
                faculty_programs = [p for p in programs.values() if p["faculty"] == identification]
                if faculty_programs:
                    print("No se puede eliminar una facultad que tiene programas registrados.")
                    continue
                faculty_students = [s for s in students.values() if s["faculty"] == identification]
                if faculty_students:
                    print("No se puede eliminar una facultad que tiene estudiantes registrados.")
                    continue
                del faculties[identification]
                print(f"La facultad con Codigo: {identification} ha sido eliminada correctamente!")
                break
            else:
                print(f"No se ha podido encontrar ninguna facultad con el codigo: {identification}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")