import sublime
import sublime_plugin

SETTINGS_FILE = "RememberSyntax.sublime-settings"
_saved = {}  # file_path -> syntax_path, in-memory mirror of settings["saved"]


def plugin_loaded():
    settings = sublime.load_settings(SETTINGS_FILE)
    _saved.update(settings.get("saved", {}))

    listener = RememberSyntaxListener()
    for window in sublime.windows():
        for view in window.views():
            listener.on_load_async(view)


class RememberSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        path = view.file_name()
        if not path:
            return
        saved = _saved.get(path)
        if saved:
            view.assign_syntax(saved)
        view.settings().add_on_change("remember_syntax", lambda: self._check(view))

    def _check(self, view):
        path = view.file_name()
        syntax = view.syntax()
        if path and syntax and _saved.get(path) != syntax.path:
            _saved[path] = syntax.path
            settings = sublime.load_settings(SETTINGS_FILE)
            settings.set("saved", _saved)
            sublime.save_settings(SETTINGS_FILE)

    def on_close(self, view):
        view.settings().clear_on_change("remember_syntax")
