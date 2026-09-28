import random
from data.storage import guardar_todos

DERECHOS = {
    "Colectivos": 452800,
    "Sin protocolo": 679100,
    "Privados": 997000,
}

def generar_codigo_solicitud(requests):
    requests_ident = str(random.randint(1000, 9999))
    while requests_ident in requests:
        requests_ident = str(random.randint(1000, 9999))
    return requests_ident

def evaluar_requisitos(request, students, paz_salvo):
    student_code = request["codigo_estudiante"]
    if student_code not in paz_salvo or not paz_salvo[student_code]:
        request["cumple_requisitos"] = False
        request["estado_solicitud"] = "Rechazada"
        return ["No tiene el paz y salvo diligenciado."]
    requierements = paz_salvo[student_code]
    positivos = [
        "trabajo_grado_aprobado", "extension_academica_paz", "ingles_aprobado",
        "paz_salvo_financiero", "paz_salvo_cartera", "fecha_terminacion_ok",
        "saber_pro_presentado",
    ]
    missing = [r for r in positivos if not requierements.get(r, False)]
    if requierements.get("multas_biblioteca", True):
        missing.append("multas_biblioteca")
    cumple = len(missing) == 0
    request["cumple_requisitos"] = cumple
    request["estado_solicitud"] = "Aprobada" if cumple else "Rechazada"
    return missing

def registrar_solicitud(requests, students, paz_salvo, billing):
    text = "SOLICITUD DE GRADOS"
    while True:
        try:
            print(text.center(40, "="))
            codigo_estudiante = input("Digite el codigo del estudiante (o 'salir'): ").strip()
            if codigo_estudiante.lower() == 'salir':
                print("Volviendo al modulo principal...")
                break
            if codigo_estudiante not in students:
                print("No se ha encontrado ningun estudiante registrado con ese codigo.")
                continue
            if students[codigo_estudiante]["status"] != "Egresado No Graduado":
                print("Lo siento este estudiante no cumple con el requisito para el")
                continue
            ya_tiene_solicitud = any(
                sol["codigo_estudiante"] == codigo_estudiante for sol in requests.values()
            )
            if ya_tiene_solicitud:
                print("Este estudiante ya tiene una solicitud de grado registrada.")
                continue
            print("Tipos de derecho de grado disponibles:")
            for tipo, valor in DERECHOS.items():
                print(f" {tipo}: ${valor}")
            tipo_derecho_grado = input("Digite el tipo de derecho de grado: ").strip()
            if tipo_derecho_grado not in DERECHOS:
                print("Tipo de derecho no valido.")
                continue
            valor_pagado = DERECHOS[tipo_derecho_grado]
            codigo_solicitud = generar_codigo_solicitud(requests)
            requests[codigo_solicitud] = {
                "codigo_estudiante": codigo_estudiante,
                "tipo_derecho_grado": tipo_derecho_grado,
                "valor_pagado": valor_pagado,
                "cumple_requisitos": False,
                "estado_solicitud": "Pendiente",
            }
            print(f"\nSOLICITUD REGISTRADA CON EXITO!\nCODIGO: {codigo_solicitud}")
            guardar_todos({}, {}, {}, requests, {}, {}, {})
            break
        except ValueError:
            print("El valor pagado debe ser un numero valido.")
            continue
        except Exception as e:
            print(f"Se ha producido un error inesperado en el programa porfavor vuelva a intentarlo {e}")
            continue

def consultar_solicitudes(requests, students, student_code=None):
    text = "SOLICITUDES DE GRADO"
    print(text.center(40, "="))
    if not requests:
        print("No hay ninguna solicitud de grado por el momento...")
        return
    for ident, data in requests.items():
        if student_code and data["codigo_estudiante"] != student_code:
            continue
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

