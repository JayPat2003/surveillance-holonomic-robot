# Bill of Materials

Hardware used in the holonomic surveillance robot prototype.

| Component | Qty | Role |
|-----------|-----|------|
| NVIDIA Jetson Nano 2GB Developer Kit | 1 | High-level compute (ROS, SLAM, vision) |
| Arduino Mega 2560 | 1 | Low-level motor control via rosserial |
| RPLiDAR A1M8 (360°, 12 m) | 1 | Mapping, localization, obstacle sensing |
| GY-521 MPU6050 | 1 | IMU orientation / EKF fusion |
| USB camera | 1 | Visual monitoring |
| Nema 23 bipolar stepper motors | 4 | Wheel actuation |
| TB6600 / eAUTOMATION stepper drivers (≈3 A) | 4 | Step/dir drive for steppers |
| Mecanum wheels (152 mm aluminum) | 4 | Omnidirectional locomotion |
| XL4015 DC buck converter | 1 | Regulated power rails |
| LiPo pack (e.g. 22.2 V 6S 13000 mAh) | 1 | Main power |
| Wooden chassis + LiDAR mount | 1 | Mechanical structure |
| E-stop (Bulgin-style terminal / button) | 1 | Safety cutoff |

See the repository README for architecture and software setup.
