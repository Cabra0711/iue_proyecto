import random

def generar_codigo_programa(programs):
    program_ident = str(random.randint(1000, 9999))
    while program_ident in programs:
        program_ident = str(random.randint(1000, 9999))
    return program_ident

def registrar_programa(programs, faculties):
    text = "REGISTRO DE PROGRAMAS ACADEMICOS"
    while True:
        try:
            print(text.center(40, "="))
            if not faculties:
                print("No hay facultades registradas porfavor registra una antes de registrar un programa")
                return
            print("FACULTADES DISPONIBLES:")
            for ident, data in faculties.items():
                print(f" {ident} - {data['name']}")
            faculty_ident = input("Digite el codigo de la facultad a la cual pertenece el programa: ").strip()
            if faculty_ident not in faculties:
                print(f"No existe ninguna facultad con el codigo: {faculty_ident}")
                continue
            program_name = input("\nDigite el nombre del programa que desea registrar: ")
            if program_name == "":
                print("Digite el nombre de un programa porfavor evite dejarlo vacio!!")
                continue
            program_level = input("\nDigite el grado de formacion (PREGRADO/POSGRADO): ").strip().upper()
            if program_level not in ["PREGRADO", "POSGRADO"]:
                print("Ingrese un grado de formacion valido (PREGRADO/POSGRADO) porfavor!!")
                continue
            program_ident = generar_codigo_programa(programs)
            programs[program_ident] = {
                "name": program_name,
                "faculty": faculty_ident,
                "formation_level": program_level,
            }
            print(f"\nPROGRAMA REGISTRADO CON EXITO! CODIGO: {program_ident} | NOMBRE: {program_name} | FACULTAD: {faculties[faculty_ident]['name']}")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def listar_programas(programs, faculties):
    text = "LISTAR PROGRAMAS"
    print(text.center(40, "="))
    if not programs:
        print("No hay programas registrados...")
        return
    for ident, data in programs.items():
        level = data['formation_level']
        print(f"""
    ID: {ident}
    FACULTAD ASOCIADA: {data['faculty']}
    {level.center(40, "-")}
    PROGRAMA: {data['name']}
""")

def eliminar_programas(programs, faculties, students):
    text = "ELIMINAR DATOS DE PROGRAMAS"
    while True:
        try:
            print(text.center(40, "="))
            if not programs:
                print("No hay programas registrados...")
                return
            ident = input("Digite el codigo del programa que desea eliminar (o 'salir'): ").strip()
            if ident.lower() == 'salir':
                break
            if ident in programs:
                program_students = [s for s in students.values() if s["program"] == ident]
                if program_students:
                    print("No se puede eliminar un programa que tiene estudiantes registrados.")
                    break
                del programs[ident]
                print(f"\nEl programa {ident} ha sido borrado exitosamente del sistema!")
                print(f"\n NOMBRE: {programs[ident]['name']} ")
                break
            else:
                print(f"No se ha podido encontrar ningun programa con el codigo: {ident}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")

def editar_programa(programs):
    text = "EDITAR DATOS DE PROGRAMAS"
    while True:
        try:
            if not programs:
                print("No hay programas registrados...")
                return
            print(text.center(40, "="))
            ident = input("Digite el codigo del programa que desea editar (o 'salir'): ").strip()
            if ident.lower() == "salir":
                break
            if ident not in programs:
                print(f"No existe ningun programa con el codigo: {ident}")
                continue
            data = programs[ident]
            print(f"Los datos actuales del programa son --> NOMBRE: {data['name']} NIVEL: {data['formation_level']}")
            print("(Presione ENTER sin escribir nada si no desea cambiar el campo)\n")
            new_name = input("Digite el nuevo nombre del programa (ENTER para no cambiar): ").strip()
            new_formationLevel = input("Digite el nuevo nivel de formacion PREGRADO/POSGRADO (ENTER para no cambiar): ").strip().upper()
            if new_name:
                programs[ident]["name"] = new_name
            if new_formationLevel and new_formationLevel in ["PREGRADO", "POSGRADO"]:
                programs[ident]["formation_level"] = new_formationLevel
            elif new_formationLevel and new_formationLevel not in ["PREGRADO", "POSGRADO"]:
                print("Nivel de formacion invalido.")
                continue
            print("Informacion actualizada correctamente!\n")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue