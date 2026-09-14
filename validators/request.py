import random

def generar_codigo_solicitud(requests):
    requests_ident = str(random.randint(1000,9999));
    while requests_ident in requests:
        requests_ident = str(random.randint(1000,9999));
    return requests_ident

def registrar_solicitud(requests, student, paz_salvo):
    text = "SOLICITUD DE GRADOS";
    while(True):
        try:
            print(text.center(40,"="));
            codigo_estudiante = input("Digite el codigo del estudiante para consultar informacion ejm(1038862427): ").strip()
            if not codigo_estudiante in student:
                print("No se ha encontrado ningun estudiante registrado con ese codigo intente de nuevo. Revisa los campos bien nuevamente!")
                continue;
            elif len(codigo_estudiante) < 10 and codigo_estudiante.isdigit():
                print("Digite un formato de codigo valido porfavor!!")
                continue
            elif codigo_estudiante.lower() == 'salir':
                print("Volviendo al modulo principal...")
                break;
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
        except Exception as e:
            print(f"Se ha producido un error inesperado en el programa porfavor vuelva a intentarlo {e}")
            continue