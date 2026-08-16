// Minimal client-side helpers for the room page.

document.addEventListener("DOMContentLoaded", () => {
    const copyBtn = document.getElementById("copy-code-btn");
    if (!copyBtn) return;

    copyBtn.addEventListener("click", async () => {
        const code = copyBtn.dataset.code;
        if (!code) return;

        try {
            await navigator.clipboard.writeText(code);
            const original = copyBtn.textContent;
            copyBtn.textContent = "Copied!";
            setTimeout(() => {
                copyBtn.textContent = original;
            }, 1500);
        } catch {
            // Clipboard may be unavailable; fail silently.
        }
    });
});
