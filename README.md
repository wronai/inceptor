# inceptor
"We need to go deeper"

**DreamArchitect** - do wielopoziomowego generowania architektur rozwiązań z Ollama Mistral:7b!

## 🚀 **Kluczowe możliwości:**

### **1. Automatyczna analiza kontekstu** 
```python
architect = DreamArchitect()
solution = architect.inception("Potrzebuję monitoring dla microservices")
```

**Biblioteka automatycznie wyciąga:**
- 🔧 **Technologie**: Python, React, Docker, AWS...
- 🎯 **Typ problemu**: logging, security, performance...  
- 📊 **Skala**: small/medium/enterprise
- ⚡ **Urgency**: urgent/normal/nice-to-have
- 🚧 **Constraints**: budget, timeline, compliance...

### **2. Wielopoziomowa architektura (3-5 levels):**

- **LIMBO** (Meta): Problem → Komponenty architektury
- **DREAM** (Design): Komponenty → Technical specs  
- **REALITY** (Code): Specs → Gotowy kod
- **DEEPER** (Integration): Code → Deployment/Monitoring
- **DEEPEST** (Evolution): System → Optimization/Scaling

### **3. Inteligentne prompty dla Mistral:7b:**

Każdy level ma zoptymalizowane prompty z:
- **Context injection** 
- **JSON structured output**
- **Dependency tracking**
- **Progressive refinement**

## 🎯 **Przykłady użycia:**

### **Proste:** 
```python
# Jedna linijka
solution = quick_solution("System logowania fullstack", levels=3)
```

### **Zaawansowane:**
```python
solution = architect.inception(
    "CI/CD z AI code review dla team 10 osób", 
    max_levels=4,
    additional_context={
        "budget": "high",
        "security": "enterprise", 
        "timeline": "1 month"
    }
)
```

### **Analiza kontekstu:**
```python
context = analyze_context("Potrzebuję urgent security audit dla GDPR compliance")
# Wynik: {'urgency': ['urgent'], 'constraints': ['security', 'gdpr']}
```

## 🔥 **Mocne strony:**

1. **Zero-setup** - działa od razu z lokalnym Ollama
2. **Context-aware** - rozumie twoje potrzeby z jednego zdania
3. **Scalable** - od simple (3 levels) do complex (5 levels)
4. **Structured output** - wszystko w JSON, łatwe do parsowania
5. **Error handling** - graceful fallbacks jeśli Mistral nie generuje poprawnego JSON

