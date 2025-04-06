# TrixyModel

TrixyModel è un software open-source per la modellazione 3D, sculpting, texturing, UV editing, rigging e altro ancora, ispirato ai migliori strumenti come Blender, ZBrush e Substance Painter.

## ✨ Funzionalità

- Viewport 3D con OpenGL
- Aggiunta primitive: Cube, Sphere, Plane
- Modalità di visualizzazione: Shaded, Wireframe, Vertices, Edit Mode
- Selezione oggetti da scena o clic
- Salvataggio file `.trixym`
- Plugin system (WIP)
- Shortcut personalizzabili
- UI ispirata a Blender

## 🛠️ Requisiti

- Python 3.10+
- PyQt6
- PyOpenGL

## 🚀 Avvio

```bash
pip install -r requirements.txt
python trixymodel/launcher.py
```

## 📂 Struttura del progetto

```
trixymodel/
├── core/           # Logica salvataggio, caricamento
├── ui/             # Interfaccia grafica
├── launcher.py     # Entry point
```

## 🧪 In lavorazione

- Edit mode interattiva
- Sculpting e rigging
- Gizmo manipolatori
- Sistema materiali + UV

---

Made with ❤️ by [Schill0](https://github.com/Schill0)
