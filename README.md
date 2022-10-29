# LSP-cspell

A basic spell checker that works well with camelCase code for Sublime's LSP.

Provided through [Spelling Checker](https://github.com/streetsidesoftware/vscode-spell-checker).

### Installation

* Install [LSP](https://packagecontrol.io/packages/LSP) and `LSP-cspell` via Package Control.
* Restart Sublime.

### Configuration

There are some ways to configure the package and the language server.

- From `Preferences > Package Settings > LSP > Servers > LSP-cspell`
- From the command palette `Preferences: LSP-cspell Settings`

### Add-On Language Dictionaries

Steps:
1. Search [npm](https://www.npmjs.com/search?q=%40cspell%2Fdict-) for your dictionary. For example, for the Portuguese dictionary look for `@cspell/dict-pt-pt`.
2. Follow the instructions in the [README](https://www.npmjs.com/package/cspell-dict-pt-pt#user-content-installation) of the package.
3. Set the `"cSpell.language"` to `"pt"` (if you want Portuguese) or `"en,pt"` (if you want English and Portuguese).

### Add-On Specialized Dictionaries

See the following [example](./examples/add-on-specialized-dictionaries) on how to configure specialized dictionaries.
