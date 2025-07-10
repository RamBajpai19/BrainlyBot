const input = document.getElementById("user-input");
const sendBtn = document.getElementById("send-btn");
const chatBox = document.getElementById("chat-box");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

function appendMessage(content, sender) {
  const msg = document.createElement("div");
  msg.classList.add("message", sender);

  // Format code blocks with ```...``` (basic Markdown support)
  if (content.includes("```")) {
    const parts = content.split("```");
    const html = parts.map((part, index) => {
      if (index % 2 === 1) {
        return `<pre><code>${escapeHTML(part.trim())}</code></pre>`;
      }
      return `<p>${part.trim()}</p>`;
    }).join("");
    msg.innerHTML = html;
  } else {
    msg.textContent = content;
  }

  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function escapeHTML(str) {
  return str.replace(/[&<>'"]/g, tag => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  }[tag]));
}


async function sendMessage() {
  const message = input.value.trim();
  if (!message) return;

  appendMessage(message, "user");
  input.value = "";

  appendMessage("Typing...", "bot");

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: message })

    });

    const data = await res.json();
    document.querySelector(".bot:last-child").remove();
    appendMessage(data.response, "bot");
  } catch (error) {
    document.querySelector(".bot:last-child").remove();
    appendMessage("Oops! Something went wrong.", "bot");
  }
}


window.addEventListener("DOMContentLoaded", () => {
  appendMessage(
    "👋 Welcome to BrainlyBot! I'm your personal tutor — Ask questions, explore subjects, and master concepts with clear, step-by-step help. Ready when you are! 🤖"
  );
});
