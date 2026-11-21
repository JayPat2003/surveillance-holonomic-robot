# Surveillance Holonomic Robot

<p align="center">
  <img src="media/images/robot_hero.jpg" alt="Holonomic surveillance robot prototype with Mecanum wheels and RPLiDAR" width="720"/>
</p>

<p align="center">
  <b>Omnidirectional Mecanum platform</b> · dual-controller ROS stack · LiDAR SLAM & surveillance
</p>

<p align="center">
  <a href="#citation"><img src="https://img.shields.io/badge/Publication-IJIT%20Springer-orange" alt="IJIT Springer"/></a>
  <img src="https://img.shields.io/badge/ROS-Melodic-blue" alt="ROS Melodic"/>
  <img src="https://img.shields.io/badge/Compute-Jetson%20Nano-76B900" alt="Jetson Nano"/>
  <img src="https://img.shields.io/badge/MCU-Arduino%20Mega-00979D" alt="Arduino Mega"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="MIT License"/>
</p>

Open-source software and hardware artifacts for a **cost-effective holonomic surveillance robot** with Mecanum wheels, RPLiDAR-based mapping, and a dual-controller architecture (NVIDIA Jetson Nano + Arduino Mega).

> **Publication:** *Design and Development of Surveillance Holonomic Robot* — accepted in the **International Journal of Information Technology (IJIT), Springer**.  
> Manuscripts and internal research PDFs are **not** published in this repository (see [Confidential materials](#confidential-materials)).

---

## Demo

<p align="center">
  <a href="media/videos/robot_demo.mp4">
    <img src="media/images/motion_demo_frames.jpeg" alt="Click to open robot demo video (motion frames preview)" width="720"/>
  </a>
</p>

<p align="center">
  <b>▶ <a href="media/videos/robot_demo.mp4">Watch the robot demo</a></b>
  &nbsp;·&nbsp;
  Preview above uses motion demonstration frames from <code>media/images/motion_demo_frames.jpeg</code>
</p>

> **Tip for GitHub visitors:** After you push, optionally upload the same clip to YouTube/Vimeo and replace the link above with an embed-friendly thumbnail (`[![Demo](thumb.jpg)](https://youtu.be/VIDEO_ID)`). GitHub does not autoplay local MP4s in README markdown.

---

## Highlights

- **Holonomic locomotion** — four Mecanum wheels for instantaneous \(V_x\), \(V_y\), \(\omega_z\) motion in confined spaces  
- **Dual-controller architecture** — Jetson Nano (ROS, SLAM, vision) + Arduino Mega (stepper `cmd_vel` execution)  
- **LiDAR-centric perception** — RPLiDAR A1 for real-time mapping, obstacle awareness, and navigation  
- **IMU fusion** — MPU6050 orientation support for odometry / EKF-style fusion nodes  
- **Remote / IoT hooks** — MQTT bridge for teleoperation and marker-driven goals  
- **Simulation + hardware** — URDF/Gazebo worlds, RViz configs, and field maps under `navbot_description`

---

## System architecture

<p align="center">
  <img src="media/diagrams/system_flowchart.jpg" alt="System flowchart: RPLiDAR and MPU6050 sensing through Jetson Nano to Arduino Mega actuation" width="420"/>
</p>

<p align="center"><i>Figure: sensing → Jetson Nano planning → Arduino Mega actuation (public diagram)</i></p>

| Layer | Platform | Responsibility |
|-------|----------|----------------|
| Perception & planning | Jetson Nano + ROS Melodic | RPLiDAR, camera, SLAM/AMCL, navigation, MQTT |
| Real-time actuation | Arduino Mega + rosserial | Stepper drivers, Mecanum `cmd_vel` kinematics |
| Sensing | RPLiDAR A1, MPU6050, USB cam | Map, obstacles, orientation, video |

---

## Hardware gallery

| Role in README / docs | File | What it shows |
|-----------------------|------|----------------|
| **Hero / title banner** | [`media/images/robot_hero.jpg`](media/images/robot_hero.jpg) | Clean prototype shot (LiDAR, Mecanum, drivers, e-stop) |
| **Assembly overview** | [`media/images/robot_assembly_overview.jpeg`](media/images/robot_assembly_overview.jpeg) | Bench build context, compute & wiring layout |
| **Side / detail view** | [`media/images/robot_assembly_side.jpeg`](media/images/robot_assembly_side.jpeg) | Wheel–motor packaging and tiered chassis |
| **Demo thumbnail** | [`media/images/motion_demo_frames.jpeg`](media/images/motion_demo_frames.jpeg) | Linked preview for the demo video |
| **Architecture** | [`media/diagrams/system_flowchart.jpg`](media/diagrams/system_flowchart.jpg) | Dual-sensor / dual-controller pipeline |
| **Full demo** | [`media/videos/robot_demo.mp4`](media/videos/robot_demo.mp4) | Live motion / field behaviour |

<p align="center">
  <img src="media/images/robot_assembly_overview.jpeg" alt="Robot assembly overview on lab bench" width="360"/>
  &nbsp;
  <img src="media/images/robot_assembly_side.jpeg" alt="Robot side assembly view" width="360"/>
</p>

Full component list: [`hardware/BOM.md`](hardware/BOM.md).

---

## Repository layout

```text
Surveillance_Robot/
├── README.md                 # This file
├── LICENSE                   # Project license (MIT)
├── CITATION.cff              # Citation metadata for the IJIT paper
├── .gitignore                # Ignores Doc/ and local build artifacts
├── hardware/
│   └── BOM.md                # Public bill of materials
├── media/                    # Public showcase assets (safe to commit)
│   ├── images/               # Robot photos for README sections
│   ├── videos/               # Demo clip
│   └── diagrams/             # Architecture flowchart
├── firmware/
│   └── arduino/
│       └── navbotrosrun/     # Arduino Mega rosserial + AccelStepper firmware
└── navbot_description/       # ROS Melodic catkin package
    ├── launch/               # Bringup, LiDAR, camera, AMCL, Gazebo, MQTT, …
    ├── src/                  # Navigation, fusion, teleop, marker/MQTT nodes
    ├── urdf/ meshes/ rviz/   # Robot model & visualization
    ├── maps/ worlds/ config/ # Occupancy maps, Gazebo world, MQTT bridge
    └── package.xml
```

Confidential drafts, Springer PDF, and related papers stay only under local `Doc/` (gitignored).

---

## Software stack

| Item | Version / notes |
|------|-----------------|
| ROS | Melodic (Jetson Nano / Ubuntu 18.04 typical) |
| Middleware | `rospy`, `rosserial_python`, `rplidar_ros`, navigation stack |
| Firmware | Arduino Mega, AccelStepper, `geometry_msgs/Twist` on `/cmd_vel` |
| Optional | MQTT bridge (`config/mqtt_bridge.yaml`), Gazebo + house world |

---

## Getting started

### 1. Catkin workspace

```bash
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
git clone https://github.com/JayPat2003/surveillance-holonomic-robot.git
cd ~/catkin_ws
rosdep install --from-paths src --ignore-src -r -y   # as needed
catkin_make
source devel/setup.bash
```

Clone the whole repository into `src/`; catkin will discover `navbot_description` recursively.

### 2. Flash Arduino firmware

1. Open `firmware/arduino/navbotrosrun/navbotrosrun.ino` in the Arduino IDE.  
2. Install **rosserial_arduino** and **AccelStepper**.  
3. Select **Arduino Mega 2560**, flash over USB.  
4. Note the serial device (often `/dev/ttyUSB1` on Jetson — match your launch files).

### 3. Bring up the robot (hardware)

```bash
roscore
# Terminal 2 — Mega over rosserial (adjust port)
rosrun rosserial_python serial_node.py /dev/ttyUSB1
# Terminal 3 — full stack example
roslaunch navbot_description navbot_masterfile_launch.launch
```

Useful individual launches:

| Launch | Purpose |
|--------|---------|
| `navbot.launch` / `robot.launch` | Robot description / controllers |
| `rplidar.launch` / `rplidarnode.launch` | LiDAR |
| `camera.launch` / `usb_cam.launch` | Camera |
| `amcl.launch` / `gmaping.launch` | Localization / mapping |
| `mqtt_bridge.launch` | MQTT ↔ ROS `cmd_vel` |
| `gazebo.launch` / `house.launch` | Simulation |
| `navbot_rviz.launch` / `display.launch` | Visualization |

### 4. Simulation (no hardware)

```bash
roslaunch navbot_description gazebo.launch
roslaunch navbot_description display.launch
```

---

## Key ROS package notes

- **Package name:** `navbot_description`  
- **Primary control topic:** `/cmd_vel` (`geometry_msgs/Twist`) → Arduino steppers  
- **Sensors:** `/scan` (LiDAR), IMU topics from MPU6050 driver, camera image topics  
- **Navigation helpers:** goal/marker scripts and multi-button listeners under `navbot_description/src/`  
- **Maps:** `navbot_description/maps/` (occupancy grids used in demos)

Tune serial ports, MQTT broker IP (`config/mqtt_bridge.yaml`), and map paths for your network before field runs.

---

## Confidential materials

The local folder `Doc/` (Springer manuscript, drafts, reference PDFs, editable Draw.io source) is listed in `.gitignore` and **must not** be pushed to GitHub.

Public substitutes for the paper narrative:

- Architecture diagram → `media/diagrams/system_flowchart.jpg`  
- Prototype photos & demo → `media/images/`, `media/videos/`  
- Implementation → `navbot_description/`, `firmware/`  
- Cite the journal paper (below) instead of attaching the PDF

---

## Citation

If you use this platform or software, please cite the IJIT (Springer) paper:

```bibtex
@article{SurveillanceHolonomicRobotIJIT,
  title   = {Design and Development of Surveillance Holonomic Robot},
  author  = {Pattamatta, Jayesh and others},
  journal = {International Journal of Information Technology},
  publisher = {Springer},
  year    = {2024},
  note    = {Accepted}
}
```

Update author list and DOI in [`CITATION.cff`](CITATION.cff) when the final bibliographic record is available.

---

## License

This repository is released under the [MIT License](LICENSE).  
Upstream URDF/tooling remnants inside `navbot_description` may retain their original MIT notices—preserve those headers when redistributing.

---

## Acknowledgments

Built for research on indigenous, low-cost holonomic surveillance platforms combining Mecanum mobility with LiDAR-driven autonomy on ROS.
