# Optical Fiber Simulator

A Python application that visualizes how light propagates through single-mode and multi-mode optical fibers. It includes:

- **3D Visualization**: Transparent core and cladding renderings using Matplotlib’s `plot_surface`.
- **Pulse Simulation**: A Gaussian-shaped pulse travels down the single-mode fiber, showing attenuation over distance.
- **Modal Rays**: Multiple rays reflect within the multi-mode core, illustrating modal dispersion.
- **Real-Time Graphs**: Dynamic plots of signal strength versus time for each fiber type.
- **Interactive GUI**: Controls for starting, pausing, resetting the simulation, step-by-step explanations, and live parameter updates via sliders.

---

## 🔧 Requirements

- **Python 3.7 or higher**
- **NumPy**: Numerical operations and array handling
- **Matplotlib**: 2D/3D plotting and animations
- **Tkinter**: Graphical interface (bundled with most Python installations)

Install with:
```bash
pip install numpy matplotlib
```

---

## ▶️ Running the Simulator

1. **Clone or download** the repository.
2. (Optional) **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate    # Windows: venv\\Scripts\\activate
   ```
3. **Launch**:
   ```bash
   python optical_fiber_simulator.py
   ```

A window will open displaying two 3D fiber models and two signal-strength graphs beneath.

---

## 🕹️ GUI Controls

- **Start / Pause / Reset**: Play, pause, or restart the animation sequence.
- **Explain**: Display pop-up messages describing each simulation step (e.g., attenuation, dispersion).
- **Update**: Apply new slider values without restarting the program.

### Parameters via Sliders

| Slider             | Effect                                             |
|--------------------|----------------------------------------------------|
| Attenuation        | Changes exponential loss coefficient (α).          |
| Dispersion         | Adjusts spread of rays in multi-mode core.         |
| Fiber Length       | Sets the axial length of both fibers (in meters).  |

---

## 📂 Code Structure

```text
optical_fiber_simulator.py
```
- **Constants Section**: Define default fiber length, core radii, speeds, attenuation, and dispersion.
- **`draw_fibers()`**: Builds translucent surfaces for core and cladding using meshgrids.
- **`animate(frame)`**: Moves Gaussian pulse and modal rays, updates ring detectors, and refreshes graphs.
- **GUI Setup**: Creates Tkinter buttons and sliders, embeds Matplotlib figure into the window.
- **Explanation Steps**: Sequence of messages guiding through physics concepts.

---

## ⚙️ Key Parameters (Defaults)

| Parameter             | Default | Description                              |
|-----------------------|---------|------------------------------------------|
| `fiber_length`        | 20      | Length of fiber along z-axis             |
| `core_radius_single`  | 0.3     | Radius of single-mode core               |
| `core_radius_multi`   | 1.0     | Radius of multi-mode core                |
| `pulse_speed`         | 0.4     | Speed of Gaussian pulse propagation      |
| `ray_speed`           | 0.25    | Speed of individual multi-mode rays      |
| `attenuation_coeff`   | 0.03    | Exponential attenuation factor (α)        |
| `dispersion_amount`   | 0.1     | Modal dispersion coefficient             |
| `max_frames`          | 300     | Total animation frames                   |

Modify these at the top of the script to experiment with different behaviors.

---

## ⚠️ Troubleshooting

- **Empty Window**: Ensure `root.mainloop()` is called after animation setup.
- **Slow Performance**: Reduce `max_frames` or increase the animation `interval`.
- **No 3D Axes**: Verify Matplotlib has `mplot3d` enabled (`pip install matplotlib`).

---

## 📝 License

MIT License — feel free to adapt and extend for educational or research purposes.
