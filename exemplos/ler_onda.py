#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo de leitura de forma de onda (waveform) de um osciloscópio Rigol.

Este script demonstra como usar o novo módulo aquisição.py para realizar capturas
de canal único ou de múltiplos canais de forma simplificada.
"""

import sys
import csv
from pathlib import Path

# Adiciona o diretório raiz do projeto ao sys.path para reconhecer o módulo 'rigol'
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Tenta importar bibliotecas científicas para plotagem se disponíveis
try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from rigol import RigolScope, aquisicao


def conectar_instrumento(endereco: str):
    """
    Retorna uma instância de RigolScope com o transporte correto baseado no endereço.
    """
    if endereco.startswith("/dev/"):
        from rigol.transporte import USBTMCtransporte
        print(f"Conectando via USBTMC nativo no Linux em: {endereco}")
        transport = USBTMCtransporte(endereco)
    else:
        from rigol.transporte import VISATransporte
        print(f"Conectando via VISA em: {endereco}")
        transport = VISATransporte(endereco)
    
    return RigolScope(transport)


def main():
    # --- CONFIGURAÇÕES ---
    # Altere o endereço conforme necessário (ex: "/dev/usbtmc0" ou recurso VISA)
    # Exemplo VISA: "USB0::0x1AB1::0x044C::DS1ZA123456789::INSTR"
    DEVICE_ADDRESS = "/dev/usbtmc0"
    
    # Canais para fins de demonstração
    CANAL_UNICO = 1
    CANAIS_MULTIPLOS = [1, 2]

    try:
        scope = conectar_instrumento(DEVICE_ADDRESS)
    except Exception as e:
        print(f"\nErro ao conectar ao instrumento: {e}")
        print("Verifique se o osciloscópio está ligado, conectado e se você possui permissões.")
        sys.exit(1)

    try:
        # Exibe a identificação do osciloscópio
        idn = scope.idn()
        print(f"\nInstrumento Identificado: {idn}")

        # Instancia a classe de aquisição passando o escopo
        acq = aquisicao(scope)

        # ----------------------------------------------------
        # Exemplo 1: Aquisição Simples (Canal Único)
        # ----------------------------------------------------
        print(f"\n--- Exemplo 1: Capturando canal {CANAL_UNICO} ---")
        try:
            waveform = acq.aquisicao_simples(channel=CANAL_UNICO)
            print(f"Captura realizada com sucesso!")
            print(f"  Canal: {waveform.canal}")
            print(f"  Modo: {waveform.modo}")
            print(f"  Pontos de dados: {len(waveform.tempo)}")
            print(f"  Timestamp da captura: {waveform.timestamp}")
            
            # Estatísticas rápidas
            v_max = max(waveform.tensao)
            v_min = min(waveform.tensao)
            v_pp = v_max - v_min
            print(f"  Vmin: {v_min:.3f} V | Vmax: {v_max:.3f} V | Vpp (calculado): {v_pp:.3f} V")

            # Salva os dados em arquivo CSV
            csv_file = Path(__file__).resolve().parent / f"captura_simples_ch{CANAL_UNICO}.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Tempo (s)", f"Tensao CH{CANAL_UNICO} (V)"])
                writer.writerows(zip(waveform.tempo, waveform.tensao))
            print(f"  Dados salvos em: {csv_file.name}")

            # Plotagem simples se matplotlib estiver disponível
            if HAS_MATPLOTLIB:
                img_file = Path(__file__).resolve().parent / f"grafico_simples_ch{CANAL_UNICO}.png"
                plt.figure(figsize=(10, 4))
                # Converte tempos para milissegundos para melhor leitura no eixo X
                tempos_ms = [t * 1e3 for t in waveform.tempo]
                plt.plot(tempos_ms, waveform.tensao, label=f"CH{waveform.canal}", color="royalblue")
                plt.title(f"Captura Simples - Canal {waveform.canal}")
                plt.xlabel("Tempo (ms)")
                plt.ylabel("Tensão (V)")
                plt.grid(True, linestyle="--", alpha=0.7)
                plt.legend()
                plt.savefig(img_file, dpi=150)
                plt.close()
                print(f"  Gráfico salvo em: {img_file.name}")

        except Exception as e:
            print(f"Falha na aquisição simples do canal {CANAL_UNICO}: {e}")

        # ----------------------------------------------------
        # Exemplo 2: Aquisição de Múltiplos Canais
        # ----------------------------------------------------
        print(f"\n--- Exemplo 2: Capturando múltiplos canais {CANAIS_MULTIPLOS} ---")
        try:
            # Captura múltiplos canais sequencialmente
            waveforms = acq.aquisicao_varios_canais(CANAIS_MULTIPLOS)
            
            # Prepara o gráfico se matplotlib estiver disponível
            if HAS_MATPLOTLIB:
                plt.figure(figsize=(10, 5))
                cores = {1: "royalblue", 2: "orange", 3: "forestgreen", 4: "purple"}
            
            for ch in CANAIS_MULTIPLOS:
                if ch in waveforms:
                    w = waveforms[ch]
                    v_pp = max(w.tensao) - min(w.tensao)
                    print(f"Canal {ch}: {len(w.tempo)} pontos capturados (Vpp: {v_pp:.3f} V)")
                    
                    # Salva arquivo CSV para cada canal
                    csv_file = Path(__file__).resolve().parent / f"captura_multipla_ch{ch}.csv"
                    with open(csv_file, mode="w", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow(["Tempo (s)", f"Tensao CH{ch} (V)"])
                        writer.writerows(zip(w.tempo, w.tensao))
                    
                    if HAS_MATPLOTLIB:
                        tempos_ms = [t * 1e3 for t in w.tempo]
                        plt.plot(tempos_ms, w.tensao, label=f"CH{ch}", color=cores.get(ch, "black"), alpha=0.8)

            if HAS_MATPLOTLIB:
                img_file = Path(__file__).resolve().parent / "grafico_multiplos_canais.png"
                plt.title("Captura de Múltiplos Canais")
                plt.xlabel("Tempo (ms)")
                plt.ylabel("Tensão (V)")
                plt.grid(True, linestyle="--", alpha=0.7)
                plt.legend()
                plt.savefig(img_file, dpi=150)
                plt.close()
                print(f"  Gráfico comparativo salvo em: {img_file.name}")

        except Exception as e:
            print(f"Falha na aquisição de múltiplos canais: {e}")

    finally:
        # Garante o fechamento da conexão
        scope.close()
        print("\nConexão fechada.")


if __name__ == "__main__":
    main()
