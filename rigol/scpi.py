class SCPIInstrument:

    def __init__(self, transport):
        self.transport = transport

    def write(self, cmd: str):
        self.transport.write(cmd)

    def query(self, cmd: str) -> str:
        return self.transport.query(cmd)

    def query_block(self, cmd: str) -> bytes:
        return self.transport.query_block(cmd)

    def idn(self):
        return self.query("*IDN?")

    def reset(self):
        self.write("*RST")

    def clear(self):
        self.write("*CLS")

    def wait(self):
        self.write("*WAI")

    def opc(self):
        return self.query("*OPC?")

    def close(self):
        self.transport.close()
        