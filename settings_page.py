"""Settings page with overlay settings."""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QKeyEvent
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QColorDialog,
    QFrame,
)

import settings_store
from config import CLR_WIDGET_BG, CLR_BUTTON_BG, CLR_TEXT, CLR_TEXT_BRIGHT, CLR_ACTIVE_BTN


def _qt_key_to_hotkey(event: QKeyEvent) -> tuple[str, str] | None:
    key = event.key()

    safe_named_keys = {
        Qt.Key.Key_F1: ("F1", "F1"),
        Qt.Key.Key_F2: ("F2", "F2"),
        Qt.Key.Key_F3: ("F3", "F3"),
        Qt.Key.Key_F4: ("F4", "F4"),
        Qt.Key.Key_F5: ("F5", "F5"),
        Qt.Key.Key_F6: ("F6", "F6"),
        Qt.Key.Key_F7: ("F7", "F7"),
        Qt.Key.Key_F8: ("F8", "F8"),
        Qt.Key.Key_F9: ("F9", "F9"),
        Qt.Key.Key_F10: ("F10", "F10"),
        Qt.Key.Key_F11: ("F11", "F11"),
        Qt.Key.Key_F12: ("F12", "F12"),
        Qt.Key.Key_Insert: ("INSERT", "Insert"),
        Qt.Key.Key_Delete: ("DELETE", "Delete"),
        Qt.Key.Key_Home: ("HOME", "Home"),
        Qt.Key.Key_End: ("END", "End"),
        Qt.Key.Key_PageUp: ("PAGEUP", "Page Up"),
        Qt.Key.Key_PageDown: ("PAGEDOWN", "Page Down"),
        Qt.Key.Key_Space: ("SPACE", "Space"),
        Qt.Key.Key_Slash: ("OEM_2", "/"),
        Qt.Key.Key_Semicolon: ("OEM_1", ";"),
        Qt.Key.Key_Apostrophe: ("OEM_7", "'"),
        Qt.Key.Key_Comma: ("COMMA", ","),
        Qt.Key.Key_Period: ("PERIOD", "."),
        Qt.Key.Key_BracketLeft: ("OEM_4", "["),
        Qt.Key.Key_BracketRight: ("OEM_6", "]"),
        Qt.Key.Key_Minus: ("MINUS", "-"),
        Qt.Key.Key_Equal: ("PLUS", "="),
        Qt.Key.Key_QuoteLeft: ("OEM_3", "`"),
        Qt.Key.Key_Backslash: ("OEM_5", "\\"),
    }
    if key in safe_named_keys:
        return safe_named_keys[key]

    if Qt.Key.Key_A <= key <= Qt.Key.Key_Z:
        label = chr(key)
        return label, label

    if Qt.Key.Key_0 <= key <= Qt.Key.Key_9:
        label = chr(key)
        return label, label

    return None


