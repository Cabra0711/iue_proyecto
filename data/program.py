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

