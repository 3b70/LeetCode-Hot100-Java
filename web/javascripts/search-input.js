/* Material的查询监听keyup；补上粘贴、手机软键盘和中文输入法的input事件。 */
(() => {
  function attach() {
    const input = document.querySelector('[data-md-component="search-query"]');
    if (!input) return;
    let composing = false;
    const notify = () => input.dispatchEvent(new KeyboardEvent("keyup", {
      key: "Unidentified", bubbles: true
    }));
    input.addEventListener("compositionstart", () => { composing = true; });
    input.addEventListener("compositionend", () => { composing = false; notify(); });
    input.addEventListener("input", () => { if (!composing) notify(); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", attach, { once: true });
  else attach();
})();
