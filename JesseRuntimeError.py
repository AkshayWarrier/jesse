from typing import Tuple

class JesseRuntimeError(RuntimeError):
    def __init__(self, pos: Tuple[int], message: str) -> None:
        super().__init__(message)
        self.pos = pos