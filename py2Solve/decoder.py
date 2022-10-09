from typing import Any, Optional

from py2Solve.tools import packet_decode


class Decoder:
    @classmethod
    def decode(self, payload: str, offset: int = 0, fport: Optional[int] = None) -> Any:
        """
        Realiza a decodificação de uma string de uma solução 2Solve

        Realiza a decodificação de uma mensagem provenientes de soluções IOT da 2Solve.

        Examples:
            >>> from py2Solve import Decoder
            >>> Decoder.decode("gB1A9P30gCQAAAAAgB5DxIAAgCUAAAAAgB9C1AAAgCYAAAAAgCNCA6PXgCcAAAAA")
            {
                'json2sense': {
                    'drainage_PH': 7.656,
                    'drainage_PH_SD': 0.0,
                    'drainage_Turbidity': 393.0,
                    'drainage_Turbidity_SD': 0.0,
                    'drainage_Conductivity': 106.0,
                    'drainage_Conductivity_SD': 0.0,
                    'drainage_Temp': 32.91,
                    'drainage_Temp_SD': 0.0
                }
            }

        Args:
            payload: String com a mensagem do dispositivo.
            offset: Offset de leitura da mensagem.
            fport: FPort utilizado pelo dispositivo para a transmissão da mensagem.

        Returns:
            Um dicionário com os valores decodificados.
        """
        return packet_decode(payload=payload, offset=offset, fport=fport)
