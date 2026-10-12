try:
    import numpy as np
except ImportError:
    np = None
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Preamble:
    format: int
    wavetype: int
    points: int
    count: int
    xincrement: float
    xorigin: float
    xreference: float
    yincrement: float
    yorigin: float
    yreference: float

    @property
    def sample_rate(self):
        return 1.0 / self.xincrement


@dataclass
class Waveform:
    tempo: any
    tensao: any
    raw: bytes
    canal: int
    modo: str
    preamble: Preamble
    timestamp: datetime

@dataclass
class Pulse:
    waveform: Waveform
    tensao_rampa: float
    tensao_fp: float
    timestamp: datetime