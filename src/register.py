class Register:
    def __init__(self):
        self._i = 0
        self._pc = 0
        self._sp = 0xF
        self._delay_reg = 0
        self._sound_reg = 0
        self.v = bytearray(16)

    @property
    def i(self):
        return self._i

    @i.setter
    def i(self, value):
        self._i = self._validate_16bit(value)

    @property
    def pc(self):
        return self._pc

    @pc.setter
    def pc(self, value):
        self._pc = self._validate_16bit(value)

    # Getter y Setter para 'sp'
    @property
    def sp(self):
        return self._sp

    @sp.setter
    def sp(self, value):
        self._sp = self._validate_8bit(value)

    @property
    def delay_reg(self):
        return self._delay_reg

    @delay_reg.setter
    def delay_reg(self, value):
        self._delay_reg = self._validate_8bit(value)

    @property
    def sound_reg(self):
        return self._sound_reg

    @sound_reg.setter
    def sound_reg(self, value):
        self._sound_reg = self._validate_8bit(value)

    @staticmethod
    def _validate_8bit(value):
        if not (0 <= value <= 255):
            raise ValueError(f"El valor {value} está fuera del rango de 8 bits (0-255).")
        return value

    @staticmethod
    def _validate_16bit(value):
        if not (0 <= value <= 65535):
            raise ValueError(f"El valor {value} está fuera del rango de 16 bits (0-65535).")
        return value
