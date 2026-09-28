import os
import sys
import time
import hashlib
from data.student_data import registrar_estudiantes, editar_estudiantes, eliminar_estudiante, listar_estudiantes, buscar_estudiante
from data.faculty import registrar_facultades, editar_facultades, listar_facultades, eliminar_facultades
from data.program import registrar_programa, listar_programas, eliminar_programas, editar_programa
from validators.request import registrar_solicitud, consultar_solicitudes, diligenciar_paz_salvo, validar_requisitos, revalidar_solicitud
from validators.auth import login_estudiante, login_admin
from data.storage import cargar_todos, guardar_todos
from data.seed import inicializar_si_es_necesario
from reports.reports import mejor_estudiante_promedio, mejor_estudiante_facultad, promedio_programas, total_recaudado, listado_solicitudes, cantidad_graduandos, porcentaje_graduandos

menu_options = ["Ingresar como Estudiante", "Ingresar como Administrador", "Salir"]
text = " IUE STUDENT PROGRAM "
flag = True

def limpiar_consola():
    sys.stdout.flush()
    os.system('cls' if os.name == 'nt' else 'clear')

def menu_estudiante(students, credentials, requests, paz_salvo, billing):
    student_menu = True
    while student_menu:
        try:
            limpiar_consola()
            print(" MODULO ESTUDIANTE ".center(40, "="))
            print("1. Ver mis datos")
            print("2. Registrar mi solicitud de grado")
            print("3. Consultar el estado de mi solicitud")
            print("4. Cerrar sesion")
            option = input("\nDigite una opcion 1/4: ").strip()
            if option == "1":
                code = input("Digite su codigo: ").strip()
                if code in students:
                    data = students[code]
                    print(f"""
                    Nombre: {data['name']} {data['last_name']}
                    Documento: {data['document_type']} {data['document_number']}
                    Facultad: {data['faculty']}
                    Programa: {data['program']}
                    Estado: {data['status']}
                    Promedio: {data['average']}
""")
                    input("Presione ENTER para continuar...")
                else:
                    print("Codigo no encontrado.")
                    time.sleep(1.5)
            elif option == "2":
                registrar_solicitud(requests, students, paz_salvo, billing)
                time.sleep(2)
            elif option == "3":
                code = input("Digite su codigo: ").strip()
                consultar_solicitudes(requests, students, student_code=code)
                input("Presione ENTER para continuar...")
                time.sleep(2)
            elif option == "4":
                print("Cerrando sesion...")
                time.sleep(1.5)
                student_menu = False
            else:
                print("\nOpcion invalida en este modulo.")
                time.sleep(1.5)
        except ValueError:
            print("Digite un valor valido porfavor!")
            time.sleep(2)

