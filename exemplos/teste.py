import sys
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path para reconhecer o módulo 'rigol'


from rigol.transporte import USBTMCtransporte
from rigol.rigol import RigolScope

transport = USBTMCtransporte("/dev/usbtmc0")

scope = RigolScope(transport)

print("Instrumento:")
print(scope.idn())

print()

print("Escala horizontal:")
print(scope.get_time_scale(), "s/div")

print()

print("Escala vertical CH1:")
print(scope.get_vertical_scale(1), "V/div")

print()

print("Offset CH1:")
print(scope.get_offset(1), "V")

print()

print("Frequência:")
print(scope.measure_frequency(1), "Hz")

print()

print("Vpp:")
print(scope.measure_vpp(1), "V")

scope.close()