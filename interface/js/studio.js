/**
 * CodeCraft Python Studio - Client Interactions & Accessibility
 */

document.addEventListener("DOMContentLoaded", () => {
  initCopyButtons();
  initSmoothScroll();
  initKeyboardNav();
});

/**
 * Initializes interactive copy buttons for all code command blocks.
 */
function initCopyButtons() {
  const codeBlocks = document.querySelectorAll(".code-block");

  codeBlocks.forEach((block) => {
    // Only add if not already present
    if (block.querySelector(".copy-btn")) return;

    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.setAttribute("type", "button");
    btn.setAttribute("aria-label", "Copy command to clipboard");
    btn.textContent = "Copy";

    btn.addEventListener("click", async () => {
      const codeElem = block.querySelector("code") || block.querySelector("pre");
      const textToCopy = codeElem ? codeElem.textContent.trim() : block.textContent.trim();

      try {
        await navigator.clipboard.writeText(textToCopy);
        const originalText = btn.textContent;
        btn.textContent = "Copied!";
        btn.style.backgroundColor = "rgba(5, 150, 105, 0.4)";
        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.backgroundColor = "";
        }, 2000);
      } catch (err) {
        // Fallback
        const textarea = document.createElement("textarea");
        textarea.value = textToCopy;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand("copy");
        document.body.removeChild(textarea);
        btn.textContent = "Copied!";
        setTimeout(() => {
          btn.textContent = "Copy";
        }, 2000);
      }
    });

    block.appendChild(btn);
  });
}

/**
 * Adds smooth scroll behavior for in-page anchor links.
 */
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href");
      if (targetId === "#") return;
      const targetElement = document.querySelector(targetId);
      if (targetElement) {
        e.preventDefault();
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });
        targetElement.focus();
      }
    });
  });
}

/**
 * Accessible keyboard navigation helpers.
 */
function initKeyboardNav() {
  const cards = document.querySelectorAll(".assignment-card");
  cards.forEach((card) => {
    const link = card.querySelector("a.btn");
    if (!link) return;
    card.setAttribute("tabindex", "0");
    card.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && document.activeElement === card) {
        link.click();
      }
    });
  });
}
