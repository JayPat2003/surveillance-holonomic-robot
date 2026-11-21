#!/usr/bin/env python3
"""Springer-style system architecture diagram (IJIT Sec. 2.2).

All connectors are strictly horizontal (180°) or vertical (90°).
Footer is drawn on a separate axes band so it never overlaps the figure.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib.lines import Line2D

INK = "#111111"
MUTED = "#555555"
LINE = "#222222"
BAND = "#f3f3f3"
FILL = "#ffffff"

ROOT = Path(__file__).resolve().parent
OUTS = [
    ROOT / "system_flowchart.png",
    ROOT / "system_flowchart.jpg",
    ROOT / "system_flowchart.pdf",
    ROOT.parent.parent / "Doc" / "Block_diagram.jpg",
    ROOT.parent.parent / "Doc" / "Block_diagram_architecture.pdf",
]


class B:
    __slots__ = ("x", "y", "w", "h")

    def __init__(self, x, y, w, h):
        self.x, self.y, self.w, self.h = float(x), float(y), float(w), float(h)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y

    @property
    def top(self):
        return self.y + self.h


def draw_box(ax, b: B, title, sub=None, lw=1.2, ts=8.2, ss=6.4):
    ax.add_patch(Rectangle(
        (b.x, b.y), b.w, b.h,
        linewidth=lw, edgecolor=INK, facecolor=FILL, zorder=3,
    ))
    if sub:
        ax.text(b.cx, b.cy + 0.13 * b.h, title, ha="center", va="center",
                fontsize=ts, color=INK, fontweight="bold", zorder=4)
        ax.text(b.cx, b.cy - 0.17 * b.h, sub, ha="center", va="center",
                fontsize=ss, color=MUTED, zorder=4)
    elif title:
        ax.text(b.cx, b.cy, title, ha="center", va="center",
                fontsize=ts, color=INK, fontweight="bold", zorder=4)


def band(ax, y, h, name):
    ax.add_patch(Rectangle(
        (0.035, y), 0.93, h,
        facecolor=BAND, edgecolor="#c8c8c8", linewidth=0.7, zorder=0,
    ))
    ax.text(0.048, y + h / 2, name, ha="left", va="center", rotation=90,
            fontsize=6.8, color=MUTED, zorder=1)


def seg(ax, x0, y0, x1, y1, lw=1.2, color=LINE, ls="-"):
    if abs(x0 - x1) > 1e-9 and abs(y0 - y1) > 1e-9:
        raise ValueError(f"non-orthogonal segment: {(x0, y0)} -> {(x1, y1)}")
    ax.plot([x0, x1], [y0, y1], color=color, lw=lw, ls=ls,
            solid_capstyle="butt", zorder=2, clip_on=False)


def head(ax, tip_x, tip_y, direction, size=0.010, color=LINE):
    s = size
    if direction == "down":
        pts = [(tip_x, tip_y), (tip_x - 0.5 * s, tip_y + s), (tip_x + 0.5 * s, tip_y + s)]
    elif direction == "up":
        pts = [(tip_x, tip_y), (tip_x - 0.5 * s, tip_y - s), (tip_x + 0.5 * s, tip_y - s)]
    elif direction == "right":
        pts = [(tip_x, tip_y), (tip_x - s, tip_y - 0.5 * s), (tip_x - s, tip_y + 0.5 * s)]
    else:
        pts = [(tip_x, tip_y), (tip_x + s, tip_y - 0.5 * s), (tip_x + s, tip_y + 0.5 * s)]
    ax.add_patch(Polygon(pts, closed=True, facecolor=color, edgecolor=color, lw=0, zorder=2))


def v_arrow(ax, x, y0, y1, lw=1.2, color=LINE, ls="-"):
    tip = 0.010
    if y1 < y0:
        seg(ax, x, y0, x, y1 + tip, lw=lw, color=color, ls=ls)
        head(ax, x, y1, "down", size=tip, color=color)
    else:
        seg(ax, x, y0, x, y1 - tip, lw=lw, color=color, ls=ls)
        head(ax, x, y1, "up", size=tip, color=color)


def h_arrow(ax, y, x0, x1, lw=1.2, color=LINE, ls="-"):
    tip = 0.010
    if x1 > x0:
        seg(ax, x0, y, x1 - tip, y, lw=lw, color=color, ls=ls)
        head(ax, x1, y, "right", size=tip, color=color)
    else:
        seg(ax, x0, y, x1 + tip, y, lw=lw, color=color, ls=ls)
        head(ax, x1, y, "left", size=tip, color=color)


def main():
    os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-surveillance")
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif", "Times", "serif"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(7.8, 10.4), dpi=300, facecolor="white")

    # Diagram region
    ax = fig.add_axes([0.03, 0.13, 0.94, 0.84])
    ax.set_xlim(0, 1)
    ax.set_ylim(0.13, 1.0)
    ax.axis("off")

    ax.text(0.50, 0.995, "System architecture of the holonomic surveillance robot",
            ha="center", va="top", fontsize=11, color=INK, fontweight="bold")
    ax.text(0.50, 0.970,
            "Dual-controller framework: Jetson Nano (high-level) and Arduino Mega (low-level)",
            ha="center", va="top", fontsize=7.5, color=MUTED)

    # Shared column centers — every vertical wire uses one of these
    C1, C2, C3 = 0.22, 0.50, 0.78
    BW = 0.236
    IW = 0.200

    band(ax, 0.155, 0.095, "Actuation")
    band(ax, 0.275, 0.150, "Low-level control")
    band(ax, 0.455, 0.220, "High-level computation")
    band(ax, 0.705, 0.145, "Sensing")

    # Sensing
    lidar = B(C1 - BW / 2, 0.750, BW, 0.075)
    cam = B(C2 - BW / 2, 0.750, BW, 0.075)
    imu = B(C3 - BW / 2, 0.750, BW, 0.075)
    draw_box(ax, lidar, "RPLiDAR A1M8", "360° · USB · /scan")
    draw_box(ax, cam, "USB camera", "visual monitoring")
    draw_box(ax, imu, "MPU6050 IMU", "I2C · orientation")

    # Jetson container wide enough for C1–C2 content
    jet = B(0.08, 0.475, 0.56, 0.185)
    draw_box(ax, jet, "", lw=1.45)
    ax.text(jet.cx, 0.635, "NVIDIA Jetson Nano  +  ROS Melodic",
            ha="center", va="center", fontsize=8.5, color=INK, fontweight="bold", zorder=4)

    IH = 0.048
    slam = B(C1 - IW / 2, 0.565, IW, IH)
    plan = B(C2 - IW / 2, 0.565, IW, IH)
    fuse = B(C1 - IW / 2, 0.495, IW, IH)
    cmd = B(C2 - IW / 2, 0.495, IW, IH)
    draw_box(ax, slam, "SLAM / mapping", "gmapping", lw=0.95, ts=7.4, ss=6.0)
    draw_box(ax, plan, "Localization & planning", "AMCL · goals", lw=0.95, ts=7.4, ss=6.0)
    draw_box(ax, fuse, "Sensor fusion", "LiDAR + IMU cues", lw=0.95, ts=7.4, ss=6.0)
    draw_box(ax, cmd, "Motion command", "/cmd_vel (Vx, ω)", lw=0.95, ts=7.4, ss=6.0)

    # Arduino
    ard = B(0.08, 0.295, 0.56, 0.110)
    draw_box(ax, ard, "", lw=1.45)
    ax.text(ard.cx, 0.380, "Arduino Mega 2560  (real-time motor control)",
            ha="center", va="center", fontsize=8.3, color=INK, fontweight="bold", zorder=4)

    ros_n = B(C1 - IW / 2, 0.308, IW, IH)
    kin = B(C2 - IW / 2, 0.308, IW, IH)
    draw_box(ax, ros_n, "rosserial node", "Twist → wheel rates", lw=0.95, ts=7.4, ss=6.0)
    draw_box(ax, kin, "Mecanum kinematics", "ω1…ω4  step/dir", lw=0.95, ts=7.4, ss=6.0)

    # Align orientation box vertical center with kinematics for a true horizontal link
    orient_h = 0.065
    orient = B(C3 - BW / 2, kin.cy - orient_h / 2, BW, orient_h)
    draw_box(ax, orient, "Orientation feedback", "stability / motion cues", lw=1.1, ts=7.4, ss=6.0)

    # Actuation on same columns
    AH, AY = 0.055, 0.170
    drv = B(C1 - BW / 2, AY, BW, AH)
    mot = B(C2 - BW / 2, AY, BW, AH)
    whl = B(C3 - BW / 2, AY, BW, AH)
    draw_box(ax, drv, "TB6600 drivers (×4)", "step / direction", ts=7.6, ss=6.1)
    draw_box(ax, mot, "Nema 23 steppers (×4)", "AccelStepper", ts=7.6, ss=6.1)
    draw_box(ax, whl, "Mecanum wheels", "Vx, Vy, ωz motion", ts=7.6, ss=6.1)

    # Sanity: column alignment
    assert abs(lidar.cx - C1) < 1e-9 and abs(drv.cx - C1) < 1e-9 and abs(ros_n.cx - C1) < 1e-9
    assert abs(cam.cx - C2) < 1e-9 and abs(mot.cx - C2) < 1e-9 and abs(kin.cx - C2) < 1e-9
    assert abs(imu.cx - C3) < 1e-9 and abs(whl.cx - C3) < 1e-9 and abs(orient.cx - C3) < 1e-9
    assert abs(drv.cy - mot.cy) < 1e-9 and abs(mot.cy - whl.cy) < 1e-9

    # ---- connectors ----
    v_arrow(ax, C1, lidar.bottom, jet.top)
    ax.text(C1 - 0.025, (lidar.bottom + jet.top) / 2, "USB", ha="right", va="center",
            fontsize=6.2, color=INK, style="italic",
            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))

    v_arrow(ax, C2, cam.bottom, jet.top)
    ax.text(C2 + 0.025, (cam.bottom + jet.top) / 2, "USB", ha="left", va="center",
            fontsize=6.2, color=INK, style="italic",
            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))

    v_arrow(ax, C3, imu.bottom, orient.top)
    ax.text(C3 + 0.025, 0.55, "I2C", ha="left", va="center",
            fontsize=6.2, color=INK, style="italic",
            bbox=dict(boxstyle="square,pad=0.05", fc="white", ec="none"))

    v_arrow(ax, C1, slam.bottom, fuse.top, color=MUTED, lw=1.0)
    v_arrow(ax, C2, plan.bottom, cmd.top, color=MUTED, lw=1.0)
    h_arrow(ax, fuse.cy, fuse.right, cmd.left, color=MUTED, lw=1.0)

    v_arrow(ax, jet.cx, jet.bottom, ard.top)
    ax.text(0.58, (jet.bottom + ard.top) / 2, "USB · rosserial · /cmd_vel",
            ha="center", va="center", fontsize=6.1, color=INK, style="italic",
            bbox=dict(boxstyle="square,pad=0.07", fc="white", ec="none"))

    h_arrow(ax, orient.cy, orient.left, kin.right)

    v_arrow(ax, C1, ros_n.bottom, drv.top)
    v_arrow(ax, C2, kin.bottom, mot.top)

    h_arrow(ax, drv.cy, drv.right, mot.left)
    h_arrow(ax, mot.cy, mot.right, whl.left)

    # Obstacle feedback: pure orthogonal rectangle path
    x_fb = 0.635
    y_top = plan.top + 0.016
    seg(ax, cmd.right, cmd.cy, x_fb, cmd.cy, ls="--")
    seg(ax, x_fb, cmd.cy, x_fb, y_top, ls="--")
    seg(ax, x_fb, y_top, plan.cx, y_top, ls="--")
    v_arrow(ax, plan.cx, y_top, plan.top, ls="--")
    ax.text(0.650, (cmd.cy + y_top) / 2, "obstacle\nfeedback",
            ha="left", va="center", fontsize=6.0, color=INK, style="italic")

    # Footer axes — isolated, generous spacing
    fax = fig.add_axes([0.03, 0.02, 0.94, 0.095])
    fax.set_xlim(0, 1)
    fax.set_ylim(0, 1)
    fax.axis("off")
    fax.plot([0.05, 0.95], [0.95, 0.95], color="#bdbdbd", lw=0.8)

    fax.text(
        0.50, 0.68,
        "Interfaces (paper Sec. 2.2): LiDAR/camera → Jetson (USB); "
        "MPU6050 → Arduino (I2C); Jetson ↔ Arduino (USB).",
        ha="center", va="center", fontsize=6.6, color=MUTED,
    )

    legend = [
        Line2D([0], [0], color=LINE, lw=1.25, label="Data / command path"),
        Line2D([0], [0], color=INK, lw=1.25, linestyle=(0, (3, 2)),
               label="Closed-loop obstacle adjustment"),
    ]
    fax.legend(
        handles=legend, loc="upper center", bbox_to_anchor=(0.5, 0.40),
        ncol=2, frameon=False, fontsize=7.2, handlelength=2.6, columnspacing=2.2,
        borderaxespad=0.0,
    )

    for path in OUTS:
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix.lower() == ".pdf":
            fig.savefig(path, facecolor="white")
        elif path.suffix.lower() in {".jpg", ".jpeg"}:
            fig.savefig(path, dpi=300, facecolor="white", pil_kwargs={"quality": 95})
        else:
            fig.savefig(path, dpi=300, facecolor="white")

    plt.close(fig)
    print("Wrote:")
    for p in OUTS:
        print(f"  {p} ({p.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
