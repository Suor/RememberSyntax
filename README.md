# Remember Syntax

Remember syntax selected for a file in Sublime Text and restore it when the file
is opened again.

This is useful for files with generic names or no extensions, where automatic
syntax detection either picks wrong syntax or gives up.

You can also define filename rules in `RememberSyntax.sublime-settings`:

```js
{
    "rules": [
        {"pattern": "service.*", "syntax": "Packages/INI/INI.sublime-syntax"},
        {"pattern": "http_proxy", "syntax": "Packages/INI/INI.sublime-syntax"}
    ]
}
```

Rules match against basename only and use Python `fnmatch` glob syntax.

When you manually change syntax for an opened file, the plugin saves that choice
under `saved` in its settings and uses it next time. Per-file saved syntax wins
over pattern rules.

