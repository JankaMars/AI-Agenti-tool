🧠 UKOL_1  OpenAI Assistant – Sčítání čísel pomocí funkčních nástrojů

Tento projekt ukazuje, jak pomocí OpenAI API (model gpt-3.5-turbo) vytvořit asistenta, který dokáže vyhodnotit výraz jako 10 + 32 pomocí vlastní funkce, kterou si AI sama zvolí a zavolá (function calling).
📦 Co kód dělá?

    Načte API klíč z .env souboru.
    Definuje funkci add_numbers, která sčítá dvě čísla.
    Předá OpenAI modelu seznam nástrojů (funkcí), které má k dispozici.
    Model automaticky vybere správnou funkci, v tomto případě add_numbers.
    Funkce se vykoná lokálně v Pythonu a výsledek se vrátí zpět modelu jako odpověď.
    Model vygeneruje finální odpověď pro uživatele.

🔧 Požadavky

    Python 3.8+
    openai
    python-dotenv

📦 Instalace

    Naklonuj repozitář nebo ulož skript.
    Vytvoř si .env soubor s následujícím obsahem:

OPENAI_API_KEY=tvůj_openai_klíč

    Nainstaluj závislosti:

pip install openai python-dotenv

    Spusť skript:

python nazev_skriptu.py






# 🧮 LangGraph Kalkulačka s OpenAI API

Tento projekt ukazuje, jak vytvořit jednoduchého agenta pro matematické výpočty pomocí [LangGraph](https://github.com/langchain-ai/langgraph) a OpenAI API. Agent využívá tzv. **tools** (nástroje) pro operace jako sčítání, odčítání, násobení a dělení.

## ✨ Funkce

- Používá modely `gpt-4.1-mini`od OpenAI.
- Má vlastní nástroje pro:
  - `sum` – sčítání dvou čísel
  - `subtract` – odečítání
  - `multiply` – násobení
  - `divide` – dělení (s ošetřením dělení nulou)
- Využívá stavový graf (`StateGraph`) k řízení logiky mezi plánovačem, vykonáním nástroje a finální odpovědí.

## 🧱 Struktura

Projekt obsahuje jeden hlavní skript, který definuje:

- **Nástroje** (`tools`)
- **Uzly grafu**: `planner`, `tool`, `final`
- **Řízení toku pomocí LangGraph**
- **Počáteční `state` se zprávami a vstupem uživatele**

## 🧰 Závislosti

Nezapomeň nainstalovat potřebné balíčky:

```bash
pip install openai langgraph python-dotenv

🔐 .env soubor

Vytvoř .env soubor v kořeni projektu s následujícím obsahem:

OPENAI_API_KEY=tvůj_openai_klíč

▶️ Spuštění

Skript můžeš spustit přímo (Ukol_Calculator.py):

python Ukol_Calculator.py

Ve skriptu je přednastavený vstup:

state = {
    "messages": [
        {"role": "system", "content": "Jsi pomocný agent, který fungule pomocí nástrojů jako jednoduchá kalkulačka."},
        {"role": "user", "content": "vyděl 10 a 0?"}
    ]
}

Agent vyhodnotí dotaz, případně použije nástroj, a vrátí odpověď.
🔄 Tok agenta

User ➝ [Planner] ➝ [Tool] (pokud potřeba) ➝ [Final] ➝ Odpověď






# 🧠 LangGraph Agent: Kalkulačka + Wikipedia (CS)

Tento projekt demonstruje jednoduchého **tool-based agenta** postaveného na [LangGraph](https://github.com/langchain-ai/langgraph), který:

- 🧮 počítá základní matematické operace
- 🌐 hledá informace na české Wikipedii

Používá OpenAI API a nástroje (tools) pro konkrétní úkoly, které agent plánuje a vyhodnocuje pomocí jazykového modelu.
---

## 📦 Závislosti

Nejprve nainstaluj potřebné knihovny:

```bash
pip install openai langgraph python-dotenv wikipedia

🔐 .env soubor

V kořenové složce projektu vytvoř .env soubor s obsahem:

OPENAI_API_KEY=tvůj_openai_klíč

✨ Podporované nástroje (tools)
Název	Popis
sum	Sčítá dvě čísla
subtract	Odečítá dvě čísla
multiply	Násobí dvě čísla
divide	Dělí dvě čísla (ošetřeno dělení nulou)
wikipedia_search	Vrací shrnutí článku z české Wikipedie
🚀 Spuštění

Skript spusť jako běžný .py soubor:

python Ukol_CalculatorAndWiki.py


Skript obsahuje vstupní stav s uživatelskou otázkou:

state = {
    "messages": [
        {"role": "system", "content": "Jsi pomocný agent, který fungule pomocí nástrojů jako jednoduchá kalkulačka. Dále umíš hledat ve wikipedii"},
        {"role": "user", "content": "Kdo je Jindřich Štreit?"}
    ]
}

Po zpracování proběhne:

planner ➝ tool (je-li třeba) ➝ final ➝ odpověď v terminálu





# 🌐 LangGraph Agent s Webovým Vyhledáváním (SerpAPI)

Tento projekt implementuje jednoduchého agenta postaveného na [LangGraph](https://github.com/langchain-ai/langgraph), který využívá nástroj pro webové vyhledávání přes [SerpAPI](https://serpapi.com/).

## ✨ Funkce

- 🔍 **Webové vyhledávání**: Agent použije `web_search`, pokud detekuje, že dotaz vyžaduje aktuální nebo obecné informace z webu.
- 🧠 **Napojení na OpenAI**: GPT-4 modely plánují použití nástrojů a generují odpověď.
- 🕹️ **LangGraph řízení**: Uzelový systém `planner → tool → final` pro efektivní řízení toku informací.

---

## 📦 Závislosti

```bash
pip install openai langgraph python-dotenv serpapi

🔐 .env soubor

Vytvoř v kořenové složce projektu .env soubor a vlož do něj:

OPENAI_API_KEY=tvůj_openai_api_klíč
SERPAPI_API_KEY=tvůj_serpapi_klíč

🛠️ Nástroj: web_search
Parametr	Typ	       Popis
query	  string	   Dotaz pro vyhledání na webu

Využívá SerpAPI pro získání prvních 3 organických výsledků z Google.
📂 Struktura kódu

    tools: definice a schéma nástrojů (zde pouze web_search)

    planner: GPT model rozhoduje, zda použít nástroj

    tool: zavolá příslušnou funkci a výsledek předá dál

    final: vygeneruje odpověď s využitím historie zpráv a nástrojů

    graph.invoke(state): spustí agenta s definovaným vstupem