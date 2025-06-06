# 📚 Dokumentacja Inceptor - Struktura plików


## 📄 Przykładowe pliki dokumentacji:

### docs/index.md
```markdown
# 🌀 Inceptor

**Multi-Level Solution Architecture Generator**

Inceptor to potężne narzędzie AI wykorzystujące Ollama Mistral:7b do generowania wielopoziomowych architektur rozwiązań. Inspirowane filmem "Inception", tworzy zagnieżdżone zadania prowadzące do kompletnych implementacji.

## ✨ Kluczowe funkcje

- 🧠 **AI-Powered**: Integracja z Ollama Mistral:7b
- 🏗️ **Multi-Level**: 3-5 poziomów architektury (LIMBO → DREAM → REALITY → DEEPER → DEEPEST)
- 🔍 **Context-Aware**: Automatyczna analiza kontekstu z jednego zdania
- 💻 **Interactive CLI**: Rich shell interface
- 📊 **Structured Output**: JSON/YAML export
- 🚀 **Zero-Setup**: Działa od razu z lokalnym Ollama

## 🚀 Quick Start

```bash
# Instalacja
pip install inceptor

# Uruchomienie
inceptor "potrzebuję system logowania dla Flask + React"

# Interaktywny shell
inceptor shell
```

[Get Started →](quick-start.md){ .md-button .md-button--primary }
[View Examples →](examples/){ .md-button }
```

### docs/installation.md
```markdown
# 📦 Instalacja

## Wymagania systemowe

- Python 3.8+
- Ollama z Mistral:7b model
- 4GB RAM (minimum)
- Połączenie internetowe (do pobrania modelu)

## Instalacja Ollama

### macOS/Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral:7b
```

### Windows
[Pobierz installer](https://ollama.ai/download) i uruchom:
```cmd
ollama pull mistral:7b
```

## Instalacja Inceptor

### Przez pip (Recommended)
```bash
pip install inceptor
```

### Z źródła
```bash
git clone https://github.com/yourusername/inceptor.git
cd inceptor
pip install -e .
```

### Development setup
```bash
git clone https://github.com/yourusername/inceptor.git
cd inceptor
pip install -e ".[dev]"
```

## Weryfikacja instalacji

```bash
# Sprawdź Ollama
ollama list

# Sprawdź Inceptor
inceptor --version
inceptor status
```
```

### docs/guide/basic-usage.md
```markdown
# 📖 Basic Usage

## Pierwsze kroki

### 1. Generowanie prostej architektury

```bash
inceptor "system logowania dla aplikacji web"
```

### 2. Ustawienie liczby poziomów

```bash
inceptor "CI/CD pipeline" --levels 4
```

### 3. Interaktywny shell

```bash
inceptor shell
```

W shell można używać:

```bash
dream> dream "monitoring system dla microservices"
dream> show
dream> save my_monitoring_system
dream> export json
```

## Przykłady komend

### Analiza kontekstu
```bash
dream> context "urgent Python security audit dla GDPR compliance"
```

### Różne formaty output
```bash
# JSON output
inceptor "problem" --output json

# YAML output  
inceptor "problem" --output yaml

# Rich summary (default)
inceptor "problem" --output summary
```

### Praca z workspace
```bash
dream> workspace        # Otwiera folder
dream> history          # Historia komend
dream> config           # Konfiguracja
```
```

## 🚀 Uruchomienie dokumentacji:

```bash
# Instalacja MkDocs
pip install mkdocs-material mkdocstrings[python] mkdocs-awesome-pages-plugin

# Development server
mkdocs serve

# Build static site
mkdocs build

# Deploy to GitHub Pages
mkdocs gh-deploy
```

## 🎨 Customizacja:

### Custom CSS (docs/assets/css/custom.css):
```css
:root {
  --md-primary-fg-color: #1976d2;
  --md-accent-fg-color: #00bcd4;
}

.md-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.inception-logo {
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

### Custom JavaScript (docs/assets/js/custom.js):
```javascript
// Terminal animation for code examples
document.addEventListener('DOMContentLoaded', function() {
  // Initialize terminal animations
  const terminals = document.querySelectorAll('.termynal');
  terminals.forEach(terminal => {
    new Termynal(terminal);
  });
});
```


**Następne kroki:**
1. Stwórz folder `docs/` i dodaj podstawowe pliki
2. Uruchom `mkdocs serve` 
3. Dostosuj treść do swojego projektu
4. Deploy na GitHub Pages z `mkdocs gh-deploy`