def menu_administrador(students, faculties, programs, requests, paz_salvo, credentials, billing):
    admin_menu = True
    while admin_menu:
        try:
            limpiar_consola()
            print(" MODULO ADMINISTRADOR ".center(40, "="))
            print("1. Estudiantes")
            print("2. Facultades")
            print("3. Programas")
            print("4. Paz y Salvo")
            print("5. Solicitudes")
            print("6. Reportes")
            print("7. Cerrar sesion")
            option = input("\nDigite una opcion 1/7: ").strip()
            if option == "1":
                students_sub = True
                while students_sub:
                    limpiar_consola()
                    print(" ESTUDIANTES ".center(40, "="))
                    print("1. Registrar")
                    print("2. Ver")
                    print("3. Buscar")
                    print("4. Editar")
                    print("5. Eliminar")
                    print("6. Atras")
                    sub_option = input("\nSeleccione una opcion 1/6: ").strip()
                    if sub_option == "1":
                        registrar_estudiantes(students, faculties, programs, credentials, paz_salvo, billing)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "2":
                        listar_estudiantes(students)
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "3":
                        buscar_estudiante(students, faculties)
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "4":
                        editar_estudiantes(students, faculties, programs, credentials, paz_salvo, billing)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "5":
                        eliminar_estudiante(students, faculties, programs, credentials, paz_salvo, billing, requests)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "6":
                        students_sub = False
                    else:
                        print("\nOpcion invalida en este modulo.")
                        time.sleep(1.5)
            elif option == "2":
                fac_sub = True
                while fac_sub:
                    limpiar_consola()
                    print(" FACULTADES ".center(40, "="))
                    print("1. Registrar")
                    print("2. Ver")
                    print("3. Buscar")
                    print("4. Editar")
                    print("5. Eliminar")
                    print("6. Atras")
                    sub_option = input("\nSeleccione una opcion 1/6: ").strip()
                    if sub_option == "1":
                        registrar_facultades(faculties)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "2":
                        listar_facultades(faculties)
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "3":
                        code = input("Digite el codigo de la facultad a buscar: ").strip()
                        if code in faculties:
                            print(f"\nID: {code}\nNombre: {faculties[code]['name']}")
                        else:
                            print("Facultad no encontrada.")
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "4":
                        editar_facultades(faculties)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "5":
                        eliminar_facultades(faculties, programs, students, requests)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "6":
                        fac_sub = False
                    else:
                        print("\nOpcion invalida en este modulo.")
                        time.sleep(1.5)
            elif option == "3":
                prog_sub = True
                while prog_sub:
                    limpiar_consola()
                    print(" PROGRAMAS ".center(40, "="))
                    print("1. Registrar")
                    print("2. Ver")
                    print("3. Buscar")
                    print("4. Editar")
                    print("5. Eliminar")
                    print("6. Atras")
                    sub_option = input("\nSeleccione una opcion 1/6: ").strip()
                    if sub_option == "1":
                        registrar_programa(programs, faculties)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "2":
                        listar_programas(programs, faculties)
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "3":
                        code = input("Digite el codigo del programa a buscar: ").strip()
                        if code in programs:
                            p = programs[code]
                            print(f"\nID: {code}\nNombre: {p['name']}\nNivel: {p['formation_level']}\nFacultad: {p['faculty']}")
                        else:
                            print("Programa no encontrado.")
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "4":
                        editar_programa(programs)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "5":
                        eliminar_programas(programs, faculties, students)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "6":
                        prog_sub = False
                    else:
                        print("\nOpcion invalida en este modulo.")
                        time.sleep(1.5)
            elif option == "4":
                diligenciar_paz_salvo(paz_salvo, students)
                guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                time.sleep(2)
            elif option == "5":
                sol_sub = True
                while sol_sub:
                    limpiar_consola()
                    print(" SOLICITUDES ".center(40, "="))
                    print("1. Consultar todas las solicitudes")
                    print("2. Validar una solicitud")
                    print("3. Validar todas las Pendientes")
                    print("4. Revalidar una solicitud")
                    print("5. Atras")
                    sub_option = input("\nSeleccione una opcion 1/5: ").strip()
                    if sub_option == "1":
                        consultar_solicitudes(requests, students)
                        input("Presione ENTER para continuar...")
                        time.sleep(2)
                    elif sub_option == "2":
                        validar_requisitos(requests, students, paz_salvo, billing)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "3":
                        validar_requisitos(requests, students, paz_salvo, billing)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "4":
                        revalidar_solicitud(requests, students, paz_salvo, billing)
                        guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                        time.sleep(2)
                    elif sub_option == "5":
                        sol_sub = False
                    else:
                        print("\nOpcion invalida en este modulo.")
                        time.sleep(1.5)
            elif option == "6":
                limpiar_consola()
                print(" REPORTES ".center(40, "="))
                print("1. Mejor estudiante por promedio (general)")
                print("2. Mejor estudiante por facultad")
                print("3. Promedio de graduandos por programa")
                print("4. Total recaudado por facultad y programa")
                print("5. Listado de solicitudes que cumplen / no cumplen")
                print("6. Cantidad de graduandos por facultad y nivel")
                print("7. Porcentaje de graduandos")
                print("8. Atras")
                sub_option = input("\nSeleccione una opcion 1/8: ").strip()
                if sub_option == "1":
                    mejor, error = mejor_estudiante_promedio(students, requests)
                    if error:
                        print(error)
                    else:
                        print(f"\nMejor estudiante: {mejor['name']} {mejor['last_name']} | Promedio: {mejor['average']}")
                    input("Presione ENTER para continuar...")
                elif sub_option == "2":
                    resultados, error = mejor_estudiante_facultad(students, requests, faculties)
                    if error:
                        print(error)
                    else:
                        for fac, stu in resultados.items():
                            print(f"Facultad {fac}: {stu['name']} {stu['last_name']} | Promedio: {stu['average']}")
                    input("Presione ENTER para continuar...")
                elif sub_option == "3":
                    resultados, extremos = promedio_programas(students, requests, programs)
                    if extremos:
                        mayor, menor = extremos
                        print(f"Programa con mayor promedio: {mayor[1]['name']} ({mayor[1]['promedio']:.2f})")
                        print(f"Programa con menor promedio: {menor[1]['name']} ({menor[1]['promedio']:.2f})")
                    input("Presione ENTER para continuar...")
                elif sub_option == "4":
                    billing_data, error = total_recaudado(billing)
                    if error:
                        print(error)
                    else:
                        for key, val in billing_data.items():
                            print(f"{key}: ${val}")
                    input("Presione ENTER para continuar...")
                elif sub_option == "5":
                    cumplen, no_cumplen = listado_solicitudes(requests)
                    print(f"\nSolicitudes que cumplen ({len(cumplen)}):")
                    for code, req in cumplen:
                        print(f"  {code}: {req['codigo_estudiante']} - {req['estado_solicitud']}")
                    print(f"\nSolicitudes que no cumplen ({len(no_cumplen)}):")
                    for code, req in no_cumplen:
                        print(f"  {code}: {req['codigo_estudiante']} - {req['estado_solicitud']}")
                    input("Presione ENTER para continuar...")
                elif sub_option == "6":
                    por_fac, por_nivel = cantidad_graduandos(requests, students, programs)
                    print("\nGraduandos por facultad:")
                    for fac, count in por_fac.items():
                        print(f"  {fac}: {count}")
                    print("\nGraduandos por nivel:")
                    for nivel, count in por_nivel.items():
                        print(f"  {nivel}: {count}")
                    input("Presione ENTER para continuar...")
                elif sub_option == "7":
                    pct_data, error = porcentaje_graduandos(requests, students)
                    if error:
                        print(error)
                    else:
                        print(f"Total graduandos: {pct_data['total_graduandos']}")
                        print(f"Porcentaje sobre solicitudes: {pct_data['sobre_solicitudes']:.2f}%")
                        print(f"Porcentaje sobre estudiantes: {pct_data['sobre_estudiantes']:.2f}%")
                    input("Presione ENTER para continuar...")
                elif sub_option == "8":
                    pass
                else:
                    print("\nOpcion invalida en este modulo.")
                    time.sleep(1.5)
            elif option == "7":
                print("Cerrando sesion...")
                time.sleep(1.5)
                admin_menu = False
            else:
                print("\nOpcion invalida en este modulo.")
                time.sleep(1.5)
        except ValueError:
            print("Digite un valor valido porfavor!")
            time.sleep(2)

