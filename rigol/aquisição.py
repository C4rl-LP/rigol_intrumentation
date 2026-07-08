class aquisicao:
    def __init__(self, scope):
        self.scope = scope
    def aquisicao_simples(self, channel):
        data = self.scope.read_waveform(channel)
        return data
    def aquisicao_varios_canais(self, canais):
        aquisicao = {}
        for canal in canais:
            aquisicao[canal] = self.aquisicao_simples(canal)
        return aquisicao