def validar_requisitos(requests, students, paz_salvo, billing):
    while True:
        try:
            print("1. Validar una solicitud")
            print("2. Validar todas las Pendientes")
            print("3. Salir")
            opcion = input("Seleccione una opcion: ").strip()
            if opcion == "3":
                break
            if opcion == "2":
                for code, req in requests.items():
                    if req["estado_solicitud"] == "Pendiente":
                        missing = evaluar_requisitos(req, students, paz_salvo)
                        if req["estado_solicitud"] == "Aprobada":
                            student_code = req["codigo_estudiante"]
                            if student_code in students:
                                stu = students[student_code]
                                fac = stu["faculty"]
                                prog = stu["program"]
                                billing[fac] = billing.get(fac, 0) + req["valor_pagado"]
                                billing[prog] = billing.get(prog, 0) + req["valor_pagado"]
                        print(f"Solicitud {code}: {req['estado_solicitud']}")
                guardar_todos({}, {}, {}, requests, {}, {}, billing)
                break
            if opcion == "1":
                ident_request = input("Diligencie el codigo de la solicitud que desea buscar ejm(2123): ").strip()
                if len(ident_request) == 4 and ident_request.isdigit():
                    if ident_request in requests:
                        request = requests[ident_request]
                        if request["estado_solicitud"] != "Pendiente":
                            print("Esta solicitud no esta en estado Pendiente.")
                            continue
                        missing = evaluar_requisitos(request, students, paz_salvo)
                        print(f"\nRESULTADO: {request['estado_solicitud']}")
                        if not request["cumple_requisitos"]:
                            print(f"Requisitos faltantes: {', '.join(missing)}")
                        if request["estado_solicitud"] == "Aprobada":
                            student_code = request["codigo_estudiante"]
                            if student_code in students:
                                stu = students[student_code]
                                fac = stu["faculty"]
                                prog = stu["program"]
                                billing[fac] = billing.get(fac, 0) + request["valor_pagado"]
                                billing[prog] = billing.get(prog, 0) + request["valor_pagado"]
                            guardar_todos({}, {}, {}, requests, {}, {}, billing)
                    else:
                        print("No se ha encontrado ninguna solicitud asociada a este codigo porfavor revise bien los datos y vuelva a intentarlo nuevamente!")
                else:
                    print("El formato diligenciado no es valido porfavor intente de nuevo..")
            else:
                break
        except ValueError:
            print("Valor invalido.")
            continue
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue

def revalidar_solicitud(requests, students, paz_salvo, billing):
    while True:
        try:
            ident_request = input("Diligencie el codigo de la solicitud que desea buscar ejm(2123): ").strip()
            if len(ident_request) == 4 and ident_request.isdigit():
                if ident_request in requests:
                    request = requests[ident_request]
                    if request["estado_solicitud"] != "Rechazada":
                        print(f"Esta solicitud esta en estado '{request['estado_solicitud']}', solo se pueden revalidar las Rechazadas.")
                        break
                    missing = evaluar_requisitos(request, students, paz_salvo)
                    print(f"\nRESULTADO: {request['estado_solicitud']}")
                    if not request["cumple_requisitos"]:
                        print(f"Requisitos pendientes: {', '.join(missing)}")
                    if request["estado_solicitud"] == "Aprobada":
                        student_code = request["codigo_estudiante"]
                        if student_code in students:
                            stu = students[student_code]
                            fac = stu["faculty"]
                            prog = stu["program"]
                            billing[fac] = billing.get(fac, 0) + request["valor_pagado"]
                            billing[prog] = billing.get(prog, 0) + request["valor_pagado"]
                        guardar_todos({}, {}, {}, requests, {}, {}, billing)
                    break
                else:
                    print("No se ha encontrado ninguna solicitud asociada a este codigo porfavor revise bien los datos y vuelva a intentarlo nuevamente!")
            else:
                print("El formato diligenciado no es valido porfavor intente de nuevo..")
        except Exception as e:
            print(f"Ha ocurrido un error inesperado intentelo de nuevo! {e}")
            continue