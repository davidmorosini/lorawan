import base64
import math
import re
from typing import Any, Dict, List, Optional, Union

from py2Solve.macros import RSHIFT23, RSHIFT127, VARIABLES_2SOLVE


def _2pow(exponent: int) -> Union[int, float]:
    """
    Retorna uma exponenciaçãoo de base 2 (2^i).

    Examples:
        >>> _2pow(3)
        8
        >>> _2pow(-3)
        0.125

    Args:
        exponent: Um valor inteiro representando o expoente da potenciação.

    Returns:
        O valor da potenciação de base 2 com o expoente fornecido.

    """
    if exponent >= 0:
        return pow(2, exponent)
    else:
        return math.pow(2, exponent)


def is_hex(string: str) -> bool:
    """
    Verifica se os caracteres de uma string são valores Hexadecimais válidos.

    Examples:
        >>> is_hex("02BA")
        True
        >>> is_hex("02BG")
        False

    Args:
        string: String a ser verificada.

    Returns:
        True caso a string contenha apenas caracteres hexadecimais válidos e False caso contrário.

    """
    hex_pattern = "^[0-9a-fA-F]+$"
    regex = re.compile(hex_pattern)
    return bool(regex.match(string))


def hex_to_dec(hex_string: str) -> int:
    """
    Converte uma string hexadecimal em um número decimal de base 10.

    Examples:
        >>> hex_to_dec("abcd")
        43981
        >>> hex_to_dec("ABCD")
        43981

    Args:
        hex_string: String com os caracteres hexadecimais.

    Returns:
        O valor decimal de base 10 que representa os caracteres hexadecimais.

    """
    hex_base = 16
    return int(hex_string, hex_base)


def base64_to_hex_buffer(base64_str: str) -> List[str]:
    """
    Transforma uma string codificada em base64 para um array de valores hexadecimais.

    Examples:
        >>> base64_to_hex_buffer("dGVzdGU=")
        ['0x74', '0x65', '0x73', '0x74', '0x65']

    Args:
        base64_str: String no formato base64.

    Returns:
        Um array de caracteres hexadecimais representando o conteúdo da string.

    """
    return [hex(p) for p in base64.b64decode(base64_str)]


def base64_string_to_byte_string(base64_str: str) -> str:
    """
    Transforma uma string codificada em base64 para uma string contendo os valores Hexadecimais decodificados.
    Caso o valor do byte seja menor ou igual a '0x0F' será substituído por '0' apenas.

    Examples:
        >>> base64_string_to_byte_string("dGVzdGU=")
        '7465737465'

    Args:
        base64_str: String no formato base64.

    Returns:
        Uma string contendo os valores hexadecimais decodificados.

    """
    buffer = base64_to_hex_buffer(base64_str)
    data = ""
    for byte in buffer:
        if hex_to_dec(byte) <= 0x0F:
            data += "0"
        # removing '0x' from byte string
        data += byte[2:]
    return data


def get_field_name_by_id(field_mapping: Dict[str, List[Union[int, str, None]]], id: int) -> str:
    """
    Recupera a chave do dicionário de nomes de acordo com o identificador.

    Examples:
        >>> get_field_name_by_id({"a": [5, 1, None, "uint"]}, 5)
        "a"

    Args:
        field_mapping: Dicionário com os campos sensoriados e seus atributos.
        id: Identificador atribuído ao campo.

    Returns:
        A chave do dicionário que representa o campo

    Raises:
        Exception: Quando o identificador não for encontrado

    """
    for field, attribs in field_mapping.items():
        if attribs[0] == id:
            return field
    raise Exception(f"ID '{id}' not found")


def float_from_byte_array(byte_array: List[int]) -> float:
    """
    Calcula o valor de um número em ponto flutuante a partir de um array de bytes.

    Examples:
        >>> float_from_byte_array([64, 244, 253, 244])
        7.656000137329102

    Args:
        byte_array: Array com os bytes que formam o valor ponto flutuante.

    Returns:
        Um valor em ponto flutuante.
    """
    byte1 = byte_array[0]
    byte2 = byte_array[1]
    byte3 = byte_array[2]
    byte4 = byte_array[3]
    word_bytes = (((((byte1 * 256) + byte2) * 256) + byte3) * 256) + byte4
    mantissa = word_bytes & 0x007FFFFF
    exponent = (word_bytes & 0x7F800000) >> 23
    sign = (word_bytes >> 31) | 1

    if exponent == 0x000:
        value = (mantissa * RSHIFT23 * 2 * RSHIFT127) if mantissa else 0.0
    elif exponent < 0xFF:
        value = (1 + mantissa * RSHIFT23) * _2pow(exponent - 127)
    else:
        value = math.nan if mantissa else math.inf

    return sign * value


def packet_decode(payload: str, offset: int = 0, fport: Optional[int] = None) -> Dict[str, Any]:
    """
    Realiza a decodificação de uma mensagem provenientes de soluções IOT da 2Solve.

    Examples:
        >>> packet_decode("gB1A9P30gCQAAAAAgB5DxIAAgCUAAAAAgB9C1AAAgCYAAAAAgCNCA6PXgCcAAAAA")
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

    payload_byte_string = base64_string_to_byte_string(payload)

    if not isinstance(offset, int) or not (offset % 1 == 0):
        raise Exception("Offset format must be a positive integer number")

    if offset < 0 or offset > len(payload_byte_string):
        raise Exception("Wrong offset value")

    json2sense = {}

    field_names = list(VARIABLES_2SOLVE.keys())
    while offset < len(payload_byte_string) - 5:
        byte_offset = payload_byte_string[offset : offset + 4]
        id = int(hex_to_dec(byte_offset))

        if id < len(field_names) or id >= 0x8000:
            offset += 4
            field_name = get_field_name_by_id(VARIABLES_2SOLVE, id)
            field = VARIABLES_2SOLVE[field_name]
            field_size = field[1]
            field_value = field[2]
            field_type = field[3]

            end_offset = offset + field_size * 2
            payload_value_offset = payload_byte_string[offset:end_offset]

            if field_type == "float":
                float_byte_array = [
                    int(hex_to_dec(payload_value_offset[0:2])),
                    int(hex_to_dec(payload_value_offset[2:4])),
                    int(hex_to_dec(payload_value_offset[4:6])),
                    int(hex_to_dec(payload_value_offset[6:8])),
                ]

                float_number = float_from_byte_array(float_byte_array)
                field_value = round(float_number, 4)
            elif field_type == "uint":
                field_value = hex_to_dec(payload_value_offset)
            elif field_type == "int16":
                decimal_number = hex_to_dec(payload_value_offset)
                field_value = (decimal_number << 16) >> 16
            elif field_type == "int32":
                decimal_number = hex_to_dec(payload_value_offset)
                field_value = (decimal_number << 32) >> 32

            offset += field_size * 2
            json2sense[field_name] = field_value
        else:
            offset += 1
    return {"json2sense": json2sense}
