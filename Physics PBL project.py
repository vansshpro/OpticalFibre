# Optical Fiber Simulation with GUI, Real-Time Graphs, Interactive Explanation, and Full 3D Features
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

# Constants
fiber_length = 20
core_radius_single = 0.3
core_radius_multi = 1.0
incident_angle_multi = np.radians(30)
ray_speed = 0.25
pulse_speed = 0.4
dz_multi = 2 * core_radius_multi / np.tan(incident_angle_multi)
dispersion_amount = 0.1
attenuation_coeff = 0.03
max_frames = 300

# Setup Tkinter GUI
root = tk.Tk()
root.title("Optical Fiber Simulator")

# Variables for interactive sliders
def update_constants():
    global attenuation_coeff, dispersion_amount, fiber_length
    attenuation_coeff = att_slider.get()
    dispersion_amount = disp_slider.get()
    fiber_length = length_slider.get()

    ax_graph_single.clear()
    ax_graph_single.set_xlim(0, max_frames)
    ax_graph_single.set_ylim(0, 100)
    ax_graph_single.set_title("Single-mode Signal Strength")

    ax_graph_multi.clear()
    ax_graph_multi.set_xlim(0, max_frames)
    ax_graph_multi.set_ylim(0, 100)
    ax_graph_multi.set_title("Multi-mode Signal Strength")

    draw_fibers()

# Explanation steps
step_text = [
    "This is a 3D simulation of signal propagation in optical fibers.",
    "On the left, you see a single-mode fiber where the signal travels straight.",
    "On the right, multi-mode fiber shows multiple rays bouncing with reflections.",
    "Attenuation reduces signal strength as light travels.",
    "Dispersion in multi-mode causes spreading and reduces clarity.",
    "The detector ring at the end captures remaining signal strength.",
    "Graphs show real-time signal strength fading due to attenuation."
]

def explain():
    for text in step_text:
        messagebox.showinfo("Explanation", text)

# Figure and subplots
fig = plt.figure(figsize=(12, 8))
ax_single = fig.add_subplot(221, projection='3d')
ax_multi = fig.add_subplot(222, projection='3d')
ax_graph_single = fig.add_subplot(223)
ax_graph_multi = fig.add_subplot(224)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=0, column=0, columnspan=6)

# Signal storage
signal_single, signal_multi = [], []
ray_lines_multi = []

# Pulse and rays initialization
phase_offsets_multi = np.linspace(0, dz_multi, 5)
ray_line_single, = ax_single.plot([], [], [], lw=3, color='magenta')
ray_particles = ax_single.scatter([], [], [], s=10, c=[], cmap='plasma')
ray_lines_multi = [ax_multi.plot([], [], [], lw=2, color='gold')[0] for _ in range(5)]
ring_single, = ax_single.plot([], [], [], color='lime')
ring_multi, = ax_multi.plot([], [], [], color='lime')
graph_single, = ax_graph_single.plot([], [], color='magenta')
graph_multi, = ax_graph_multi.plot([], [], color='gold')

frame_counter = [0]

# Draw fibers
z = np.linspace(0, fiber_length, 200)
theta = np.linspace(0, 2 * np.pi, 60)
Z, T = np.meshgrid(z, theta)

def draw_fibers():
    for ax, core_radius in zip([ax_single, ax_multi], [core_radius_single, core_radius_multi]):
        for coll in ax.collections[:]:
            try:
                if hasattr(coll, "_facecolors3d"):
                    ax.collections.remove(coll)
            except Exception:
                pass
        cladding_radius = core_radius * 1.3
        Z, T = np.meshgrid(np.linspace(0, fiber_length, 200), np.linspace(0, 2 * np.pi, 60))
        ax.plot_surface(cladding_radius * np.cos(T), cladding_radius * np.sin(T), Z, alpha=0.03, color='white')
        ax.plot_surface(core_radius * np.cos(T), core_radius * np.sin(T), Z, alpha=0.06, color='deepskyblue')
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_zlim(0, fiber_length)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])

# Initial fiber draw
draw_fibers()

