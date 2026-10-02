const vscode = require('vscode');
const { exec } = require('child_process');
const path = require('path');

function activate(context) {
    let disposable = vscode.commands.registerCommand('hus.runInterpreter', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('مافي ملف مفتوح حالياً!');
            return;
        }

        const filePath = editor.document.fileName;
        const scriptDir = path.join(context.extensionPath, 'interpreter');
        const pythonScript = path.join(scriptDir, 'lang.py');

        // أمر تشغيل البايثون على الملف الحالي
        exec(`python3 "${pythonScript}" "${filePath}"`, (error, stdout, stderr) => {
            const outputChannel = vscode.window.createOutputChannel("Hus Output");
            outputChannel.clear();
            
            if (error) {
                outputChannel.appendLine(`خطأ في التنفيذ:\n${stderr}`);
                outputChannel.show(true);
                return;
            }
            
            outputChannel.appendLine(stdout);
            outputChannel.show(true);
        });
    });

    context.subscriptions.push(disposable);
}

function deactivate() {}

exports.activate = activate;
exports.deactivate = deactivate;