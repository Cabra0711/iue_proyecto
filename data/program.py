import random;

def generar_codigo_programa(programs):
    program_ident = str(random.randint(1000,9999));
    while program_ident in programs:
        program_ident = str(random.randint(1000,9999));
    return program_ident

def registrar_programa(programs, faculties):
    text = "REGISTRO DE PROGRAMAS ACADEMICOS"
    level = ["PREGRADO", "POSGRADO", "ESPECIALIZACION", "MAESTRIA"]
    while(True):
        try:
            print(text.center(40,"="));
            if not faculties:
                print("No hay facultades registradas porfavor registra una antes de registrar un programa");
                return

            print("FACULTADES DISPONIBLES: ")
            for ident, data in faculties.items():
                print(f" {ident} - {data['name']}")

            faculty_ident = input("Digite el codigo de la facultad a la cual pertenece el programa: ").strip()
            if faculty_ident not in faculties:
                print(f"No existe ninguna facultad con el código: {faculty_ident}")
                continue

            program_name = input("\nDigite el nombre de el programa que desea registrar ejm (DERECHO): ")
            if program_name == "":
                print("Digite el nombre de un programa porfavor evite dejarlo vacio!!")
                continue
            
            program_level = input("\nDigite el grado de formacion de el programa ejm (PREGRADO/POSGRADO/ESPECIALIZACION/MAESTRIA): ").upper()

            if program_level not in level:
                print("Ingrese un grado de formacion valido porfavor!!")
                continue

            program_ident = generar_codigo_programa(programs)
            programs[program_ident] = {
                "name": program_name,
                "faculty": faculty_ident,
                "formation_level": program_level,
            }

            print(f"\nPROGRAMA REGISTRADO CON EXITO!\nCODIGO: {program_ident} | NOMBRE: {program_name} | FACULTAD: {faculties[faculty_ident]['name']}")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def listar_programas(programs, faculties):
    text = "LISTAR PROGRAMAS"
    print(text.center(40, "="));
    if not faculties and not programs:
        print("No hay facultades o un programa registrado porfavor registra una antes para visualizar a donde pertenece");
        return
        
    for ident, data in programs.items():
        level = data['formation_level']
        print(f"""
    ID: {ident}
    FACULTAD ASOCIADA: {data['faculty']}
    {level.center(40, "-")}
    PROGRAMA: {data['name']}
""")

def eliminar_programas(programs, faculties):
    text = "ELIMINAR DATOS DE PROGRAMAS"
    while(True):
        try:
            print(text.center(40, "="));
            if not faculties and not programs:
                print("No hay facultades o un programa registrado porfavor registra una antes para visualizar a donde pertenece");
                return
            ident = input("Digite el numero de identificacion del programa que deseas buscar(ejm: 1298): ").strip()
            if ident.lower() == 'salir':
                break;
            if ident in programs:
                deleted_program = programs.pop(ident);
                print(f"\nEl programa {ident} ha sido borrado exitosamente del sistema!")
                print(f"\n NOMBRE: {deleted_program['name']} ")
                break;
            else:
                print(f"No se ha podido encontrar ningun programa con el codigo: {ident}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")

def editar_programa(programs, faculties):
    text = "EDITAR DATOS DE PROGRAMAS"
    while(True):
        try:
            if not faculties and not programs:
                print("No hay facultades o un programa registrado porfavor registra una antes para visualizar a donde pertenece");
                return
            
            print(text.center(40, "="))
            ident = input("Digite el numero de identificacion del programa que desea editar (o 'salir'): ").strip()
            if ident.lower() == "salir":
                break

            if ident not in programs:
                print(f"No existe ningun programa con el codigo: {ident}")
                continue

            data = programs[ident]
            print(f"Los datos actuales del programa son --> NOMBRE: {data['name']} NIVEL: {data['formation_level']}")
            print("(Presione ENTER sin escribir nada si no desea cambiar el campo)\n")

            new_name = input("Digite el nuevo nombre del programa (ENTER para no cambiar): ").strip()
            new_formationLevel = input("Digite el nuevo nivel de formacion (ENTER para no cambiar): ").strip().upper()

            if new_name:
                programs[ident]["name"] = new_name
            if new_formationLevel:
                programs[ident]["formation_level"] = new_formationLevel

            print("¡Información actualizada correctamente!\n")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
               
                