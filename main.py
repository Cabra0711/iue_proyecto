import os;
import time;
import sys;
from data.student_data import registrar_estudiantes, editar_estudiantes, eliminar_estudiante, listar_estudiantes;

menu_options = ["Registro de estudiantes", "Registro de Facultades", "Registro de Programas", "Solicitudes", "Salir"]
text = " IUE STUDENT PROGRAM "
flag = True
students = {};

def limpiar_consola():
    sys.stdout.flush()
    os.system('cls' if os.name == 'nt' else 'clear')



while flag:
    try:
        limpiar_consola()
        print(text.center(40, "="))
        for i, option in enumerate(menu_options, start=1):
            print(f"{i}. {option}")
        option = int(input("\nDigite una opcion 1/5: "))
        print(option)

        if option <= 0:
            print("El numero que digitaste tiene que ser de un valor mayor a 0!")
            time.sleep(2)
        
        elif option == 5:
            print("Saliendo...")
            time.sleep(1.5)
            flag = False

        elif option > 5:
            print("Ingrese un valor que este dentro del rango porfavor! 1/5")
            time.sleep(2)
        
        elif option == 1:
            students_menu = True
            while students_menu:
                limpiar_consola()  
                text_students = " MODULO REGISTRO DE ESTUDIANTES "
                print(text_students.center(40, "="))  
                print("1. Registrar Estudiante: ")
                print("2. Ver Estudiantes: ")
                print("3. Eliminar Estudiante: ")
                print("4. Editar Estudiante: ")
                print("5. <-- Atras")

                sub_option = int(input("\nSeleccione una opción del módulo 1/5: "))

                if sub_option == 1:
                    registrar_estudiantes(students)
                elif sub_option == 2:
                    listar_estudiantes(students)
                    time.sleep(2)
                elif sub_option == 3:
                    eliminar_estudiante(students)
                elif sub_option == 4:
                    editar_estudiantes(students)
                elif sub_option == 5:
                    students_menu = False
                else:
                    print("\nOpción inválida en este módulo.")
                    time.sleep(1.5)
                    
    except ValueError:
        print("Digite un valor valido porfavor!")
        time.sleep(2)