# Animation function
def animate(frame):
    frame_counter[0] = frame
    z = np.linspace(0, fiber_length, 300)
    center = (frame * pulse_speed) % (fiber_length + 10) - 5
    envelope = np.exp(-0.5 * ((z - center) / 1.2)**2)
    beam = envelope * np.sin(10 * z)
    attenuation = np.exp(-attenuation_coeff * z)
    beam *= attenuation
    x = beam
    y = np.zeros_like(z)
    ray_line_single.set_data(x, y)
    ray_line_single.set_3d_properties(z)
    ray_particles._offsets3d = (x[::10], y[::10], z[::10])
    ray_particles.set_array(attenuation[::10])
    s_strength = envelope[z > fiber_length - 1].sum() * 100 * np.exp(-0.005 * frame)
    signal_single.append(s_strength if not signal_single else 0.9 * signal_single[-1] + 0.1 * s_strength)

    if s_strength > 2:
        ang = np.linspace(0, 2 * np.pi, 100)
        ring_single.set_data(core_radius_single * np.cos(ang), core_radius_single * np.sin(ang))
        ring_single.set_3d_properties(np.full_like(ang, fiber_length))
    else:
        ring_single.set_data([], [])
        ring_single.set_3d_properties([])

    m_strengths = []
    for i, line in enumerate(ray_lines_multi):
        z_vals, x_vals = [], []
        z_pos = (frame * ray_speed + phase_offsets_multi[i]) % dz_multi
        x_pos, dir_x = 0, 1
        disp = dispersion_amount * (i - 2)
        while z_pos < fiber_length:
            next_z = min(z_pos + dz_multi, fiber_length)
            next_x = dir_x * (core_radius_multi + disp)
            z_vals += [z_pos, next_z]
            x_vals += [x_pos, next_x]
            z_pos, x_pos = next_z, next_x
            dir_x *= -1
        alpha = np.exp(-attenuation_coeff * z_vals[-1])
        line.set_data(x_vals, [0]*len(x_vals))
        line.set_3d_properties(z_vals)
        line.set_alpha(alpha)
        if z_vals[-1] >= fiber_length - 1:
            m_strengths.append(alpha * 100)

    m_avg = np.mean(m_strengths) * np.exp(-0.005 * frame) if m_strengths else 0
    signal_multi.append(m_avg if not signal_multi else 0.9 * signal_multi[-1] + 0.1 * m_avg)

    if m_avg > 2:
        ang = np.linspace(0, 2 * np.pi, 100)
        ring_multi.set_data(core_radius_multi * np.cos(ang), core_radius_multi * np.sin(ang))
        ring_multi.set_3d_properties(np.full_like(ang, fiber_length))
    else:
        ring_multi.set_data([], [])
        ring_multi.set_3d_properties([])

    graph_single.set_data(np.arange(len(signal_single)), signal_single)
    graph_multi.set_data(np.arange(len(signal_multi)), signal_multi)
    ax_graph_single.set_xlim(0, max_frames)
    ax_graph_single.set_ylim(0, 100)
    ax_graph_single.set_title("Single-mode Signal Strength")
    ax_graph_multi.set_xlim(0, max_frames)
    ax_graph_multi.set_ylim(0, 100)
    ax_graph_multi.set_title("Multi-mode Signal Strength")

ani = FuncAnimation(fig, animate, frames=max_frames, interval=50, blit=False)

# GUI Buttons and Sliders
tk.Button(root, text="Start", command=lambda: ani.event_source.start()).grid(row=1, column=0)
tk.Button(root, text="Pause", command=lambda: ani.event_source.stop()).grid(row=1, column=1)

def reset_simulation():
    global signal_single, signal_multi
    ani.event_source.stop()
    signal_single.clear()
    signal_multi.clear()
    frame_counter[0] = 0

    ax_graph_single.clear()
    ax_graph_single.set_xlim(0, max_frames)
    ax_graph_single.set_ylim(0, 100)
    ax_graph_single.set_title("Single-mode Signal Strength")

    ax_graph_multi.clear()
    ax_graph_multi.set_xlim(0, max_frames)
    ax_graph_multi.set_ylim(0, 100)
    ax_graph_multi.set_title("Multi-mode Signal Strength")

    draw_fibers()
    ani.event_source.start()

tk.Button(root, text="Reset", command=reset_simulation).grid(row=1, column=2)
tk.Button(root, text="Explain", command=explain).grid(row=1, column=3)
tk.Button(root, text="Update", command=update_constants).grid(row=1, column=4)

# Sliders for real-time adjustments
att_slider = tk.Scale(root, from_=0.01, to=0.1, resolution=0.005, orient='horizontal', label='Attenuation')
att_slider.set(attenuation_coeff)
att_slider.grid(row=2, column=0)

disp_slider = tk.Scale(root, from_=0.01, to=0.5, resolution=0.01, orient='horizontal', label='Dispersion')
disp_slider.set(dispersion_amount)
disp_slider.grid(row=2, column=1)

length_slider = tk.Scale(root, from_=10, to=40, resolution=1, orient='horizontal', label='Fiber Length')
length_slider.set(fiber_length)
length_slider.grid(row=2, column=2)

root.mainloop()
