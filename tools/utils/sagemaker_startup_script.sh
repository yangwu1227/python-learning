#!/bin/bash
# Startup script for SageMaker Notebook to configure code-server

# Define an array of extension URLs
extension_urls=(
    "https://link-to-extension1.vsix"
    "https://link-to-extension2.vsix"
    # Add more URLs as needed
)

# Install each extension from the list
for url in "${extension_urls[@]}"; do
    echo "Installing extension from: $url"
    curl "$url" --verbose --output temp.vsix
    code-server --install-extension temp.vsix
    rm temp.vsix
done

# Ensure the code-server configuration directory exists
CONFIG_DIR="$HOME/.local/share/code-server"
mkdir -p "$CONFIG_DIR"

# Write keybindings.json
cat >"$CONFIG_DIR/keybindings.json" <<'EOF'
[
    {
        "key": "cmd+enter",
        "command": "jupyter.execSelectionInteractive",
        "when": "editorTextFocus && isWorkspaceTrusted && jupyter.ownsSelection && !findInputFocussed && !notebookEditorFocused && !replaceInputFocussed && editorLangId == 'python'"
    },
    {
        "key": "shift+enter",
        "command": "-jupyter.execSelectionInteractive",
        "when": "editorTextFocus && isWorkspaceTrusted && jupyter.ownsSelection && !findInputFocussed && !notebookEditorFocused && !replaceInputFocussed && editorLangId == 'python'"
    }
]
EOF

# Write settings.json
cat >"$CONFIG_DIR/settings.json" <<'EOF'
{
    "jupyter.interactiveWindow.textEditor.executeSelection": true,
    "autoDocstring.docstringFormat": "numpy",
    "interactiveWindow.executeWithShiftEnter": true,
    "files.insertFinalNewline": true,
    "terminal.integrated.inheritEnv": false,
    "[python]": {
        "diffEditor.ignoreTrimWhitespace": false
    },
    "workbench.colorTheme": "Visual Studio 2017 Dark - C++",
    "diffEditor.ignoreTrimWhitespace": false,
    "python.terminal.activateEnvInCurrentTerminal": true,
    "workbench.iconTheme": "material-icon-theme"
}
EOF

echo "Startup script completed."
