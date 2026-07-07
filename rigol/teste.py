from transporte import USBTMCtransporte
from rigol import RigolScope

transport = USBTMCtransporte("/dev/usbtmc0")
scope = RigolScope(transport)

scope.stop()

scope.set_waveform_source(1)
scope.set_waveform_mode("RAW")
scope.set_waveform_format("BYTE")

print("Preamble:")
print(scope.get_preamble())

dados = scope.get_waveform_raw()

print(f"Número de bytes: {len(dados)}")
print(f"Primeiros 20 bytes: {list(dados[:20])}")

scope.run()
scope.close()