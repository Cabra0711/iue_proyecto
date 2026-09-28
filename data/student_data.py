from data.storage import guardar_todos
from validators.auth import hash_password
import random

def generar_codigo_estudiante():
    while True:
        code = str(random.randint(1000000000, 9999999999))
        yield code

def registrar_estudiantes(students, faculties, programs, credentials, paz_salvo, billing):
    text = "REGISTRO DE ESTUDIANTES"
    gen = generar_codigo_estudiante()
    while True:
        try:
            print(text.center(40, "="))
            student_ident = input("Digite el Codigo de identificacion de el estudiante ejm (1034861231): ").strip()
            if len(student_ident) != 10 or not student_ident.isdigit():
                print("El codigo de identificacion del estudiante debe tener 10 caracteres numericos")
                continue
            if student_ident in students:
                print(f"El {student_ident} del estudiante ya se encuentra en el sistema!\n Corrija la informacion o Intente de nuevo!!")
                continue

            student_name = input("Digite el nombre del estudiante (ejm: Juan Pedrito): ").strip()
            student_lastName = input("Digite el apellido del estudiante (ejm: Cabrera Perez): ").strip()
            document_type = input("Tipo de documento (CC/TI/CE/Pasaporte): ").strip().upper()
            if document_type not in ["CC", "TI", "CE", "PASAPORTE"]:
                print("Tipo de documento invalido.")
                continue
            document_number = input("Numero de documento: ").strip()
            phone = input("Telefono: ").strip()

            print("FACULTADES DISPONIBLES:")
            for ident, data in faculties.items():
                print(f" {ident} - {data['name']}")
            faculty = input("Digite el codigo de la facultad: ").strip()
            if faculty not in faculties:
                print("Facultad no existe.")
                continue

            faculty_programs = [p for p in programs.values() if p["faculty"] == faculty]
            if not faculty_programs:
                print("No hay programas registrados en esta facultad.")
                continue
            print("PROGRAMAS DISPONIBLES:")
            for ident, data in faculty_programs.items():
                print(f" {ident} - {data['name']} ({data['formation_level']})")
            program = input("Digite el codigo del programa: ").strip()
            if program not in programs or programs[program]["faculty"] != faculty:
                print("Programa no valido para esta facultad.")
                continue

            status = input("Estado (Activo/No Activo/Egresado No Graduado/Graduado): ").strip()
            if status not in ["Activo", "No Activo", "Egresado No Graduado", "Graduado"]:
                print("Estado invalido.")
                continue
            average = float(input("Promedio (0.0-5.0): ").strip())
            if average < 0.0 or average > 5.0:
                print("Promedio fuera de rango.")
                continue

            students[student_ident] = {
                "name": student_name,
                "last_name": student_lastName,
                "document_type": document_type,
                "document_number": document_number,
                "phone": phone,
                "faculty": faculty,
                "program": program,
                "status": status,
                "average": average,
            }
            cred_hash = hash_password(document_number)
            credentials[student_ident] = {"password_hash": cred_hash}
            paz_salvo[student_ident] = {}
            print(f"Estudiante {student_name} registrado con exito!\n")
            guardar_todos(students, {}, {}, {}, {}, credentials, {})
            break
        except ValueError:
            print("Valor invalido.")
            continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def buscar_estudiante(students, faculties):
    text = "BUSCAR ESTUDIANTE"
    print(text.center(40, "="))
    code = input("Digite el codigo del estudiante: ").strip()
    if code in students:
        data = students[code]
        fac_name = faculties.get(data['faculty'], {}).get('name', data['faculty'])
        print(f"""
    ID: {code}
    Nombre: {data['name']} {data['last_name']}
    Documento: {data['document_type']} {data['document_number']}
    Telefono: {data['phone']}
    Facultad: {fac_name}
    Programa: {data.get('program', 'N/A')}
    Estado: {data['status']}
    Promedio: {data['average']}
""")
    else:
        print("No se encontro ningun estudiante con ese codigo.")

def editar_estudiantes(students, faculties, programs, credentials, paz_salvo, billing):
    while True:
        try:
            text = "EDITAR ESTUDIANTE"
            print(text.center(40, "="))
            edit_student = input("Digite el codigo del estudiante que desea editar (o 'salir'): ").strip()
            if edit_student.lower() == 'salir':
                break
            if edit_student not in students:
                print(f"El codigo {edit_student} del estudiante que escribiste es incorrecto valide los datos e intente de nuevo...")
                continue
            data = students[edit_student]
            print(f"Los datos actuales del estudiante son --> Nombre: {data['name']} | Apellido: {data['last_name']}")
            print("(Presione ENTER sin escribir nada si no desea cambiar el campo)\n")

            new_name = input("Digite el nombre del estudiante (ENTER para no cambiar): ").strip()
            if new_name:
                data["name"] = new_name
            new_lastName = input("Digite el apellido del estudiante (ENTER para no cambiar): ").strip()
            if new_lastName:
                data["last_name"] = new_lastName
            new_phone = input("Digite el telefono (ENTER para no cambiar): ").strip()
            if new_phone:
                data["phone"] = new_phone
            new_status = input("Digite el estado (ENTER para no cambiar): ").strip()
            if new_status and new_status in ["Activo", "No Activo", "Egresado No Graduado", "Graduado"]:
                data["status"] = new_status
            new_average = input("Digite el promedio (ENTER para no cambiar): ").strip()
            if new_average:
                data["average"] = float(new_average)

            print("Informacion actualizada correctamente!\n")
            guardar_todos(students, {}, {}, {}, {}, credentials, {})
            break
        except ValueError:
            print("Valor invalido.")
            continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def eliminar_estudiante(students, faculties, programs, credentials, paz_salvo, billing, requests):
    text = "ELIMINAR DATOS DE ESTUDIANTE"
    while True:
        try:
            print(text.center(40, "="))
            identification = input("Digite el codigo del estudiante que desea eliminar (o 'salir'): ").strip()
            if identification.lower() == 'salir':
                break
            if identification not in students:
                print(f"No se ha podido encontrar ningun estudiante con el codigo: {identification}")
                continue
            has_request = any(sol["codigo_estudiante"] == identification for sol in requests.values())
            if has_request:
                print("No se puede eliminar un estudiante que tiene una solicitud registrada.")
                break
            del students[identification]
            if identification in credentials:
                del credentials[identification]
            if identification in paz_salvo:
                del paz_salvo[identification]
            print(f"El estudiante con Codigo: {identification} ha sido eliminado correctamente!")
            guardar_todos(students, {}, {}, {}, {}, credentials, billing)
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def listar_estudiantes(students):
    text = "LISTAR DATOS DE ESTUDIANTES"
    print(text.center(40, "="))
    if not students:
        print("No hay estudiantes que mostrar...")
        return
    for ident, data in students.items():
        print(f"""
    ID: {ident}
    Name: {data['name']}
    Last Name: {data['last_name']}
    Estado: {data['status']}
    Promedio: {data['average']}
""")