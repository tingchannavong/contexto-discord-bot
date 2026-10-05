import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open
import os
import sys

# Tell Python to look one folder up (the outer folder) for modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture(autouse=True)
def setup_dummy_json_file():
    # 1. Match the exact folder path your bot code expects
    os.makedirs("/app/data", exist_ok=True)
    
    # 2. Create a dummy json file so open() succeeds naturally
    file_path = "/app/data/user_data.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write('{"dummy": "data"}')
            
    yield

@pytest.mark.asyncio
@patch("contexto_bot_dc.bot")
async def test_on_ready_broadcasts_message(mock_bot):

    # Arrange: Set up mock bot states and guilds
    mock_bot.synced = False
    mock_bot.user = "TestBot#1234"

    # Create a mock channel and a mock guild
    mock_channel = AsyncMock()
    mock_channel.name = "general"

    mock_guild = MagicMock()
    mock_guild.name = "Test Server"
    mock_guild.system_channel = None  
    mock_guild.text_channels = [mock_channel]

    mock_permissions = MagicMock()
    mock_permissions.send_messages = True
    mock_channel.permissions_for.return_value = mock_permissions

    mock_bot.guilds = [mock_guild]

    from contexto_bot_dc import bot, on_ready

    # Act: Run the on_ready event handler
    await on_ready()

    # Assert: Verify the message was sent and the sync flag was updated
    mock_channel.send.assert_awaited_once_with("Hello folks, I'm back online!")
    assert mock_bot.synced is True