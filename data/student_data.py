students = {};

def registrar_estudiantes(students):
    text = "REGISTRO DE ESTUDIANTES"
    while(True):
        try:
            print(text.center(40,"="));
            student_ident = input("Digite el Codigo de identificacion de el estudiante ejm (1034861231): ").strip();
            if len(student_ident) == 10 and student_ident.isdigit():
                print("Codigo del estudiante guardado correctamente!")
            else:
                print("El codigo de identficiacion del estudiante debe tener 10 caracteres");
                continue;

            if student_ident in students:
                print(f"El {student_ident} del estudiante ya se encuentra en el sistema!\n Corrija la informacion o Intente de nuevo!!")
                continue;
            
            student_name = input("Digite el nombre del estudiante (ejm: Juan Pedrito): ");
            student_lastName = input("Digite el apellido del estudiante (ejm: Cabrera Perez): ")
            students[student_ident] = {
                "name" : student_name,
                "last_name" : student_lastName
            }
            print(f"¡Estudiante {student_name} registrado con éxito!\n")
            break 
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")

def editar_estudiantes(students):
    while(True):
        try: 
            text = "EDITAR ESTUDIANTE"
            print(text.center(40, "="))

            edit_student = input("Digite el codigo del estudiante que desea editar ejm(104286921): ").strip();
            if edit_student.lower() == 'salir':
                break

            if edit_student in students:
                data = students[edit_student]
                print(f"Los datos actuales del estudiante son --> Nombre: {data['name']} | Apellido: {data['last_name']}")
                print("(Presione ENTER sin escribir nada si no desea cambiar el campo)\n")

                new_name = input("Digite el nombre del estudiante ejm: ( Juan Pedrito): ");
                new_lastName = input("Digite el apellido del estudiante ejm: (Cabrera Perez): ")

                if new_name:
                    students[edit_student]["name"] = new_name;
                if new_lastName :
                    students[edit_student]["last_name"] = new_lastName;
                print("¡Información actualizada correctamente!\n")
                break
            else:
                print(f"El codigo: {edit_student} del estudiante que escribiste es incorrecto valide los datos e intente de nuevo...")
                continue;
        except Exception as e:
                    print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")

def eliminar_estudiante(students):
    text = "ELIMINAR DATOS DE ESTUDIANTE"
    while(True):
        try:
            print(text.center(40, "="))
            identification = input("Digite el codigo del estudiante que desea editar ejm(104286921): ").strip();
            if identification.lower() == 'salir':
                break
            
            if identification in students:
                deleted_student = students.pop(identification);
                print(f"El estudiante con Codigo: {identification} ha sido eliminado correctamente!")
                print(f"Nombre: {deleted_student['name']} {deleted_student['last_name']}")
                break
            else:
                print(f"No se ha podido encontrar ningun estudiante con el codigo: {identification}")
                continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")

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
""");