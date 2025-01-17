"""Common fixtures for the Poolsense tests."""

from collections.abc import Generator
from unittest.mock import AsyncMock, patch

import pytest

from homeassistant.components.poolsense.const import DOMAIN
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD

from tests.common import MockConfigEntry


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock, None, None]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.poolsense.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture
def mock_poolsense_client() -> Generator[AsyncMock, None, None]:
    """Mock a PoolSense client."""
    with (
        patch(
            "homeassistant.components.poolsense.PoolSense",
            autospec=True,
        ) as mock_client,
        patch(
            "homeassistant.components.poolsense.config_flow.PoolSense",
            new=mock_client,
        ),
    ):
        client = mock_client.return_value
        client.test_poolsense_credentials.return_value = True
        yield client


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=DOMAIN,
        title="test@test.com",
        unique_id="test@test.com",
        data={
            CONF_EMAIL: "test@test.com",
            CONF_PASSWORD: "test",
        },
    )
