### **1. Minimal Architecture (3 poziomy):**
- **LIMBO**: Problem → Komponenty  
- **DREAM**: Komponenty → Technical specs
- **REALITY**: Specs → Kod

### **2. Zero dependencies oprócz:**
- `requests` (do Ollama)
- `json` (built-in)

### **3. Proste użycie:**

```bash
# Command line
python inceptor.py "system logowania Flask"

# Interactive mode  
python inceptor.py

# Programmatic
from inceptor import quick_solution
result = quick_solution("CI/CD pipeline")
```

## 💻 **Przykład działania:**

```bash
🌀 Simple Dream Architect
==============================
✅ Ollama connection: OK

🎯 Describe your problem: system logowania dla Flask app

🌀 Inception starting for: system logowania dla Flask app
📊 Level 1: LIMBO - Meta Architecture...
   Components: ['authentication', 'session_management', 'user_database']
🎭 Level 2: DREAM - Solution Design...  
   Architecture: Flask app z SQLAlchemy i session management
🌍 Level 3: REALITY - Implementation...
   Files: ['app.py', 'models.py', 'config.py']

==================================================
📋 RESULTS:
==================================================

🏗️ ARCHITECTURE:
   Flask app z SQLAlchemy i session management

💻 TECHNOLOGIES:
   • Flask
   • SQLAlchemy
   • bcrypt

📁 GENERATED FILES:

--- app.py ---
from flask import Flask, request, session
from models import User, db
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/login', methods=['POST'])
def login():
    # Login implementation
    ...

💾 Save files? (y/n): y
   ✅ Saved: output/app.py
   ✅ Saved: output/models.py  
   ✅ Saved: output/config.py
```

## 🔧 **Quick Functions:**

```python
# Tylko kod, bez verbose
files = just_code("monitoring system")
print(files['main.py'])

# Pełne rozwiązanie
solution = quick_solution("REST API z auth")
print(solution['dream']['architecture'])
```

## ⚡ **Setup w 30 sekund:**

```bash
# 1. Uruchom Ollama
ollama serve
ollama pull mistral:7b

# 2. Skopiuj kod do inceptor.py

# 3. Uruchom
python inceptor.py "twój problem"
```

## 🎪 **Dlaczego to działa:**

1. **Prosty flow**: 3 poziomy, jasny przepływ
2. **Error handling**: Fallback jeśli JSON nie parsuje  
3. **Flexible**: CLI + programmatic API
4. **Real output**: Generuje rzeczywiste pliki kodu
5. **No dependencies**: Tylko requests + built-ins

