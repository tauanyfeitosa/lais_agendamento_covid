class AgendamentoLotadoException(Exception):
    def __init__(self, message, field=None):
        super().__init__(message)
        self.field = field
