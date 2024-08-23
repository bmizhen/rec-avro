# see https://github.com/bmizhen/rec-avro/blob/master/LICENSE

from rec_avro import *
import io
from fastavro import writer, reader, schema


def rec_test_data():
    return [
        (1, 1),
        (1 / 4, 1 / 4),  # 1/3 would not come back exact from avro read/write
        ('str', 'str'),
        ([], {'_': []}),
        ([[]], {'_': [{'_': []}]}),
        ({'a': [[]]}, {'_': {'a': {'_': [{'_': []}]}}}),
        ([1, '2', [3, '4', None]], {'_': [1, '2', {'_': [3, '4', None]}]}),
        ([[1, 2, {'a': []}]], {'_': [{'_': [1, 2, {'_': {'a': {'_': []}}}]}]}),
        ({}, {'_': {}}),
        ([{}], {'_': [{'_': {}}]}),
        ({'a': 'b'}, {'_': {'a': 'b'}}),
        ({'_': {}}, {'_': {'_': {'_': {}}}}),
        ({'_': [1, 2, 3]}, {'_': {'_': {'_': [1, 2, 3]}}})
    ]


def test_to_rec_avro_destructive():
    assert to_rec_avro_destructive(None) is None
    assert to_rec_avro_destructive(True) is True
    assert to_rec_avro_destructive(False) is False
    for a, b in rec_test_data():
        assert to_rec_avro_destructive(a) == b


def test_from_rec_avro_destructive():
    assert from_rec_avro_destructive(None) is None
    assert from_rec_avro_destructive(True) is True
    assert from_rec_avro_destructive(False) is False
    for b, a in rec_test_data():
        assert from_rec_avro_destructive(a) == b


def test_long_roundtrip():
    data_in = list(make_test_data(1000))
    data_out = list(make_test_data(1000))

    assert from_rec_avro_destructive(to_rec_avro_destructive(data_in)) == data_out


def test_avro_roundtrip():
    data_in = [a for a, b in rec_test_data() if isinstance(a, (map, list))]
    data_out = [a for a, b in rec_test_data()if isinstance(a, (map, list))]
    compare_avro_roundtrip(data_in, data_out)


def test_write_read_rec_avro():
    compare_avro_roundtrip(make_test_data(100), make_test_data(100))


def test_json_roundtrip():
    compare_avro_roundtrip(load_json('tests/test_data.json'),
                           load_json('tests/test_data.json'))


def load_json(filename):
    import json

    with open(filename, 'rb') as f:
        return json.load(f)


def make_test_data(n):
    return (
        {'-': [{'LONG_FIELD_NAME': [True, False, None, [1, 2, [1, 2]],
                                    {'a': 'b', 'c': [{'a': [[], []]}]}],
                'a': [{'b': i}, '3', {'c': i * 2}]}]}
        for i in range(n)
    )

def test_rec_avro_marker():
    s = schema.parse_schema(rec_avro_schema())
    assert is_rec_avro_schema(s)

def write_read(in_data):
    buff = io.BytesIO()
    rec_schema = rec_avro_schema()
    writer(buff, schema.parse_schema(rec_schema), in_data)
    buff.seek(0)

    return [r for r in reader(buff)]


def compare_avro_roundtrip(in_data, out_data):
    out = write_read((to_rec_avro_destructive(r) for r in in_data))
    assert [from_rec_avro_destructive(r) for r in out] == list(out_data)


def make_float_data():
    return ({'a': [10.3 / (i + 1)]} for i in range(10))


def _test_write_read_float_data():
    compare_avro_roundtrip(make_float_data(), make_float_data())
