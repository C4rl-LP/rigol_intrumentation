from .scpi import SCPIInstrument
from dataclasses import dataclass
from datetime import datetime
from .data_class import Preamble, Waveform



class RigolScope(SCPIInstrument):

    # -----------------------
    # Aquisição
    # -----------------------

    def run(self):
        self.write(":RUN")

    def stop(self):
        self.write(":STOP")

    def single(self):
        self.write(":SING")

    def autoscale(self):
        self.write(":AUT")

    # -----------------------
    # Escala vertical
    # -----------------------

    def get_vertical_scale(self, channel: int = 1):
        return float(
            self.query(f":CHAN{channel}:SCAL?")
        )

    def set_vertical_scale(self,
                           scale: float,
                           channel: int = 1):

        self.write(
            f":CHAN{channel}:SCAL {scale}"
        )

    # -----------------------
    # Offset
    # -----------------------

    def get_offset(self,
                   channel: int = 1):

        return float(
            self.query(f":CHAN{channel}:OFFS?")
        )

    def set_offset(self,
                   offset: float,
                   channel: int = 1):

        self.write(
            f":CHAN{channel}:OFFS {offset}"
        )

    # -----------------------
    # Canal ligado/desligado
    # -----------------------

    def enable_channel(self,
                       channel: int = 1):

        self.write(
            f":CHAN{channel}:DISP ON"
        )

    def disable_channel(self,
                        channel: int = 1):

        self.write(
            f":CHAN{channel}:DISP OFF"
        )

    # -----------------------
    # Base de tempo
    # -----------------------

    def get_time_scale(self):

        return float(
            self.query(":TIM:SCAL?")
        )

    def set_time_scale(self,
                       scale: float):

        self.write(
            f":TIM:SCAL {scale}"
        )

    # -----------------------
    # Trigger
    # -----------------------

    def set_trigger_level(self,
                          level: float):

        self.write(
            f":TRIG:EDGE:LEV {level}"
        )

    def get_trigger_level(self):

        return float(
            self.query(":TRIG:EDGE:LEV?")
        )

    def set_trigger_source(self,
                           channel: int):

        self.write(
            f":TRIG:EDGE:SOUR CHAN{channel}"
        )

    # -----------------------
    # Medidas
    # -----------------------

    def measure_frequency(self,
                          channel: int = 1):

        return float(
            self.query(
                f":MEAS:FREQ? CHAN{channel}"
            )
        )

    def measure_period(self,
                       channel: int = 1):

        return float(
            self.query(
                f":MEAS:PER? CHAN{channel}"
            )
        )

    def measure_vpp(self,
                    channel: int = 1):

        return float(
            self.query(
                f":MEAS:VPP? CHAN{channel}"
            )
        )

    def measure_vrms(self,
                     channel: int = 1):

        return float(
            self.query(
                f":MEAS:VRMS? CHAN{channel}"
            )
        )

    #---------------------------
    # Médias 
    #-------------------------

    def get_vmean(self,
                    channel: int = 1):
        return float(
            self.query(f":MEASure:ITEM? VAVG,CHAN{channel}")
        )

    # -----------------------
    # Forma de onda
    # -----------------------

    def set_waveform_source(self,
                            channel: int = 1):

        self.write(
            f":WAV:SOUR CHAN{channel}"
        )

    def set_waveform_mode(self,
                          mode="RAW"):

        self.write(
            f":WAV:MODE {mode}"
        )

    def set_waveform_format(self,
                            fmt="BYTE"):

        self.write(
            f":WAV:FORM {fmt}"
        )

    def get_preamble(self):

        return self.query(":WAV:PRE?")

    def get_waveform_raw(self):

        return self.query_block(":WAV:DATA?")
    def read_waveform(self, channel: int, modo: str = "NORM", fmt: str = "BYTE") -> Waveform:
        
        if modo.upper() == "RAW":
            self.stop()
            self.wait()

        self.set_waveform_source(channel)
        self.set_waveform_mode(modo)
        self.set_waveform_format(fmt)
        preamble_str = self.get_preamble()

        params = preamble_str.split(',')
        if len(params) < 10:
            raise RuntimeError("Preâmbulo inválido.")
        
        preamblereturn = Preamble(
            format=int(params[0]),
            wavetype=int(params[1]),
            points=int(params[2]),
            count=int(params[3]),
            xincrement=float(params[4]),
            xorigin=float(params[5]),
            xreference=float(params[6]),
            yincrement=float(params[7]),
            yorigin=float(params[8]),
            yreference=float(params[9]),
        )

        raw = self.get_waveform_raw()

        if len(raw) == 0:
            raise RuntimeError("Nenhum dado retornado.")

        if np is not None:
            raw_array = np.frombuffer(raw, dtype=np.uint8)
            n_points = min(preamblereturn.points, len(raw_array))
            raw_array = raw_array[:n_points]
            
            tempos = preamblereturn.xorigin + np.arange(n_points) * preamblereturn.xincrement
            tensoes = (raw_array - preamblereturn.yorigin - preamblereturn.yreference) * preamblereturn.yincrement
        else:
            n_points = min(preamblereturn.points, len(raw))
            tempos = [preamblereturn.xorigin + i * preamblereturn.xincrement for i in range(n_points)]
            tensoes = [(raw[i] - preamblereturn.yorigin - preamblereturn.yreference) * preamblereturn.yincrement for i in range(n_points)]

        if modo.upper() == "RAW":
            self.run()

        return Waveform(
            tempo=tempos,
            tensao=tensoes,
            raw=raw,
            canal=channel,
            modo=modo,
            preamble=preamblereturn,
            timestamp=datetime.now()
        )