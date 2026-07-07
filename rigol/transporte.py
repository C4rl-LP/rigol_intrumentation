import os
from pathlib import Path

try:
    import pyvisa
except ImportError:
    pyvisa = None

try:
    devices = list(Path("/dev").glob("usbtmc*"))
except Exception:
    devices = []

class USBTMCtransporte():
    def __init__(self, device: str):
        self.device = device
        self.f = open(device, "r+b", buffering=0)
    
    def write(self, cmd: str):
        if not cmd.endswith("\n"):
            cmd += "\n"
        self.f.write((cmd + '\n').encode())

    def query(self, cmd: str, n: int = 4096) -> str:
        self.write(cmd)
        return self.f.read(n).decode().strip()
    
    def read_n(self, n: int) -> bytes:
        data = bytearray()
        while len(data) < n:
            chunk = self.f.read(n - len(data))
            if chunk == b"":
                raise RuntimeError("conexão encerrada.")
            data.extend(chunk)
        return bytes(data)

    def read_block(self) -> bytes:
        """
        Lê um bloco binário SCPI.

        Formato:
            #<N><LLLL...><dados>
        onde
            N = número de dígitos do tamanho
            L = tamanho dos dados
        """
        if self.read_n(1) != b"#":
            raise RuntimeError("Resposta SCPI inválida")
        try:
            ndigits = int(self.read_n(1).decode())
        except Exception as e:
            raise TypeError("Tipo errado") from e
        
        tamanho = int(self.read_n(ndigits).decode())
        return self.read_n(tamanho)

    def query_block(self, cmd: str) -> bytes:
        self.write(cmd)
        return self.read_block()
        
    def close(self):
        self.f.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()


class VISATransporte():
    def __init__(self, device: str):
        self.device = device
        if pyvisa is None:
            raise ImportError("O pacote pyvisa não está instalado. Instale-o com 'pip install pyvisa'.")
        self.rm = pyvisa.ResourceManager()
        self.instr = self.rm.open_resource(device)
    
    def write(self, cmd: str):
        if not cmd.endswith("\n"):
            cmd += "\n"
        self.instr.write(cmd)

    def query(self, cmd: str, n: int = 4096) -> str:
        return self.instr.query(cmd).strip()
    
    def read_n(self, n: int) -> bytes:
        try:
            return self.instr.read_bytes(n)
        except Exception as e:
            raise RuntimeError("conexão encerrada ou timeout.") from e

    def read_block(self) -> bytes:
        """
        Lê um bloco binário SCPI.

        Formato:
            #<N><LLLL...><dados>
        onde
            N = número de dígitos do tamanho
            L = tamanho dos dados
        """
        if self.read_n(1) != b"#":
            raise RuntimeError("Resposta SCPI inválida")
        try:
            ndigits = int(self.read_n(1).decode())
        except Exception as e:
            raise TypeError("Tipo errado") from e
        
        tamanho = int(self.read_n(ndigits).decode())
        return self.read_n(tamanho)

    def query_block(self, cmd: str) -> bytes:
        self.write(cmd)
        return self.read_block()
        
    def close(self):
        self.instr.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()



