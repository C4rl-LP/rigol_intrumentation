from pathlib import Path

devices = list(Path("/dev").glob("usbtmc*"))

class USBTMCtransporte():
    def __init__(self, device: str):
        self.device = device
        self.f = open(device, "r+b", buffering= 0)
    
    def write(self, cmd):
        if not cmd.endswith("\n"):
            cmd += "\n"
        self.f.write((cmd+ '\n').encode())

    def query(self, cmd, n = 4096):
        self.write(cmd)
        return self.f.read(n).decode().strip()
    
    
    def read_n(self, n:int):
        data = bytearray()
        while len(data)< n:
            chunk = self.f.read(n - len(data))
            
            if chunk ==  b"":
                raise RuntimeError("conexão encerrada.")
            data.extend(chunk)

        return data
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
        except:
            raise TypeError("Tipo errado")
        
        tamanho = int(self.read_n(ndigits).decode())
        return self.read_n(tamanho)
    def query_block(self, cmd):
        self.write(cmd)

        return self.read_block()
    
        
    def close(self):
        self.f.close()
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()



