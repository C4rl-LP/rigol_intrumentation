# Controle de Osciloscópios Rigol

Este repositório contém uma biblioteca em Python para controle e comunicação com osciloscópios da Rigol utilizando comandos SCPI. Por hora o projeto funciona apenas para linux. 

## Estrutura do Projeto

O projeto é dividido nos seguintes módulos e arquivos principais:

### 1. Pacote `rigol/`
Este é o pacote principal da biblioteca, contendo a lógica de comunicação e comandos específicos:

* **[rigol/transporte.py](file:///home/carlos/códigos/rigol_control/rigol/transporte.py)**:
  Contém a classe `USBTMCtransporte`, responsável por abrir a conexão com o dispositivo físico (como `/dev/usbtmc0`), ler/gravar dados puros e processar blocos binários de dados (padrão IEEE 488.2).
  
* **[rigol/scpi.py](file:///home/carlos/códigos/rigol_control/rigol/scpi.py)**:
  Contém a classe base `SCPIInstrument`, que define as operações genéricas de instrumentos SCPI, como gravação de comandos (`write`), consultas (`query`), identificação (`idn`), reinicialização (`reset`) e tratamento básico de erros.

* **[rigol/rigol.py](file:///home/carlos/códigos/rigol_control/rigol/rigol.py)**:
  Herda de `SCPIInstrument` e implementa a classe `RigolScope`. Esta classe traduz as ações do usuário em comandos SCPI específicos para osciloscópios Rigol (como controle de escala vertical/horizontal, trigger, medição de frequência/tensão e captura de formas de onda em formato bruto/binário).

* **[rigol/__init__.py](file:///home/carlos/códigos/rigol_control/rigol/__init__.py)**:
  Arquivo de inicialização que torna a pasta `rigol/` um pacote importável em Python.

### 2. Scripts de Teste e Legado
* **[teste/teste.py](file:///home/carlos/códigos/rigol_control/teste/teste.py)**:
  Script de demonstração e teste. Ele adiciona o diretório raiz do projeto ao caminho de busca do Python (`sys.path`), conecta-se ao osciloscópio em `/dev/usbtmc0`, lê suas configurações (escala horizontal, escala vertical do canal 1, offset, frequência e Vpp) e exibe os resultados no terminal.
  
* **[sl.py](file:///home/carlos/códigos/rigol_control/sl.py)**:
  Módulo legado com a classe `transporte`, contendo métodos de escrita e leitura de n bits/bytes e blocos binários.

## Pré-requisitos e Instalação

### Permissões de USBTMC
Para se comunicar com o osciloscópio no Linux via USBTMC (ex: `/dev/usbtmc0`), o usuário atual precisa ter permissões de escrita e leitura no dispositivo correspondente. Isso geralmente é resolvido adicionando o usuário ao grupo `dialout` ou criando uma regra `udev`.

### Como Executar os Testes
Para rodar o teste principal, execute o seguinte comando a partir da raiz do projeto:

```bash
python3 teste/teste.py
```
