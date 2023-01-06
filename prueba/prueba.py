import pandas as pd
from rut_chile import rut_chile

datos = pd.read_excel('Registro_Inicial.xlsx')
datos['RUT'] = datos['RUT'].apply(lambda name: str(name).replace(' ', ''))

def extraerRutInvalido(ruts):
    rutIncorrectos= []
    for rut in ruts:
        try:
            if rut_chile.is_valid_rut(rut) == False:
                rutIncorrectos.append(rut)
            
        except ValueError:
            rutIncorrectos.append(rut)
    return rutIncorrectos

rutInvalidos = extraerRutInvalido(datos['RUT'])
mask = datos['RUT'].isin(rutInvalidos)

datosTxt = datos[mask]
datos = datos[-mask]

datosTxt.to_csv('rutsInvalidos.txt', sep = '|', index= False)

def formatoTexto(text: str) -> str:
    return text.title().strip()

def formatoTelefono(telefono: str) -> str:
    telefonoModificado = str(telefono).replace(' ', '').replace('+56', '')
    numero = ''
    for fonoCaracter in telefonoModificado:
        if fonoCaracter.isnumeric():
            numero = numero + fonoCaracter
    return numero

def formatoRut(rut: str) -> str:
      return rut_chile.format_capitalized_rut_with_dots(rut)


def generarUsername(rut: str):
    rutModuficado = rut.replace('.','').replace('k', '0').replace('K', '0').replace('-', '')
    return rutModuficado

def generarPassword(rut: str):
    rutModificado = rut.replace('.','')[0:4]
    return rutModificado

def formatoCursos(curso: str):
    cursosList = curso.split(',')

    cursoFormateado = []
    for c in cursosList:
        cursoFormateado.append(c.strip().title())
    
    return cursoFormateado


#formato telefono
datos['Teléfono'] = datos['Teléfono'].map(lambda name: formatoTelefono(name))

datosTerminados = pd.DataFrame()

datosTerminados['username'] = datos['RUT'].map(lambda name: generarUsername(name))
datosTerminados['password'] = datos['RUT'].map(lambda name: generarPassword(name))
datosTerminados['firstname'] = datos['Nombres'].map(lambda name: formatoTexto(name))
datosTerminados['lastname'] = datos['Apellidos'].map(lambda name: formatoTexto(name))
datosTerminados['email'] = datos['Dirección de correo electrónico'].map(lambda email: email.strip())
datosTerminados['institución'] = datos['Establecimiento'].map(lambda name: formatoTexto(name))
datosTerminados['course1'] = datos['¿Cuál o cuáles cursos le interesan?'].map(lambda name: formatoCursos(name))
datosTerminados['role1'] = '5'
datosTerminados['profile_field_RUT'] = datos['RUT'].map(lambda name: formatoRut(name))



# cursos = datosTerminados['course1']

# cursosNoRepetidos=[]
# #determinar cursos no repetidos.
# for curso in cursos:
#     for nombreCursos in curso.split(','):
#         if nombreCursos.strip() not in cursosNoRepetidos:
#             cursosNoRepetidos.append(nombreCursos.strip())

registroAgrupado = {}

for registro in datosTerminados.itertuples():
    for curso in registro.course1:
        print(pd.Series(registro))
        if curso not in registroAgrupado:
            registroAgrupado[curso] = [registro]
        else:
            registroAgrupado[curso].append(registro)


for key, value in registroAgrupado.items():
    datosIngresados = pd.DataFrame(value)

    datosIngresados.to_csv(f'{key}.csv', index= False)

datosTerminados.to_csv('datosTerminados.csv', index= False)


# username: Rut sin puntos ni guion, reemplazando letra K con un cero
# password: Primeros 4 dígitos del rut
# firstname: Primer nombre
# lastname: Apellidos
# email: Correo email
# course1: Nombre del Curso
# role1: número 5
# institución: Establecimiento
# profile_field_RUT: Rut con puntos, guion y letra