class SettingsPage(QWidget):
    logout_requested = Signal()
    overlay_always_on_top_changed = Signal(bool)
    restart_requested = Signal()

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self._controller = controller
        self._capturing_hotkey = False
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        header = QLabel("Settings")
        header.setStyleSheet(f"font-size: 36px; font-weight: bold; color: {CLR_TEXT_BRIGHT};")
        layout.addWidget(header)

        color_frame = QFrame()
        color_frame.setStyleSheet(f"QFrame {{ background-color: {CLR_WIDGET_BG}; border-radius: 8px; padding: 16px; }}")
        color_layout = QHBoxLayout(color_frame)
        label = QLabel("Overlay Background Color")
        label.setStyleSheet(f"color: {CLR_TEXT_BRIGHT}; font-size: 22px; font-weight: bold;")
        color_layout.addWidget(label)
        color_layout.addStretch()

        self._color_preview = QFrame()
        self._color_preview.setFixedSize(40, 40)
        self._color_preview.setStyleSheet("border-radius: 4px; border: 1px solid #555;")
        color_layout.addWidget(self._color_preview)

        self._color_btn = QPushButton("Choose Color")
        self._color_btn.setFixedHeight(40)
        self._color_btn.setStyleSheet(
            f"QPushButton {{ background-color: {CLR_BUTTON_BG}; color: {CLR_TEXT}; border-radius: 4px; padding: 0 16px; font-size: 19px; font-weight: bold; }} "
            "QPushButton:hover { background-color: #3e4278; }"
        )
        self._color_btn.clicked.connect(self._pick_color)
        color_layout.addWidget(self._color_btn)
        layout.addWidget(color_frame)

        aot_frame = QFrame()
        aot_frame.setStyleSheet(f"QFrame {{ background-color: {CLR_WIDGET_BG}; border-radius: 8px; padding: 16px; }}")
        aot_layout = QHBoxLayout(aot_frame)

        aot_label = QLabel("Overlay Always on Top")
        aot_label.setStyleSheet(f"color: {CLR_TEXT_BRIGHT}; font-size: 22px; font-weight: bold;")
        aot_layout.addWidget(aot_label)
        aot_layout.addStretch()

        self._aot_btn = QPushButton("On")
        self._aot_btn.setCheckable(True)
        self._aot_btn.setFixedHeight(40)
        self._aot_btn.setFixedWidth(80)
        self._aot_btn.setChecked(settings_store.get_overlay_always_on_top())
        self._aot_btn.clicked.connect(self._on_aot_toggled)
        self._update_aot_style()
        aot_layout.addWidget(self._aot_btn)
        layout.addWidget(aot_frame)

        hotkey_frame = QFrame()
        hotkey_frame.setStyleSheet(f"QFrame {{ background-color: {CLR_WIDGET_BG}; border-radius: 8px; padding: 16px; }}")
        hotkey_layout = QVBoxLayout(hotkey_frame)
        hotkey_layout.setSpacing(10)

        hotkey_top = QHBoxLayout()
        hotkey_label = QLabel("Chat Hotkey")
        hotkey_label.setStyleSheet(f"color: {CLR_TEXT_BRIGHT}; font-size: 22px; font-weight: bold;")
        hotkey_top.addWidget(hotkey_label)
        hotkey_top.addStretch()

        self._chat_hotkey_value = QLabel(settings_store.get_chat_hotkey_label())
        self._chat_hotkey_value.setStyleSheet(f"color: {CLR_TEXT_BRIGHT}; font-size: 22px; font-weight: bold;")
        hotkey_top.addWidget(self._chat_hotkey_value)
        hotkey_layout.addLayout(hotkey_top)

        hotkey_btn_row = QHBoxLayout()
        self._chat_hotkey_btn = QPushButton("Press a Key")
        self._chat_hotkey_btn.setFixedHeight(40)
        self._chat_hotkey_btn.setStyleSheet(
            f"QPushButton {{ background-color: {CLR_BUTTON_BG}; color: {CLR_TEXT_BRIGHT}; border-radius: 4px; padding: 0 16px; font-size: 18px; font-weight: bold; }} "
            f"QPushButton:hover {{ background-color: {CLR_ACTIVE_BTN}; }}"
        )
        self._chat_hotkey_btn.clicked.connect(self._begin_hotkey_capture)
        hotkey_btn_row.addWidget(self._chat_hotkey_btn, 0, Qt.AlignmentFlag.AlignLeft)
        hotkey_btn_row.addStretch()
        hotkey_layout.addLayout(hotkey_btn_row)

        self._chat_hotkey_status = QLabel("Used to open chat during bans, matches, and the post-match screen. F-keys are recommended for best keyboard layout support.")
        self._chat_hotkey_status.setStyleSheet(f"color: {CLR_TEXT}; font-size: 16px;")
        self._chat_hotkey_status.setWordWrap(True)
        hotkey_layout.addWidget(self._chat_hotkey_status)
        layout.addWidget(hotkey_frame)

        layout.addStretch()

        self._logout_btn = QPushButton("Log Out")
        self._logout_btn.setFixedWidth(200)
        self._logout_btn.setFixedHeight(44)
        self._logout_btn.setStyleSheet(
            "QPushButton { background-color: #8b2020; color: white; font-size: 19px; font-weight: bold; border-radius: 6px; } "
            "QPushButton:hover { background-color: #a52a2a; }"
        )
        self._logout_btn.clicked.connect(self._on_logout)
        layout.addWidget(self._logout_btn, alignment=Qt.AlignLeft)

        self._load_current_color()
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _load_current_color(self):
        self._set_preview_color(settings_store.get_overlay_color())

    def _set_preview_color(self, hex_color: str):
        self._color_preview.setStyleSheet(f"background-color: {hex_color}; border-radius: 4px; border: 1px solid #555;")

    def _pick_color(self):
        current = QColor(settings_store.get_overlay_color())
        color = QColorDialog.getColor(current, self, "Overlay Background Color")
        if color.isValid():
            hex_color = color.name()
            settings_store.set_overlay_color(hex_color)
            self._set_preview_color(hex_color)

    def _on_aot_toggled(self, checked: bool):
        self._update_aot_style()
        settings_store.set_overlay_always_on_top(checked)
        self.overlay_always_on_top_changed.emit(checked)

    def _update_aot_style(self):
        checked = self._aot_btn.isChecked()
        self._aot_btn.setText("On" if checked else "Off")
        if checked:
            self._aot_btn.setStyleSheet(
                f"QPushButton {{ background-color: {CLR_ACTIVE_BTN}; color: white; border-radius: 4px; font-size: 19px; font-weight: bold; }}"
            )
        else:
            self._aot_btn.setStyleSheet(
                f"QPushButton {{ background-color: {CLR_BUTTON_BG}; color: {CLR_TEXT}; border-radius: 4px; font-size: 19px; font-weight: bold; }} "
                "QPushButton:hover { background-color: #3e4278; }"
            )

    def _begin_hotkey_capture(self):
        self._capturing_hotkey = True
        self._chat_hotkey_btn.setText("Press any supported key...")
        self._chat_hotkey_status.setText("Press a supported key. F-keys are best for international keyboard layouts. Press Esc to cancel.")
        self.setFocus(Qt.FocusReason.ActiveWindowFocusReason)

    def keyPressEvent(self, event: QKeyEvent):
        if not self._capturing_hotkey:
            return super().keyPressEvent(event)

        if event.key() == Qt.Key.Key_Escape:
            self._capturing_hotkey = False
            self._chat_hotkey_btn.setText("Press a Key")
            self._chat_hotkey_status.setText("Hotkey capture cancelled.")
            event.accept()
            return

        mapped = _qt_key_to_hotkey(event)
        if mapped is None:
            self._chat_hotkey_status.setText("That key is not supported yet. Try an F-key, letter, number, Insert/Delete/Home/End/Page Up/Page Down, punctuation, or Space.")
            event.accept()
            return

        code, label = mapped
        settings_store.set_chat_hotkey(code, label)
        self._chat_hotkey_value.setText(label)
        self._chat_hotkey_btn.setText("Press a Key")
        self._chat_hotkey_status.setText(f"Chat hotkey set to {label}.")
        self._capturing_hotkey = False
        if self._controller is not None:
            self._controller.update_chat_hotkey_setting(code, label)
        event.accept()

    def _on_logout(self):
        self.logout_requested.emit()
