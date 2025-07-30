# Project Nunya

**A fully offline, memory-capable local LLM assistant stack. Built for sovereignty, resilience, and cognitive autonomy.**

---

## 🧠 What It Is

Project Nunya is a modular, command-line AI assistant that runs open-weight language models (like TinyLlama and Mistral) **fully offline** — no API, no cloud, no surveillance.

It includes:

- A custom CLI chat interface (`tiny_chat.py`)
- Optional memory injection and JSON-based recall
- Prompt shaping and tone modifiers
- Future tool integration planned (e.g., math via SymPy, subprocess hooks)
- Model-swapping support via `llama.cpp`

---

## 🌐 Why It Matters

Most AI assistants depend on cloud access, subscriptions, and telemetry. Nunya is different:

- 📴 **Runs offline**
- 🔏 **No telemetry or accounts**
- 🧩 **Customizable prompt flow**
- 🧠 **Modular memory loop**
- ⚙️ **Works on 10-year-old CPUs or with a single GPU**

Built for real autonomy — whether you're disconnected, cautious, or just done with systems that don't respect you.

---

## 🚀 Quick Start

1. Download a GGUF model (e.g. TinyLlama or Mistral)
2. Adjust the model path in `tiny_chat.py`
3. Run the script:

```bash
python tiny_chat.py
```

Type `#memoryon` to enable memory tracking. Type `quit` to exit.

---

## 🖼️ Sample Output

![TinyLlama demo](tiny_chat_demo.png)

---

## 📝 Philosophy

> *“Made by someone who hoped we wouldn’t need it.  
> And who loved someone enough to build it anyway.”*

---

## 📜 License

Apache 2.0  
This project is open, inspectable, and meant to be carried forward.

Contact: `ProjectNunyaDev@protonmail.com`
