# tiny_chat.py – v2 (SymPy-integrated offline assistant, July 30, 2025)

from llama_cpp import Llama
import datetime
import json
import os
import sympy
import re
from sympy.parsing.sympy_parser import parse_expr

# --- System Time & Info ---
now = datetime.datetime.now()
current_year = now.year
current_month = now.strftime("%B")
current_day = now.strftime("%A")
current_date = now.strftime("%B %d, %Y")

# --- Model Path ---
model_path = r"E:\\Project-Nunya\\llama_runner_gpu\\TinyLlama-1.1B-Chat-v1.0-Q4_K_M.gguf"

# --- Load Model ---
llm = Llama(
    model_path=model_path,
    n_ctx=512,
    n_threads=4,
    n_gpu_layers=0,
    verbose=False
)

# --- Load Memory Archive ---
memory_path = "tiny_memory.json"
if os.path.exists(memory_path):
    with open(memory_path, "r", encoding="utf-8") as f:
        memory = json.load(f)
else:
    memory = []

def save_memory(mem):
    with open(memory_path, "w", encoding="utf-8") as f:
        json.dump(mem[-100:], f, indent=2, ensure_ascii=False)

def update_memory(mem, user_msg, assistant_msg):
    assistant_msg = assistant_msg.split("User:")[0].split("###")[0].strip()
    if not assistant_msg or "tinylama.com" in assistant_msg:
        return
    mem.append(f"User said: '{user_msg}' → Assistant replied: '{assistant_msg}'")

# --- Memory Toggle ---
use_memory = False

# --- Natural Language to Math Replacement ---
def normalize_math_words(text):
    word_to_number = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
        "ten": "10", "eleven": "11", "twelve": "12", "thirteen": "13",
        "fourteen": "14", "fifteen": "15", "sixteen": "16", "seventeen": "17",
        "eighteen": "18", "nineteen": "19", "twenty": "20"
    }

    for word, number in word_to_number.items():
        text = re.sub(rf"\b{word}\b", number, text, flags=re.IGNORECASE)

    replacements = {
        r"plus": "+",
        r"add": "+",
        r"minus": "-",
        r"subtract": "-",
        r"times": "*",
        r"multiplied by": "*",
        r"divided by": "/",
        r"over": "/",
        r"squared": "**2",
        r"cubed": "**3",
        r"to the power of (\d+)": r"**\1",
        r"square root of": "sqrt",
        r"the square root of": "sqrt"
    }

    for word, symbol in replacements.items():
        text = re.sub(rf"\b{word}\b", symbol, text, flags=re.IGNORECASE)

    # Fix "2x3" or "3×4" to "2*3"
    text = re.sub(r"(\d)\s*[x×]\s*(\d)", r"\1*\2", text)

    return text

# --- Try SymPy Parsing ---
def try_sympy(user_input):
    try:
        cleaned = normalize_math_words(user_input)

        cleaned = cleaned.lower().strip()
        if cleaned.startswith("what is "):
            cleaned = cleaned[8:]
        elif cleaned.startswith("calculate "):
            cleaned = cleaned[10:]
        cleaned = cleaned.rstrip("?")

        # Final cleanup
        cleaned = cleaned.replace(" x ", " * ")

        if any(op in cleaned for op in ["==", "<", ">", "<=", ">="]):
            return None

        sympy_symbols = sympy.symbols('x y z a b n')
        expr = parse_expr(cleaned, evaluate=True, local_dict={"sqrt": sympy.sqrt})

        if isinstance(expr, sympy.logic.boolalg.Boolean):
            return None

        result = sympy.simplify(expr)
        return str(result)
    except Exception:
        return None

# --- Start Chat Loop ---
print("TinyLlama AGI Mode (Concise Style, With Optional Memory #memoryon/#memoryoff). Type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        print("Exiting TinyLlama. Goodbye!")
        break
    elif user_input.lower() == "#memoryon":
        use_memory = True
        print("[Memory ON]")
        continue
    elif user_input.lower() == "#memoryoff":
        use_memory = False
        print("[Memory OFF]")
        continue

    # --- Try evaluating as SymPy expression ---
    sympy_result = try_sympy(user_input)
    if sympy_result is not None:
        print("\nTinyLlama (via SymPy):", sympy_result)
        continue

    # --- Optional Style Modifier ---
    mode_prompt = ""
    modes = {
        "#funny": "You are a witty and playful assistant.",
        "#serious": "You are a precise and informative assistant.",
        "#sarcastic": "You are a sarcastic assistant who gives dry, witty answers."
    }
    for key in modes:
        if user_input.startswith(key):
            mode_prompt = modes[key] + "\n"
            user_input = user_input[len(key):].strip()
            break

    # --- Prompt Shaping for Short Answers ---
    limiter_prefix = ""
    if "step" in user_input.lower() or "instructions" in user_input.lower():
        limiter_prefix = "(Answer in 5 steps or fewer.) "

    # --- Temperature Control ---
    factual_keywords = ["how many", "what year", "who", "what is", "where", "capital", "president", "date", "day", "month"]
    temperature = 0.4 if any(k in user_input.lower() for k in factual_keywords) else 0.7

    # --- Prompt Construction ---
    system_context = (
        "You are TinyLlama, a helpful and concise AI assistant. "
        "Keep answers under 100 words unless otherwise requested.\n"
        f"(Today is {current_date}. The current year is {current_year}. "
        f"It is the month of {current_month}, and the day is {current_day}.)\n\n"
    )

    recent_mem = "\n".join(memory[-3:]) + "\n" if use_memory and memory else ""
    prompt = (
        system_context
        + mode_prompt
        + recent_mem
        + f"User: {limiter_prefix}{user_input}\nAssistant:"
    )

    try:
        result = llm(
            prompt,
            max_tokens=150,
            temperature=temperature,
            top_p=0.95,
            stop=["User:", "You:", "Assistant:"]
        )
        raw_output = result["choices"][0]["text"].strip()
    except Exception as e:
        print("TinyLlama Error:", e)
        continue

    # --- Post-processing: Trim off any hallucinated junk
    if "\n" in raw_output:
        lines = raw_output.split("\n")
        clean_lines = [l.strip() for l in lines if l.strip() and len(l.strip()) > 3]
        final_output = "\n".join(clean_lines).strip()
    else:
        final_output = raw_output.strip()

    print("\nTinyLlama:", final_output)
    update_memory(memory, user_input, final_output)
    save_memory(memory)

# Made by someone who hoped we wouldn’t need it.
# And who loved someone enough to build it anyway
