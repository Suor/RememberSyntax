import sublime
import sublime_plugin

SETTINGS_FILE = "RememberSyntax.sublime-settings"
_tracked = {}  # view_id -> last known syntax path

def plugin_loaded():
    # Ensure settings are loaded
    sublime.load_settings(SETTINGS_FILE)

class RememberSyntaxListener(sublime_plugin.EventListener):
    def on_load_async(self, view):
        path = view.file_name()
        if not path:
            return
        settings = sublime.load_settings(SETTINGS_FILE)
        saved = settings.get("saved", {}).get(path)
        if saved:
            view.assign_syntax(saved)
        # Track current syntax and listen for changes
        view.settings().add_on_change("remember_syntax", lambda: self._check(view))

    def _check(self, view):
        path = view.file_name()
        if not path:
            return
        syntax = view.syntax()
        if not syntax:
            return
        vid = view.id()
        current = syntax.path
        if _tracked.get(vid) != current:
            _tracked[vid] = current
            settings = sublime.load_settings(SETTINGS_FILE)
            saved = settings.get("saved", {})
            saved[path] = current
            settings.set("saved", saved)
            sublime.save_settings(SETTINGS_FILE)

    def on_close(self, view):
        vid = view.id()
        _tracked.pop(vid, None)
        view.settings().clear_on_change("remember_syntax")
