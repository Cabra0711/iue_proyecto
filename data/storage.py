import os
import importlib
csv = importlib.import_module('csv')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(BASE_DIR, "csv")

CSV_FILES = {
    "students": "students.csv",
    "faculties": "faculties.csv",
    "programs": "programs.csv",
    "requests": "requests.csv",
    "paz_salvo": "paz_salvo.csv",
    "credentials": "credentials.csv",
    "billing": "billing.csv",
}

def asegurar_csv_dir():
    if not os.path.exists(CSV_DIR):
        os.makedirs(CSV_DIR)

def cargar_csv(tabla):
    asegurar_csv_dir()
    nombre_archivo = CSV_FILES.get(tabla)
    if not nombre_archivo:
        return {}
    ruta = os.path.join(CSV_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return {}
    datos = {}
    with open(ruta, encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for fila in reader:
            clave = fila.pop("id", None) or fila.pop("codigo", None)
            if clave is None:
                continue
            for key, val in fila.items():
                if val == "True":
                    fila[key] = True
                elif val == "False":
                    fila[key] = False
                else:
                    try:
                        fila[key] = float(val)
                        if fila[key] == int(fila[key]):
                            fila[key] = str(fila[key])
                    except (ValueError, TypeError):
                        pass
            datos[clave] = fila
    return datos

def guardar_csv(tabla, datos):
    asegurar_csv_dir()
    nombre_archivo = CSV_FILES.get(tabla)
    if not nombre_archivo:
        return
    ruta = os.path.join(CSV_DIR, nombre_archivo)
    if not datos:
        return
    campos = list(datos[next(iter(datos))].keys())
    if "id" not in campos:
        campos.append("id")
    with open(ruta, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for clave, valores in datos.items():
            fila = dict(valores)
            fila["id"] = clave
            for key, val in fila.items():
                if isinstance(val, bool):
                    fila[key] = str(val)
                elif isinstance(val, float):
                    fila[key] = str(val)
            writer.writerow(fila)

def cargar_todos():
    students = cargar_csv("students")
    faculties = cargar_csv("faculties")
    programs = cargar_csv("programs")
    requests = cargar_csv("requests")
    paz_salvo = cargar_csv("paz_salvo")
    credentials = cargar_csv("credentials")
    billing = cargar_csv("billing")
    return students, faculties, programs, requests, paz_salvo, credentials, billing

def guardar_todos(students, faculties, programs, requests, paz_salvo, credentials, billing):
    guardar_csv("students", students)
    guardar_csv("faculties", faculties)
    guardar_csv("programs", programs)
    guardar_csv("requests", requests)
    guardar_csv("paz_salvo", paz_salvo)
    guardar_csv("credentials", credentials)
    guardar_csv("billing", billing)