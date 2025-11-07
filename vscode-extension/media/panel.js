/*
 * Multi-Agent Code Review — Webview Bridge
 * ----------------------------------------
 * This script runs inside the webview panel.
 * It listens for messages from the VS Code extension backend
 * and updates the UI with the latest review results.
 */

(function () {
  // Access the VS Code API (for secure messaging)
  const vscode = acquireVsCodeApi();

  // Listen for messages from the extension backend
  window.addEventListener("message", (event) => {
    const data = event.data;
    if (data.html) {
      // Replace the current webview content with new HTML
      document.body.innerHTML = data.html;
      // Scroll smoothly to top for readability
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  });

  // Optional: Let user know the panel is ready
  console.log("✅ Multi-Agent Review webview initialized");
})();
