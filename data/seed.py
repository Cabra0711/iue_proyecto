from data.storage import guardar_csv, CSV_DIR
import os

FACULTADES = {
    "001": {"name": "Ciencias Políticas y Jurídicas"},
    "002": {"name": "Ciencias Empresariales"},
    "003": {"name": "Ciencias Humanas y Educación"},
    "004": {"name": "Ingenierías"},
}

PROGRAMAS = {
    "020": {"name": "Derecho", "faculty": "001", "formation_level": "PREGRADO"},
    "023": {"name": "Seguridad y Salud en el Trabajo", "faculty": "001", "formation_level": "PREGRADO"},
    "025": {"name": "Técnico Profesional en Tránsito Transporte y Seguridad Vial", "faculty": "001", "formation_level": "PREGRADO"},
    "026": {"name": "Tecnología en Gestión de Proyectos Sociales y Comunitarios", "faculty": "001", "formation_level": "PREGRADO"},
    "200": {"name": "Esp. Derecho Administrativo Laboral", "faculty": "001", "formation_level": "POSGRADO"},
    "201": {"name": "Esp. Responsabilidad Estatal", "faculty": "001", "formation_level": "POSGRADO"},
    "202": {"name": "Esp. Contratación Estatal", "faculty": "001", "formation_level": "POSGRADO"},
    "203": {"name": "Esp. Derecho Disciplinario", "faculty": "001", "formation_level": "POSGRADO"},
    "204": {"name": "Esp. Derecho Administrativo", "faculty": "001", "formation_level": "POSGRADO"},
    "205": {"name": "Esp. Derecho Laboral y de la Seguridad Social", "faculty": "001", "formation_level": "POSGRADO"},
    "031": {"name": "Contaduría Pública", "faculty": "002", "formation_level": "PREGRADO"},
    "032": {"name": "Administración y Mercados Internacionales", "faculty": "002", "formation_level": "PREGRADO"},
    "033": {"name": "Administración de Negocios Internacionales", "faculty": "002", "formation_level": "PREGRADO"},
    "034": {"name": "Administración Financiera", "faculty": "002", "formation_level": "PREGRADO"},
    "035": {"name": "Tecnología en Control de Gestión en Sistemas de Información Contable", "faculty": "002", "formation_level": "PREGRADO"},
    "036": {"name": "Mercadeo", "faculty": "002", "formation_level": "PREGRADO"},
    "300": {"name": "Esp. Finanzas y Proyectos", "faculty": "002", "formation_level": "POSGRADO"},
    "301": {"name": "Esp. Logística", "faculty": "002", "formation_level": "POSGRADO"},
    "302": {"name": "Esp. Gerencia", "faculty": "002", "formation_level": "POSGRADO"},
    "041": {"name": "Psicología", "faculty": "003", "formation_level": "PREGRADO"},
    "042": {"name": "Trabajo Social", "faculty": "003", "formation_level": "PREGRADO"},
    "400": {"name": "Esp. Psicología de la Actividad Física y del Deporte", "faculty": "003", "formation_level": "POSGRADO"},
    "401": {"name": "Esp. Psicogerontología", "faculty": "003", "formation_level": "POSGRADO"},
    "440": {"name": "Maestría en Ciencias Sociales", "faculty": "003", "formation_level": "POSGRADO"},
    "010": {"name": "Ingeniería de Sistemas", "faculty": "004", "formation_level": "PREGRADO"},
    "011": {"name": "Ingeniería Electrónica", "faculty": "004", "formation_level": "PREGRADO"},
    "012": {"name": "Ingeniería Industrial", "faculty": "004", "formation_level": "PREGRADO"},
    "013": {"name": "Ingeniería Informática", "faculty": "004", "formation_level": "PREGRADO"},
    "014": {"name": "Tecnología en Desarrollo de Sistemas de Información", "faculty": "004", "formation_level": "PREGRADO"},
    "100": {"name": "Esp. Gestión de TIC Empresarial", "faculty": "004", "formation_level": "POSGRADO"},
    "101": {"name": "Esp. Seguridad de la Información de las Organizaciones", "faculty": "004", "formation_level": "POSGRADO"},
    "102": {"name": "Esp. Prospectiva Tecnológica", "faculty": "004", "formation_level": "POSGRADO"},
    "103": {"name": "Esp. Gestión Estratégica de la Innovación", "faculty": "004", "formation_level": "POSGRADO"},
}

DERECHOS = {
    "Colectivos": 452800,
    "Sin protocolo": 679100,
    "Privados": 997000,
}

ESTUDIANTES_EJEMPLO = {
    "1034861231": {"name": "Carlos Andrés", "last_name": "Martínez Rojas", "document_type": "CC", "document_number": "1034861231", "phone": "3123456789", "faculty": "001", "program": "020", "status": "Egresado No Graduado", "average": 3.5},
    "2045678901": {"name": "María Fernanda", "last_name": "García López", "document_type": "CC", "document_number": "2045678901", "phone": "3134567890", "faculty": "002", "program": "031", "status": "Egresado No Graduado", "average": 4.2},
    "3056789012": {"name": "Juan Pablo", "last_name": "Ramírez Sánchez", "document_type": "TI", "document_number": "3056789012", "phone": "3145678901", "faculty": "003", "program": "041", "status": "Egresado No Graduado", "average": 3.8},
    "4067890123": {"name": "Ana Lucía", "last_name": "Pérez Torres", "document_type": "CC", "document_number": "4067890123", "phone": "3156789012", "faculty": "004", "program": "010", "status": "Graduado", "average": 4.5},
    "5078901234": {"name": "Luis Eduardo", "last_name": "Hernández Vargas", "document_type": "CC", "document_number": "5078901234", "phone": "3167890123", "faculty": "001", "program": "200", "status": "Egresado No Graduado", "average": 3.2},
    "6089012345": {"name": "Sofía Camila", "last_name": "Restrepo Muñoz", "document_type": "CE", "document_number": "6089012345", "phone": "3178901234", "faculty": "002", "program": "034", "status": "Activo", "average": 4.7},
}

def sembrar_datos(students, faculties, programs, requests, paz_salvo, credentials, billing):
    for cod, info in FACULTADES.items():
        if cod not in faculties:
            faculties[cod] = dict(info)
    for cod, info in PROGRAMAS.items():
        if cod not in programs:
            programs[cod] = dict(info)
    for cod, info in ESTUDIANTES_EJEMPLO.items():
        if cod not in students:
            students[cod] = dict(info)
            import hashlib
            cred = hashlib.sha256(info["document_number"].encode()).hexdigest()
            credentials[cod] = {"password_hash": cred}

def inicializar_si_es_necesario(students, faculties, programs, requests, paz_salvo, credentials, billing):
    if not faculties:
        sembrar_datos(students, faculties, programs, requests, paz_salvo, credentials, billing)
        return True
    return False