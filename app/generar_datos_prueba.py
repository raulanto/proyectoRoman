import os
import random
import django
from datetime import  timedelta
from django.utils import timezone
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')  # Ajusta 'app.settings' según tu estructura

django.setup()
fake = Faker('es_MX')


from django.contrib.auth.models import User
from registro.models import Pais, Estado, Ciudad, Registro

FISICO=[('vivo', 'Vivo'), ('muerto', 'Muerto')]
SEXO = [
    ('mujer', 'Mujer'),
    ('hombre', 'Hombre')
]

ESTADO_CIVIL = [
    ('soltero', 'Soltero'),
    ('casado', 'Casado'),
    ('divorciado', 'Divorciado'),
    ('viudo', 'Viudo'),
    ('union libre', 'Union Libre')
]

# Crear datos básicos de ubicación si no existen
def crear_ubicaciones():
    # Crear país
    pais, created = Pais.objects.get_or_create(
        nombre="México",
        codigo="MX"
    )

    # Crear estados
    estados_mexico = [
        ("Aguascalientes", "AGS"),
        ("Baja California", "BC"),
        ("Baja California Sur", "BCS"),
        ("Campeche", "CAM"),
        ("Chiapas", "CHIS"),
        ("Chihuahua", "CHIH"),
        ("Ciudad de México", "CDMX"),
        ("Coahuila", "COAH"),
        ("Colima", "COL"),
        ("Durango", "DGO"),
        ("Guanajuato", "GTO"),
        ("Guerrero", "GRO"),
        ("Hidalgo", "HGO"),
        ("Jalisco", "JAL"),
        ("México", "MEX"),
        ("Michoacán", "MICH"),
        ("Morelos", "MOR"),
        ("Nayarit", "NAY"),
        ("Nuevo León", "NL"),
        ("Oaxaca", "OAX"),
        ("Puebla", "PUE"),
        ("Querétaro", "QRO"),
        ("Quintana Roo", "QR"),
        ("San Luis Potosí", "SLP"),
        ("Sinaloa", "SIN"),
        ("Sonora", "SON"),
        ("Tabasco", "TAB"),
        ("Tamaulipas", "TAM"),
        ("Tlaxcala", "TLAX"),
        ("Veracruz", "VER"),
        ("Yucatán", "YUC"),
        ("Zacatecas", "ZAC")
    ]

    estados_objs = []
    for nombre, codigo in estados_mexico:
        estado, created = Estado.objects.get_or_create(
            nombre=nombre,
            codigo=codigo,
            pais=pais
        )
        estados_objs.append(estado)

    # Crear ciudades para cada estado
    ciudades_por_estado = 3
    ciudades_objs = []
    for estado in estados_objs:
        for _ in range(ciudades_por_estado):
            ciudad, created = Ciudad.objects.get_or_create(
                nombre=fake.city(),
                estado=estado
            )
            ciudades_objs.append(ciudad)

    return ciudades_objs


# Función para generar fecha de nacimiento aleatoria
def generar_fecha_nacimiento():
    hoy = timezone.now().date()
    edad = random.randint(18, 80)
    fecha_nacimiento = hoy - timedelta(days=edad * 365 + random.randint(0, 364))
    return fecha_nacimiento


# Función para generar RFC
def generar_rfc(nombre, apellido_paterno, apellido_materno, fecha_nacimiento):
    letra_apellido_paterno = apellido_paterno[:1].upper()
    primera_vocal_interna_apellido = next((c for c in apellido_paterno[1:] if c.lower() in 'aeiou'), 'X').upper()
    letra_apellido_materno = apellido_materno[:1].upper() if apellido_materno else 'X'
    letra_nombre = nombre[:1].upper()

    fecha_str = fecha_nacimiento.strftime("%y%m%d")

    # Homoclave aleatoria (3 dígitos alfanuméricos)
    homoclave = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))

    return f"{letra_apellido_paterno}{primera_vocal_interna_apellido}{letra_apellido_materno}{letra_nombre}{fecha_str}{homoclave}"


# Función para generar CURP
def generar_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, sexo):
    # Primera letra del apellido paterno
    letra_apellido_paterno = apellido_paterno[:1].upper()

    # Primera vocal interna del apellido paterno
    primera_vocal_interna_apellido = next((c for c in apellido_paterno[1:] if c.lower() in 'aeiou'), 'X').upper()

    # Primera letra del apellido materno (o X si no tiene)
    letra_apellido_materno = apellido_materno[:1].upper() if apellido_materno else 'X'

    # Primera letra del nombre
    letra_nombre = nombre[:1].upper()

    # Fecha de nacimiento (año, mes, día)
    fecha_str = fecha_nacimiento.strftime("%y%m%d")

    # Sexo (H para hombre, M para mujer)
    letra_sexo = 'H' if sexo == 'hombre' else 'M'

    # Entidad federativa (2 letras)
    entidad_federativa = random.choice(['AS', 'BC', 'BS', 'CC', 'CS', 'CH', 'CL', 'CM', 'DF', 'DG',
                                        'GT', 'GR', 'HG', 'JC', 'MC', 'MN', 'MS', 'NT', 'NL', 'OC',
                                        'PL', 'QT', 'QR', 'SP', 'SL', 'SR', 'TC', 'TS', 'TL', 'VZ',
                                        'YN', 'ZS', 'NE'])

    # Consonantes internas
    consonantes = [c for c in (apellido_paterno[1:] + apellido_materno[1:] + nombre[1:]) if c.upper() not in 'AEIOU']
    primera_consonante_interna = consonantes[0].upper() if consonantes else 'X'
    segunda_consonante_interna = consonantes[1].upper() if len(consonantes) > 1 else 'X'

    # Dígito verificador (número o letra)
    digito_verificador = random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    return f"{letra_apellido_paterno}{primera_vocal_interna_apellido}{letra_apellido_materno}{letra_nombre}{fecha_str}{letra_sexo}{entidad_federativa}{primera_consonante_interna}{segunda_consonante_interna}{digito_verificador}"


