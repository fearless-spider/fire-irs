# pylint: disable=missing-docstring, invalid-name

import re
from copy import deepcopy

import jsonschema
import pytest
from jsonschema import validate
from utils import (INVALID_DOLLAR_AMOUNTS, INVALID_TINS, INVALID_ZIPS,
                   PAYEE_BLANK_MAP, SCHEMA, VALID_ALL_DATA,
                   VALID_DOLLAR_AMOUNTS, VALID_TINS, VALID_ZIPS, check_blanks,
                   check_invalid_amount, check_invalid_tin, check_invalid_zip,
                   check_valid_amount, check_valid_tin, check_valid_zip,
                   check_value_too_long)

from fire.entities import payees

VALID_PAYEE = []
VALID_PAYEE = VALID_ALL_DATA["payees"]


"""
Schema validation tests: payee
"""


def test_payee_schema_ignore_extra_data():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    temp["payees"][0]["extraneous_key"] = "should_be_ignored"
    assert validate(temp, SCHEMA) is None, f"Object: {temp}"


def test_payee_schema_overly_long_values():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    for i, payee in enumerate(temp["payees"]):
        for key, value in payee.items():
            if isinstance(value, str):
                yield check_value_too_long, temp, ["payees", i, key], value + 99 * "A"


def test_payee_schema_amount_codes():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    for i, payee in enumerate(temp["payees"]):
        for key in payee.keys():
            if re.match(r"^payment_amount_", key):
                payload = ["payees", i, key]
                for amount in VALID_DOLLAR_AMOUNTS:
                    yield check_valid_amount, temp, payload, amount
                for amount in INVALID_DOLLAR_AMOUNTS:
                    yield check_invalid_amount, temp, payload, amount


def test_payee_schema_validation_tins():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    for i, _ in enumerate(temp["payees"]):
        for tin in VALID_TINS:
            yield check_valid_tin, temp, ["payees", i, "payees_tin"], tin
        for tin in INVALID_TINS:
            yield check_invalid_tin, temp, ["payees", i, "payees_tin"], tin


def test_payee_schema_zip_codes():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    for i, _ in enumerate(temp["payees"]):
        for zip_code in VALID_ZIPS:
            yield check_valid_zip, temp, ["payees", i, "payee_zip_code"], zip_code
        for zip_code in INVALID_ZIPS:
            yield check_invalid_zip, temp, ["payees", i, "payee_zip_code"], zip_code


@pytest.mark.xfail(raises=jsonschema.exceptions.ValidationError)
def test_missing_required_data():
    temp = {}
    temp["payees"] = deepcopy(VALID_PAYEE)
    del temp["payees"][0]["payees_tin"]
    validate(temp, SCHEMA)


"""
User data transformation tests: payees.xform()
"""


def test_payee_xform_uppercase():
    temp = deepcopy(VALID_PAYEE)
    temp[0]["first_payee_name_line"] = "nocaps mclowercase"
    transformed = payees.xform(temp)
    assert transformed[0]["first_payee_name_line"] == "NOCAPS MCLOWERCASE"


def test_payee_xform_remove_punctuation():
    temp = deepcopy(VALID_PAYEE)
    temp[0]["payees_tin"] = "12-1234567"
    transformed = payees.xform(temp)
    assert transformed[0]["payees_tin"] == "121234567"


def test_payee_xform_adds_system_fields():
    temp = deepcopy(VALID_PAYEE)
    assert "blank_2" not in temp
    transformed = payees.xform(temp)
    assert "blank_2" in transformed[0]


"""
FIRE-formatted ASCII string generation tests: payees.fire()
"""


def test_payee_fire_string_length():
    temp = deepcopy(VALID_PAYEE)
    transformed = payees.xform(temp)
    test_string = payees.fire(transformed)
    assert len(test_string) == 750 * len(temp)


def test_payee_fire_padding_blanks():
    temp = deepcopy(VALID_PAYEE)
    temp[0]["payee_mailing_address"] = "1234 ROADSTREET AVE"
    transformed = payees.xform(temp)
    test_string = payees.fire(transformed)
    addr = test_string[367:407]

    assert addr[0:19] == "1234 ROADSTREET AVE"
    assert addr[19:] == 21 * "\x00"


def test_payee_fire_padding_zeros():
    temp = deepcopy(VALID_PAYEE)
    temp[0]["record_sequence_number"] = "2"
    transformed = payees.xform(temp)
    test_string = payees.fire(transformed)
    sequence_num = test_string[499:507]
    assert sequence_num == "00000002"


def test_payee_fire_blanks_layout():
    temp = deepcopy(VALID_PAYEE)
    transformed = payees.xform(temp)
    test_string = payees.fire(transformed)
    for (offset_1_indexed, inclusive_bound) in PAYEE_BLANK_MAP:
        yield check_blanks, test_string[(offset_1_indexed - 1) : inclusive_bound]
