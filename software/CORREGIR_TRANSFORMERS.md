# Corregir Error de Transformers con TTS

## 🔴 Problema

Error: `ImportError: cannot import name 'BeamSearchScorer' from 'transformers'`

**Causa:** TTS 0.22.0 requiere una versión más antigua de `transformers` que contenga `BeamSearchScorer`, pero tienes instalada la versión 4.57.1 que ya no lo incluye.

## ✅ Solución

Necesitas **downgrade** (bajar la versión) de `transformers` a una versión compatible:

```bash
# Activa tu entorno virtual primero
.\env\Scripts\activate

# Instala la versión compatible de transformers
pip install transformers==4.35.2
```

## 📋 Versiones Compatibles

- **TTS 0.22.0** requiere: `transformers >= 4.20.0, < 4.40.0`
- **Versión recomendada:** `transformers==4.35.2` (última versión que funciona bien con TTS 0.22.0)

## 🔄 Verificar Instalación

Después de instalar, verifica:

```bash
pip show transformers
```

Debería mostrar: `Version: 4.35.2`

## ⚠️ Nota

Si tienes otras librerías que requieren una versión más nueva de `transformers`, tendrás que decidir qué librería usar o encontrar versiones compatibles de ambas.

## 🧪 Probar

Después de corregir, prueba nuevamente el sintetizador. El error debería desaparecer.