# Función principal para crear registros
def crear_registros(num_registros=500):
    # Obtener ciudades disponibles
    ciudades = Ciudad.objects.all()
    if not ciudades.exists():
        ciudades = crear_ubicaciones()

    # Obtener un usuario para el campo usuario_registro
    usuario = User.objects.first()
    if not usuario:
        usuario = User.objects.create_user('admin', 'admin@example.com', 'password')

    # Regímenes fiscales comunes en México
    regimenes = [
        "Sueldos y Salarios",
        "Honorarios",
        "Arrendamiento",
        "Actividades Empresariales",
        "RIF",
        "Incorporación Fiscal"
    ]

    # Ocupaciones comunes
    ocupaciones = [
        "Ingeniero", "Médico", "Abogado", "Contador", "Arquitecto",
        "Profesor", "Enfermero", "Programador", "Diseñador", "Chef",
        "Electricista", "Plomero", "Carpintero", "Vendedor", "Gerente",
        "Administrador", "Recepcionista", "Secretario", "Chofer", "Agricultor"
    ]

    # Niveles de escolaridad
    escolaridades = [
        "Primaria", "Secundaria", "Preparatoria", "Técnico", "Licenciatura",
        "Maestría", "Doctorado"
    ]

    # Parentescos
    parentescos = [
        "Padre", "Madre", "Hermano", "Hermana", "Esposo", "Esposa",
        "Hijo", "Hija", "Tío", "Tía", "Primo", "Prima", "Abuelo", "Abuela"
    ]

    for _ in range(num_registros):
        # Datos personales básicos
        sexo = random.choice(['hombre', 'mujer'])
        if sexo == 'hombre':
            nombre = fake.first_name_male()
            apellido = fake.last_name()
            apellido_materno = fake.last_name()
        else:
            nombre = fake.first_name_female()
            apellido = fake.last_name()
            apellido_materno = fake.last_name()

        # Generar fecha de nacimiento y edad
        fecha_nacimiento = generar_fecha_nacimiento()
        edad = (timezone.now().date() - fecha_nacimiento).days // 365

        # Generar RFC y CURP
        rfc = generar_rfc(nombre, apellido, apellido_materno, fecha_nacimiento)
        curp = generar_curp(nombre, apellido, apellido_materno, fecha_nacimiento, sexo)

        # Seleccionar ciudad aleatoria
        ciudad = random.choice(ciudades)

        # Crear registro
        registro = Registro(
            # Datos personales
            nombre=nombre,
            apellido=apellido,
            email=fake.email(),
            telefono=fake.phone_number(),
            fecha_nacimiento=fecha_nacimiento,
            edad=edad,
            sexo=sexo,
            estado_fisico=random.choice([x[0] for x in FISICO]),

            # Datos fiscales
            rfc=rfc[:9],  # Asegurarnos que no exceda los 9 caracteres
            curp=curp,
            regimen=random.choice(regimenes),

            # Dirección
            colonia="x",
            calle=fake.street_name(),
            numero=str(random.randint(1, 999)),
            cp=fake.postcode(),
            ciudad=ciudad,

            # Estado civil y ocupación
            estado_civil=random.choice([x[0] for x in ESTADO_CIVIL]),
            ocupacion=random.choice(ocupaciones),
            escolaridad=random.choice(escolaridades),

            # Contacto de emergencia
            telefono_emergencia=fake.phone_number(),
            parentesco=random.choice(parentescos),
            nombre_emergencia=fake.first_name(),
            apellido_emergencia=fake.last_name(),

            # Referencia personal
            nombre_referencia=fake.first_name(),
            apellido_referencia=fake.last_name(),
            telefono_referencia=fake.phone_number(),

            # Datos de la empresa (opcional, no todos tienen)
            nombre_empresa=fake.company() ,
            puesto=random.choice(ocupaciones) ,
            fecha_ingreso=fake.date_between(start_date='-10y', end_date='today') ,
            antiguedad=random.randint(1, 10) ,
            sueldo_empresa=round(random.uniform(5000, 50000), 2) ,
            telefono_empresa=fake.phone_number() ,
            direccion_empresa=fake.address() ,
            cp_empresa=fake.postcode() ,

            # Usuario que registra
            usuario_registro=usuario,
            fecha_registro=fake.date_between(start_date='-10y', end_date='today')
        )

        registro.save()

    print(f"Se han creado {num_registros} registros exitosamente.")


if __name__ == '__main__':
    crear_registros(1500)