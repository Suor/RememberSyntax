import fnmatch
import os.path
import sublime
import sublime_plugin

SETTINGS_FILE = "RememberSyntax.sublime-settings"
_rules = {}
_saved = {}    # file_path -> syntax_path, in-memory mirror of settings["saved"]
_assigned = {} # view_id -> syntax_path assigned at load time


class RememberSyntaxListener(sublime_plugin.EventListener):
    def on_load(self, view):
        path = view.file_name()
        if not path:
            return
        syntax = _saved.get(path) or _match_rule(path)
        if syntax:
            view.assign_syntax(syntax)
        _assigned[view.id()] = view.syntax().path if view.syntax() else None
        view.settings().add_on_change("remember_syntax", lambda: self._check(view))

    def _check(self, view):
        path = view.file_name()
        syntax = view.syntax()
        if not path or not syntax:
            return
        vid = view.id()
        current = syntax.path
        if current != _assigned.get(vid):
            _assigned[vid] = _saved[path] = current
            settings = sublime.load_settings(SETTINGS_FILE)
            settings.set("saved", _saved)
            sublime.save_settings(SETTINGS_FILE)

    def on_close(self, view):
        _assigned.pop(view.id(), None)
        view.settings().clear_on_change("remember_syntax")


def plugin_loaded():
    _load_settings()

    listener = RememberSyntaxListener()
    for window in sublime.windows():
        for view in window.views():
            listener.on_load(view)

def _load_settings():
    global _rules, _saved
    settings = sublime.load_settings(SETTINGS_FILE)
    _saved = settings.get("saved", {})
    _rules = settings.get("rules", {})

def _match_rule(path):
    basename = os.path.basename(path)
    for rule in _rules:
        if fnmatch.fnmatch(basename, rule["pattern"]):
            return rule["syntax"]
    return None
