def mejor_estudiante_promedio(students, requests):
    graduandos = {}
    for code, req in requests.items():
        if req.get("estado_solicitud") == "Aprobada":
            student_code = req["codigo_estudiante"]
            if student_code in students:
                graduandos[student_code] = students[student_code]
    if not graduandos:
        return None, "No hay graduandos registrados."
    mejor = max(graduandos.values(), key=lambda s: s.get("average", 0))
    return mejor, None

def mejor_estudiante_facultad(students, requests, faculties):
    resultados = {}
    for code, req in requests.items():
        if req.get("estado_solicitud") == "Aprobada":
            student_code = req["codigo_estudiante"]
            if student_code in students:
                stu = students[student_code]
                fac = stu.get("faculty", "")
                if fac not in resultados or stu.get("average", 0) > resultados[fac].get("average", 0):
                    resultados[fac] = stu
    if not resultados:
        return None, "No hay graduandos por facultad."
    return resultados, None

def promedio_programas(students, requests, programs):
    resultados = {}
    for code, req in requests.items():
        if req.get("estado_solicitud") == "Aprobada":
            student_code = req["codigo_estudiante"]
            if student_code in students:
                stu = students[student_code]
                prog = stu.get("program", "")
                if prog not in resultados:
                    resultados[prog] = {"suma": 0, "count": 0}
                resultados[prog]["suma"] += stu.get("average", 0)
                resultados[prog]["count"] += 1
    if not resultados:
        return None, "No hay datos para calcular promedios por programa."
    for prog in resultados:
        resultados[prog]["promedio"] = resultados[prog]["suma"] / resultados[prog]["count"]
    mayor = max(resultados.items(), key=lambda x: x[1]["promedio"])
    menor = min(resultados.items(), key=lambda x: x[1]["promedio"])
    return resultados, (mayor, menor)

def total_recaudado(billing):
    if not billing:
        return None, "No hay datos de facturación."
    return billing, None

def listado_solicitudes(requests):
    cumplen = []
    no_cumplen = []
    for code, req in requests.items():
        if req.get("estado_solicitud") == "Aprobada":
            cumplen.append((code, req))
        elif req.get("estado_solicitud") == "Rechazada":
            no_cumplen.append((code, req))
    return cumplen, no_cumplen

def cantidad_graduandos(requests, students, programs):
    por_facultad = {}
    por_nivel = {}
    for code, req in requests.items():
        if req.get("estado_solicitud") == "Aprobada":
            student_code = req["codigo_estudiante"]
            if student_code in students:
                stu = students[student_code]
                fac = stu.get("faculty", "")
                por_facultad[fac] = por_facultad.get(fac, 0) + 1
                prog_code = stu.get("program", "")
                if prog_code in programs:
                    nivel = programs[prog_code].get("formation_level", "UNKNOWN")
                    por_nivel[nivel] = por_nivel.get(nivel, 0) + 1
    return por_facultad, por_nivel

def porcentaje_graduandos(requests, students):
    total_solicitudes = len(requests)
    total_estudiantes = len(students)
    total_graduandos = sum(1 for r in requests.values() if r.get("estado_solicitud") == "Aprobada")
    if total_solicitudes == 0:
        return None, "No hay solicitudes registradas."
    pct_solicitudes = (total_graduandos / total_solicitudes) * 100 if total_solicitudes > 0 else 0
    pct_estudiantes = (total_graduandos / total_estudiantes) * 100 if total_estudiantes > 0 else 0
    return {"sobre_solicitudes": pct_solicitudes, "sobre_estudiantes": pct_estudiantes, "total_graduandos": total_graduandos}, None