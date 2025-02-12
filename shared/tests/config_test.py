from os import environ
from pathlib import Path
from unittest import mock

from pytest import mark, raises

from libretime_shared.config import BaseConfig, DatabaseConfig, RabbitMQConfig


# pylint: disable=too-few-public-methods
class FixtureConfig(BaseConfig):
    api_key: str
    database: DatabaseConfig
    rabbitmq: RabbitMQConfig = RabbitMQConfig()


FIXTURE_CONFIG_RAW = """
api_key: "f3bf04fc"

# Comment !
database:
    host: "localhost"
    port: 5432

ignored: "ignored"
"""


def test_base_config(tmp_path: Path):
    config_filepath = tmp_path / "config.yml"
    config_filepath.write_text(FIXTURE_CONFIG_RAW)

    with mock.patch.dict(
        environ,
        {
            "LIBRETIME_API": "invalid",
            "LIBRETIME_DATABASE": "invalid",
            "LIBRETIME_DATABASE_PORT": "8888",
            "LIBRETIME_RABBITMQ_HOST": "changed",
            "WRONGPREFIX_API_KEY": "invalid",
        },
    ):
        config = FixtureConfig(filepath=config_filepath)

        assert config.api_key == "f3bf04fc"
        assert config.database.host == "localhost"
        assert config.database.port == 8888
        assert config.rabbitmq.host == "changed"
        assert config.rabbitmq.port == 5672

    # Optional model: loading default values (rabbitmq)
    with mock.patch.dict(environ, {}):
        config = FixtureConfig(filepath=config_filepath)
        assert config.rabbitmq.host == "localhost"
        assert config.rabbitmq.port == 5672

    # Optional model: overriding using environment (rabbitmq)
    with mock.patch.dict(environ, {"LIBRETIME_RABBITMQ_HOST": "changed"}):
        config = FixtureConfig(filepath=config_filepath)
        assert config.rabbitmq.host == "changed"
        assert config.rabbitmq.port == 5672


FIXTURE_CONFIG_RAW_INI = """
[database]
host = changed
port = 6666
"""


def test_base_config_ini(tmp_path: Path):
    config_filepath = tmp_path / "config.conf"
    config_filepath.write_text(FIXTURE_CONFIG_RAW_INI)

    with mock.patch.dict(
        environ,
        {"LIBRETIME_API_KEY": "f3bf04fc"},
    ):
        config = FixtureConfig(filepath=config_filepath)

        assert config.api_key == "f3bf04fc"
        assert config.database.host == "changed"
        assert config.database.port == 6666


FIXTURE_CONFIG_RAW_MISSING = """
database:
    host: "localhost"
"""

FIXTURE_CONFIG_RAW_INVALID = """
database
    host: "localhost"
"""


@mark.parametrize(
    "raw,exception",
    [
        (FIXTURE_CONFIG_RAW_INVALID, SystemExit),
        (FIXTURE_CONFIG_RAW_MISSING, SystemExit),
    ],
)
def test_load_config_error(tmp_path: Path, raw, exception):
    config_filepath = tmp_path / "config.yml"
    config_filepath.write_text(raw)

    with raises(exception):
        with mock.patch.dict(environ, {}):
            FixtureConfig(filepath=config_filepath)
