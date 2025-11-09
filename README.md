# N-D Wireframe Renderer
**Author:** Jerry Yang

A Pygame-based visualization tool for rendering and exploring geometric wireframes in arbitrary dimensions (2D and higher).  
Objects are projected from N-dimensional space onto a 2D plane using perspective projection, allowing interactive rotation, custom line definitions, and preset shapes such as hypercubes and hyperpyramids.

Includes features for command-based editing, file I/O, and real-time visual controls.  
Designed for experimentation, visualization, and learning about higher-dimensional geometry.

---

## Setup

**Requirements:**
- Python 3.9+
- Pygame (`pip install pygame`)

**To run:**
```bash
python main.py
```

---

## Controls

| Key | Action |
|-----|--------|
| `/` | Open command panel |
| Arrow Keys | Rotate / Change rotation plane |
| `=` / `-` | Adjust perspective depth |
| `[` / `]` | Adjust rotation speed |
| `Q` | Toggle scale correction |
| `P` | Cycle color palette |
| `Tab` | Toggle info overlay |
| `Ctrl + S` | Save screenshot |
| Window close | Quit program |

---

## Command Panel

Open the panel with `/` and type a command.  
Available commands:

```
add           - Add a line
remove        - Remove a line
view lines    - View all current lines
preset        - Load a preset (hypercube, hyperpyramid)
center        - Set rotation center
plane         - Set rotation plane
clear         - Clear all lines
load          - Load from file
save          - Save to file
dimensions    - Change number of dimensions
log           - Toggle console logging
help / keys   - View help or key bindings
/             - Exit command panel
```

---

## File Structure

```
N-D-Wireframe-Renderer/
│
├── main.py                # Main program
├── file_shapes/           # Saved wireframe files (.txt)
├── screenshots/           # Saved screenshots (.png)
└── README.md              # Project info
```

---

## Notes / TODO

- [ ] Add screenshots and examples  
- [ ] Split large file into multiple modules  
- [ ] Improve descriptions and docstrings  
- [ ] Add more preset shapes (e.g., simplex, tesseract)  
- [ ] Consider adding mouse control and animations