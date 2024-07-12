import pytest

from src.utils import (
    CommandName,
    BotTokenName,
    AutopopArg,
    is_valid_map_number,

)


def test_command_name_enum_values():
    assert CommandName.AUTOPOP == "autopop"
    assert CommandName.POP == "pop"
    assert CommandName.STATUS == "status"
    assert CommandName.HELP == "help"


def test_missing_method_with_known_command():
    assert CommandName._missing_("autopop") == CommandName.AUTOPOP
    assert CommandName._missing_("pop") == CommandName.POP
    assert CommandName._missing_("status") == CommandName.STATUS
    assert CommandName._missing_("help") == CommandName.HELP


def test_missing_method_with_unknown_command():
    assert CommandName._missing_("unknown") is None


def test_missing_method_with_case_insensitive_command():
    assert CommandName._missing_("AutOpOp") == CommandName.AUTOPOP
    assert CommandName._missing_("PoP") == CommandName.POP
    assert CommandName._missing_("StAtUs") == CommandName.STATUS
    assert CommandName._missing_("HeLp") == CommandName.HELP


def test_bot_token_name_enum_values():
    assert BotTokenName.PRODUCTION == "PRODUCTION_BOT_TOKEN"
    assert BotTokenName.DEVELOPMENT == "DEVELOPMENT_BOT_TOKEN"


def test_missing_method_with_known_token():
    assert BotTokenName._missing_("PRODUCTION_BOT_TOKEN") == BotTokenName.PRODUCTION
    assert BotTokenName._missing_("DEVELOPMENT_BOT_TOKEN") == BotTokenName.DEVELOPMENT


def test_missing_method_with_unknown_token():
    assert BotTokenName._missing_("UNKNOWN_BOT_TOKEN") is None


def test_missing_method_with_case_insensitive_token():
    assert BotTokenName._missing_("production_bot_token") == BotTokenName.PRODUCTION
    assert BotTokenName._missing_("development_bot_token") == BotTokenName.DEVELOPMENT


def test_autopop_arg_enum_values():
    assert AutopopArg.ON == "on"
    assert AutopopArg.OFF == "off"


def test_missing_method_with_known_arg():
    assert AutopopArg._missing_("on") == AutopopArg.ON
    assert AutopopArg._missing_("off") == AutopopArg.OFF


def test_missing_method_with_unknown_arg():
    assert AutopopArg._missing_("unknown") is None


def test_missing_method_with_case_insensitive_arg():
    assert AutopopArg._missing_("On") == AutopopArg.ON
    assert AutopopArg._missing_("OfF") == AutopopArg.OFF


def test_is_valid_map_number():
    assert is_valid_map_number('1234') is True
    assert is_valid_map_number(1234) is True

    assert is_valid_map_number('123') is False
    assert is_valid_map_number('12345') is False
    assert is_valid_map_number(123) is False
    assert is_valid_map_number(12345) is False

    assert is_valid_map_number('abcd') is False

    assert is_valid_map_number('12ab') is False

    assert is_valid_map_number('') is False

    assert is_valid_map_number('0123') is True
    assert is_valid_map_number(123) is False

    assert is_valid_map_number('-1234') is False
    assert is_valid_map_number(-1234) is False

    assert is_valid_map_number('12.34') is False
    assert is_valid_map_number(12.34) is False


def test_is_valid_map_number_with_non_string_inputs():
    assert is_valid_map_number(True) is False
    assert is_valid_map_number(False) is False


def test_missing_method_with_non_string_inputs():
    with pytest.raises(TypeError):
        CommandName._missing_(1234)
    with pytest.raises(TypeError):
        BotTokenName._missing_(12.34)
    with pytest.raises(TypeError):
        AutopopArg._missing_(True)
