/**
 * Multi-Agent Code Review Extension
 * ---------------------------------
 * This file defines the VS Code command that runs your Python
 * review orchestrator and displays results in a webview panel.
 */

import * as vscode from "vscode";
import { execFile } from "child_process";
import * as path from "path";

export function activate(context: vscode.ExtensionContext) {
  console.log("🚀 Multi-Agent Code Review Extension Activated");

  const disposable = vscode.commands.registerCommand(
    "review.runFile",
    async () => {
      const editor = vscode.window.activeTextEditor;
      if (!editor) {
        vscode.window.showErrorMessage(
          "No active file. Open a Python file to review."
        );
        return;
      }

      const filePath = editor.document.fileName;
      const workspace =
        vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ||
        path.dirname(filePath);

      // Create a Webview panel to display results
      const panel = vscode.window.createWebviewPanel(
        "multiAgentReview",
        "Multi-Agent Code Review",
        vscode.ViewColumn.Beside,
        { enableScripts: true }
      );

      panel.webview.html = getInitialHTML();

      // Determine Python path (from virtualenv)
      const pythonPath =
        process.platform === "win32"
          ? path.join(workspace, ".venv", "Scripts", "python.exe")
          : path.join(workspace, ".venv", "bin", "python");

      const entry = path.join(workspace, "cli", "main.py");

      // Run the CLI script
      execFile(
        pythonPath,
        [entry, "review", filePath],
        { cwd: workspace },
        (err, stdout, stderr) => {
          if (err) {
            panel.webview.postMessage({
              html: `<pre style="color:red">${stderr || err.message}</pre>`,
            });
            return;
          }

          try {
            const data = JSON.parse(stdout);
            const html = renderResults(data);
            panel.webview.postMessage({ html });
          } catch (e: any) {
            panel.webview.postMessage({
              html: `<pre style="color:red">Error parsing JSON: ${e.message}</pre>`,
            });
          }
        }
      );

      // Listen for messages (if we add interactivity later)
      panel.webview.onDidReceiveMessage((message) => {
        console.log("Received message from webview:", message);
      });
    }
  );

  context.subscriptions.push(disposable);
}

export function deactivate() {
  console.log("🛑 Multi-Agent Code Review Extension Deactivated");
}

/**
 * Initial HTML (loading state)
 */
function getInitialHTML(): string {
  return `
  <!DOCTYPE html>
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      body { font-family: system-ui, sans-serif; padding: 20px; }
      .loading { font-size: 16px; color: gray; }
    </style>
  </head>
  <body>
    <div class="loading">⚙️ Running Multi-Agent Review... Please wait.</div>
    <script>
      const vscode = acquireVsCodeApi();
      window.addEventListener('message', (event) => {
        document.body.innerHTML = event.data.html;
      });
    </script>
  </body>
  </html>`;
}

/**
 * Render formatted results from the Python CLI JSON output
 */
function renderResults(data: any): string {
  const section = (title: string, findings: any[]) => `
    <section>
      <h2 style="margin-top:20px">${title}</h2>
      ${
        findings.length
          ? findings
              .map(
                (f) => `
          <div style="border:1px solid #ccc; border-radius:8px; padding:10px; margin:8px 0;">
            <b>[${f.severity}] ${f.rule_id}</b> — L${f.line}
            <pre style="background:#f6f8fa; padding:8px; border-radius:6px; overflow-x:auto;">
${escapeHtml(f.message || "")}
${f.code_snippet ? "\n" + escapeHtml(f.code_snippet) : ""}
${f.suggestion ? "\n💡 Suggestion: " + escapeHtml(f.suggestion) : ""}
            </pre>
          </div>`
              )
              .join("")
          : "<i>No issues found.</i>"
      }
    </section>`;

  return `
  <html>
  <body style="font-family:system-ui, sans-serif; padding:20px; line-height:1.5;">
    <h1>🤖 Multi-Agent Code Review</h1>
    ${section("🧩 Static Analysis", data.static)}
    ${section("🛡️ Security Findings", data.security)}
    ${section("💬 LLM Reviewer Comments", data.llm)}
  </body>
  </html>`;
}

function escapeHtml(unsafe: string): string {
  return unsafe.replace(/[&<>"']/g, (c) => {
    return {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    }[c] as string;
  });
}
