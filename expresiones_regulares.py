import re

# Ejercicio 1 encontrar el patrón en una cadena

coincidencia = re.search(r'ab*', 'reabsorber')
print (f"coincide:{coincidencia}")

if coincidencia:
    print (f"Grupo: {coincidencia.group()} Start:{coincidencia.start()} End:{coincidencia.end()}")

# Ejercicio 2 busca todos los numeros de un string
regex = '[0-9]+'
coincidencia = re.findall(regex, 'El 10 de Mayo de 2019')
print (f"coinciden: {coincidencia}")

# Ejercicio 3 regex compilado
regex = re.compile('[0-9]+')
print(regex.findall('Me fui de casa a las 20:00 el 10 de Mayo de 2019'))