if __name__ == "__main__":
    while flag:
        try:
            limpiar_consola()
            print(text.center(40, "="))
            for i, option in enumerate(menu_options, start=1):
                print(f"{i}. {option}")
            option = input("\nDigite una opcion 1/3: ").strip()

            if option == "1":
                students, faculties, programs, requests, paz_salvo, credentials, billing = cargar_todos()
                inicializar_si_es_necesario(students, faculties, programs, requests, paz_salvo, credentials, billing)
                guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                code = input("Codigo de estudiante: ").strip()
                pwd = input("Contrasena: ").strip()
                stored_hash = login_estudiante(credentials, code)
                if stored_hash and stored_hash == hashlib.sha256(pwd.encode()).hexdigest():
                    menu_estudiante(students, credentials, requests, paz_salvo, billing)
                else:
                    print("Credenciales incorrectas.")
                    time.sleep(2)
            elif option == "2":
                students, faculties, programs, requests, paz_salvo, credentials, billing = cargar_todos()
                inicializar_si_es_necesario(students, faculties, programs, requests, paz_salvo, credentials, billing)
                guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing)
                username = input("Usuario: ").strip()
                password = input("Contrasena: ").strip()
                if login_admin(username, password):
                    menu_administrador(students, faculties, programs, requests, paz_salvo, credentials, billing)
                else:
                    print("Credenciales incorrectas.")
                    time.sleep(2)
            elif option == "3":
                print("Saliendo...")
                time.sleep(1.5)
                flag = False
            else:
                print("Ingrese un valor que este dentro del rango porfavor! 1/3")
                time.sleep(2)
        except ValueError:
            print("Digite un valor valido porfavor!")
            time.sleep(2)

    print("credenciales_demo: admin / admin123")