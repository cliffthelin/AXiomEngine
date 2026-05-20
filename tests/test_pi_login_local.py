import json
from pathlib import Path

import scripts.settings_manager as settings_manager
from pi.pi import PI, _select_ollama_login_model, handle_login_command


def test_login_aliases_select_local_ollama_models():
    assert _select_ollama_login_model("local") == "ollama/qwen3.6:27b"
    assert _select_ollama_login_model("researcher") == "ollama/gemma4:e2b"
    assert _select_ollama_login_model("skill") == "ollama/cmdmbox/skill-expert"


def test_login_command_persists_global_and_project_ollama_settings(tmp_path, monkeypatch):
    monkeypatch.setenv("PI_CODING_AGENT_DIR", str(tmp_path / ".pi"))
    monkeypatch.chdir(tmp_path)
    settings_manager._manager = None
    pi = PI()

    handle_login_command(pi, ["researcher"], interactive=False)

    global_settings = tmp_path / ".pi" / "agent" / "settings.json"
    project_settings = tmp_path / ".pi" / "settings.json"
    global_data = json.loads(global_settings.read_text())
    project_data = json.loads(project_settings.read_text())
    assert global_data["defaultProvider"] == "ollama"
    assert global_data["defaultModel"] == "ollama/gemma4:e2b"
    assert project_data["defaultProvider"] == "ollama"
    assert project_data["defaultModel"] == "ollama/gemma4:e2b"
    assert pi.agent.state.model == "ollama/gemma4:e2b"
