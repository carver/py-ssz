import pytest

from ssz import (
    DeserializationError,
    decode,
    encode,
)
from ssz.sedes import (
    Boolean,
)


@pytest.mark.parametrize(
    'value,expected',
    (
        (True, b'\x01'),
        (False, b'\x00'),
    ),
)
def test_boolean_serialize_values(value, expected):
    sedes = Boolean()
    assert sedes.serialize(value) == expected


@pytest.mark.parametrize(
    'value',
    (
        None,
        1,
        0,
        'True',
        b'True',
    ),
)
def test_boolean_serialize_bad_values(value):
    sedes = Boolean()
    with pytest.raises(TypeError):
        sedes.serialize(value)


@pytest.mark.parametrize(
    'value,expected',
    (
        (b'\x01', True),
        (b'\x00', False),
    ),
)
def test_boolean_deserialization(value, expected):
    sedes = Boolean()
    assert sedes.deserialize(value) == expected


@pytest.mark.parametrize(
    'value',
    (
        b' ',
        b'\x02',
        b'\x00\x00',
        b'\x01\x00',
        b'\x00\x01',
        b'\x01\x01',
    ),
)
def test_boolean_deserialization_bad_value(value):
    sedes = Boolean()
    with pytest.raises(DeserializationError):
        sedes.deserialize(value)


@pytest.mark.parametrize(
    'value,expected',
    (
        (True, True),
        (False, False),
    ),
)
def test_boolean_round_trip(value, expected):
    sedes = Boolean()
    assert sedes.deserialize(sedes.serialize(value)) == expected


@pytest.mark.parametrize(
    'value,expected',
    (
        (True, True),
        (False, False),
    ),
)
def test_boolean_round_trip_codec(value, expected):
    sedes = Boolean()
    assert decode(encode(value), sedes) == expected
