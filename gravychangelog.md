## Modified existing files

### Bridge/bridge_controller.py
- Imports added:
  - `settings_store`
  - `updater_service`
  - `BRIDGE_COMPONENT_VERSION`
- `bridge_version_mismatch` signal changed from `Signal(str)` to `Signal(dict)`
- `game_version_mismatch` signal changed from URL-style handling to structured payload handling
- `self.in_postmatch` removed
- Fields added:
  - `_server_bridge_component_version`
  - `_server_game_component_version`
  - `last_game_component_version`
  - `last_version_info`
- Methods added:
  - `_apply_version_info(version_info)`
  - `_build_version_payload(scope, bridge_download_url="")`
  - `_bridge_version_mismatch_detected()`
  - `_push_chat_hotkey_to_game()`
  - `update_chat_hotkey_setting(key_code, key_label)`
- Login version check flow changed to use `_apply_version_info()` and `_bridge_version_mismatch_detected()`
- Reconnect version check flow changed to use `_apply_version_info()` and `_bridge_version_mismatch_detected()`
- On game connect, chat hotkey push added
- `_on_game_version_received(...)` signature changed from `(game_version: float)` to `(game_version: float, game_component_version: str = "")`
- `_on_game_version_received(...)` now checks optional game component version
- `match_result` send flow changed to include `placements_remaining` when available
- Match data caching/profile refresh handling expanded
- Relay handling added or expanded for:
  - match scrapped
  - game to server chat
  - server to game chat
  - seed change request
  - draw request
  - forfeit
  - close postmatch
  - rank reveal to game

### Bridge/config.py
- `BRIDGE_VERSION` changed from `1.11` to `1.12`
- Added:
  - `BRIDGE_COMPONENT_VERSION = "1.10.0"`
  - `GAME_COMPONENT_VERSION = "1.10.0"`
  - `GITHUB_OWNER`
  - `GITHUB_REPO`
  - `LATEST_RELEASE_API`
  - `GITHUB_RELEASES_PAGE`
  - `BRIDGE_ASSET_NAME = "S2Ranked.zip"`
  - `GAME_ASSET_NAME = "SpelunkyRanked.zip"`
  - `APP_FOLDER_NAME = "Ranked App"`
  - `MOD_SUBPATH = os.path.join("Mods", "Packs", "S2ranked")`

### Bridge/login_page.py
- Connection removed:
  - `self._controller.bridge_version_mismatch.connect(self._show_version_mismatch)`

### Bridge/main_window.py
- Imports added:
  - `QApplication`
  - `QSizePolicy`
  - `QScrollArea`
  - `UpdatePanel`
- Window size changed from `960x640` to `960x720`
- State added:
  - `_update_dot`
  - `_update_available`
- Sidebar/nav button styling adjusted
- Update navigation button row added
- Update indicator dot added
- Update page added
- Version mismatch page reworked
- `UpdatePanel` instances added:
  - standard updater panel
  - mismatch repair panel
- Signal hookups changed:
  - `game_version_mismatch` now connects to `_show_version_mismatch`
  - `bridge_version_mismatch` now connects to `_show_version_mismatch`
- `settings_page.restart_requested.connect(QApplication.quit)` added
- `update_completed` hookups added for both update panels
- Methods added:
  - `_build_update_button_row()`
  - `_set_update_indicator(show)`
  - `_create_update_page()`
  - `_on_update_completed(bridge_updated, game_updated)`
  - `_show_version_mismatch(payload)`
  - `_check_update_indicator()`
- `_create_version_mismatch_page()` changed
- Old `_show_game_version_mismatch(download_url)` flow removed
- Login success flow updated to refresh updater labels and delayed update indicator check

### Bridge/overlay_window.py
- `_on_progress` signature changed from `(area, level, theme)` to `(area, theme)`

### Bridge/settings_page.py
- Added signal:
  - `restart_requested = Signal()`
- Added state:
  - `_capturing_hotkey`
- Added function:
  - `_qt_key_to_hotkey(event)`
- Added chat hotkey UI elements:
  - current hotkey display
  - capture button
  - status/help text
- Added methods:
  - `_begin_hotkey_capture()`
  - overridden `keyPressEvent(...)`
- `self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)` added
- Logout flow changed to emit `logout_requested` without directly clearing login creds in this page

### Bridge/settings_store.py
- Added:
  - `get_update_game_dir()`
  - `set_update_game_dir(path)`
  - `get_update_app_dir()`
  - `set_update_app_dir(path)`
  - `get_chat_hotkey_code()`
  - `get_chat_hotkey_label()`
  - `set_chat_hotkey(code, label)`
- Default chat hotkey values added:
  - code `F8`
  - label `F8`

### Bridge/udp_relay.py
- `game_version_received` signal changed from `Signal(float)` to `Signal(float, str)`
- `version_response` handling changed to emit:
  - `float(data.get("version", 0.0))`
  - `str(data.get("component_version", ""))`

## Added source-level files

### Bridge/update_panel.py
- New file added
- Contains:
  - `UpdateCheckWorker`
  - `UpdateInstallWorker`
  - `UpdatePanel`

### Bridge/updater_service.py
- New file added
- Contains:
  - `normalize_version(value)`
  - `default_app_install_dir()`
  - `find_game_root()`
  - `current_app_dir()`
  - `download_file(url, out_path, progress_callback=None)`
  - `resolve_release_assets(server_version_info=None)`
  - `install_game_mod(zip_path, game_root)`
  - `install_bridge(zip_path, target_dir, version_text)`
  - `_write_version_file(...)`
  - `launch_update_script(script_path)`

### main.lua
- New file added
- Bundled Lua mod file present in new zip

## No removed files

- No files removed from original zip
