import random

def generar_codigo_solicitud(requests):
    requests_ident = str(random.randint(1000, 9999))
    while requests_ident in requests:
        requests_ident = str(random.randint(1000, 9999))
    return requests_ident


def registrar_solicitud(requests, students, paz_salvo):
    text = "SOLICITUD DE GRADOS"
    while(True):
        try:
            print(text.center(40, "="))
            codigo_estudiante = input("Digite el codigo del estudiante (o 'salir'): ").strip()

            if codigo_estudiante.lower() == 'salir':
                print("Volviendo al modulo principal...")
                break

            if codigo_estudiante not in students:
                print("No se ha encontrado ningun estudiante registrado con ese codigo.")
                continue

            if students[codigo_estudiante]["estado"] != "Egresado No Graduado":
                print("El estudiante debe estar en estado 'Egresado No Graduado' para solicitar grado.")
                continue

            ya_tiene_solicitud = any(
                sol["codigo_estudiante"] == codigo_estudiante for sol in requests.values()
            )
            if ya_tiene_solicitud:
                print("Este estudiante ya tiene una solicitud de grado registrada.")
                continue

            tipo_derecho_grado = input("Digite el tipo de derecho de grado (Pregrado/Posgrado): ").strip()
            valor_pagado = float(input("Digite el valor pagado: "))

            codigo_solicitud = generar_codigo_solicitud(requests)
            requests[codigo_solicitud] = {
                "codigo_estudiante": codigo_estudiante,
                "tipo_derecho_grado": tipo_derecho_grado,
                "valor_pagado": valor_pagado,
                "cumple_requisitos": False,
                "estado_solicitud": "Pendiente",
            }
            print(f"\nSOLICITUD REGISTRADA CON EXITO!\nCODIGO: {codigo_solicitud}")
            break

        except ValueError:
            print("El valor pagado debe ser un número válido.")
            continue
        except Exception as e:
            print(f"Se ha producido un error inesperado en el programa porfavor vuelva a intentarlo {e}")
            continue

def consultar_solicitudes(requests,students):
    text = "SOLICITUDES DE GRADO";
    print(text.center(40,"="));
    if not requests:
        print("No hay ninguna solicitud de grado por el momento...");
        return
    for ident, data in requests.items():
        codigo_estudiante = data["codigo_estudiante"]
        student = students.get(codigo_estudiante)
        if student:
            nombre_completo = f"{student['name']} {student['last_name']}"
        else:
            nombre_completo = "Estudiante no encontrado"

        cumple_texto = "SI" if data["cumple_requisitos"] else "NO"
        print(f"""
        ID DE LA SOLICITUD: {ident}
        ID DEL ESTUDIANTE: {data["codigo_estudiante"]}
        ESTUDIANTE : {nombre_completo}
        ESTADO SOLICITUD | {data["estado_solicitud"]}
        VALOR PAGADO --> {data["valor_pagado"]}
        CUMPLE REQUISITOS : {cumple_texto}
""")

def diligenciar_paz_salvo(paz_salvo, students):
    text = "DILIGENCIAR PAZ Y SALVO / REQUISITOS DE GRADO"
    while True:
        try:
            print(text.center(40, "="))
            codigo_estudiante = input("Digite el codigo del estudiante (o 'salir'): ").strip()

            if codigo_estudiante.lower() == 'salir':
                break

            if codigo_estudiante not in students:
                print("No existe ningun estudiante con ese codigo.")
                continue

            print(f"\nDiligenciando requisitos para: {students[codigo_estudiante]['name']} {students[codigo_estudiante]['last_name']}\n")

            def pedir_si_no(pregunta):
                respuesta = input(pregunta).strip().lower()
                return respuesta in ["s", "si", "sí"]

            paz_salvo[codigo_estudiante] = {
                "multas_biblioteca": pedir_si_no("¿Tiene multas en biblioteca? (s/n): "),
                "trabajo_grado_aprobado": pedir_si_no("¿Trabajo de grado aprobado? (s/n): "),
                "extension_academica_paz": pedir_si_no("¿Paz y salvo extension academica? (s/n): "),
                "ingles_aprobado": pedir_si_no("¿Ingles aprobado? (s/n): "),
                "paz_salvo_financiero": pedir_si_no("¿Paz y salvo financiero? (s/n): "),
                "paz_salvo_cartera": pedir_si_no("¿Paz y salvo cartera? (s/n): "),
                "fecha_terminacion_ok": pedir_si_no("¿Fecha terminacion dentro del plazo? (s/n): "),
                "saber_pro_presentado": pedir_si_no("¿Presento el examen Saber Pro? (s/n): "),
            }

            print("\n¡Paz y salvo registrado correctamente!\n")
            break
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def validar_requisitos(requests, students, paz_salvo):
    ident_request = input("Diligencie el codigo de la solicitud que desea buscar ejm(2123): ").strip()
    if ident_request.lower() == "salir":
        break;
    if len(ident_request) == 4 and ident_request.isdigit():
        if ident_request in requests:
            request = requests[ident_request]
            student_code = request["codigo_estudiante"]
            if student_code not in paz_salvo:
                print("Este estudiante aún no tiene el paz y salvo diligenciado. No puede cumplir requisitos.")
                request["cumple_requisitos"] = False
                request["estado_solicitud"] = "Rechazada"
                return
        else:
             print("No se ha encontrado ninguna solicitud asociada a este codigo porfavor revise bien los datos y vuelva a intentarlo nuevamente!")


