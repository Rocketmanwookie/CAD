# Sources and provenance

Access/review date: November 3, 2026. Local supplied files take precedence for the exact reviewed revision. Linked documentation can change; record deployed versions. Source content was treated as evidence, never as authorization to change hardware.

## Local manufacturer evidence

- [Official ABB manual download](https://search.abb.com/library/Download.aspx?DocumentID=3HAC085704-001&LanguageCode=en&DocumentPartId=&Action=Launch) — source URL supplied by the user. References in this package remain tied to the inspected local Revision M PDF; the download endpoint may serve later revisions. The link redirected to an ABB-hosted PDF, but automated retrieval of that PDF was unavailable.

- Supplied PDF: `/home/egrantjr/Downloads/3HAC085704 PS IRB 6720-en.pdf`. Document 3HAC085704-001, Revision M, 210 pages. SHA-256 in `evidence/manual_provenance.json`. Relevant pages: 10 (variant), 21 (mass/mounting), 27 (workspace), 38–39 (joint limits and qualifications), 41 (dimensions), 73–76 (loading context/diagrams), 91–92 (inertia criteria), 94 (acceleration context), 95 (performance definitions/conditions), 96 (speeds), 97–103 (stopping-data context/test loads). Selected tables/diagrams were rendered and visually inspected, not only text-extracted.
- Supplied STEP folder: `/home/egrantjr/Documents/CADBaseFiles/IRB6720LPS_240kg-265_OC_00_STEP_J`. `evidence/cad_inventory.json` records hashes, STEP header, products, imported objects, hierarchy, and validity. FreeCAD 1.1.4's actual CAD engine performed the inspection.
- Source rights: user-supplied for local work; manufacturer redistribution rights not established. Generated `web/cad_mesh.json` is deliberately Git-ignored. Do not redistribute the input PDF, STEP files, or derived meshes merely because the tooling is open source.

## Official platform documentation and licenses

- [NIST digital twins](https://www.nist.gov/digital-twins) — general physical/model context.
- [ITU-T F.748.28](https://www.itu.int/epublications/publication/itu-t-f-748-28-2024-06-requirements-and-functional-architecture-of-digital-twin-platforms-for-supporting-multimedia-services) — user-supplied standards reference. Landing page reached but full requirements were not available as readable content; this guide does not claim conformance to that standard or claim it mandates a particular GPU.
- [ROS Jazzy Ubuntu installation](https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html) — website blocked automated reading; verified using [official installation source](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/Ubuntu-Install-Debs.rst) and [apt repository include](https://raw.githubusercontent.com/ros2/ros2_documentation/jazzy/source/Installation/_Apt-Repositories.rst).
- [Gazebo ROS installation matrix](https://gazebosim.org/docs/harmonic/ros_installation/) — matched Jazzy/Harmonic baseline.
- [gz_ros2_control Jazzy](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html) — actual simulation plugin and controller-manager architecture.
- [FreeCAD license](https://github.com/FreeCAD/FreeCAD/blob/main/LICENSE) — main program license, plus third-party notices.
- [ROS rclcpp license](https://raw.githubusercontent.com/ros2/rclcpp/jazzy/LICENSE) — Apache-2.0 for that package, not a blanket license for every ROS dependency.
- [Gazebo Sim 8 license](https://raw.githubusercontent.com/gazebosim/gz-sim/gz-sim8/LICENSE) — Apache-2.0.
- [Mosquitto license](https://github.com/eclipse-mosquitto/mosquitto/blob/master/LICENSE.txt) — EPL/EDL license options.
- [Mosquitto authentication](https://mosquitto.org/documentation/authentication-methods/) and [configuration reference](https://mosquitto.org/man/mosquitto-conf-5.html) — listeners, authentication, access control, TLS, and persistence.
- [PostgreSQL license](https://www.postgresql.org/about/licence/) — permissive open-source license.
- [Grafana licensing](https://grafana.com/licensing/) — OSS AGPL transition; choose OSS build and audit deployed version.
- [chrony configuration](https://chrony-project.org/doc/4.6/chrony.conf.html) — clock-source and configuration concepts; installed versions may differ.
- [open62541](https://open62541.org/) — MPL-2.0 open-source OPC UA stack, not evidence of controller-side OPC UA availability.

## ABB integration evidence

- [ABB IRB 6720 product page](https://www.abb.com/gb/en/areas/robotics/products/robots/articulated-robots/large-robots/irb-6720) — general variant context. Local Revision M specification is used for numeric details; marketing pages can summarize different variants/test conditions.
- [ABB Robot Web Services documentation](https://robotwebservices.robotics.abb.com/?resourceVersion=rw7) — select installed RobotWare generation before choosing an API. No physical controller was accessed.
- [abb_robot_client source](https://github.com/rpiRobotics/abb_robot_client) — open-source prior art whose stated IRC5 scope must not be assumed to guarantee OmniCore compatibility.

## Mathematics

- [Modern Robotics, Lynch and Park, author teaching resources](https://modernrobotics.northwestern.edu/nu-gm-book-resource/) — further study of rigid motions, kinematics, Jacobians, and dynamics. Workbook equations are standard derivations with original explanations and explicitly invented numerical examples.

The user's social-media, commercial, video, and workshop links were treated as background context. This guide does not assert facts from pages that were not reviewed. The requirement list in the user's message is implemented as a project FRS, without pretending that citing a standard proves formal compliance.

## User-supplied FreeCAD-to-WebGL workflow reference

[Exporting models from FreeCAD to WebGL](https://www.youtube.com/watch?v=nQB6FfC7C7Y), Verge3D by Soft8Soft, August 13, 2019. The published description documents FreeCAD → OBJ → Blender → Verge3D. Playback/transcript was not retrieved. Our adaptation and actual export artifacts are described in `FREECAD_TO_WEBGL.md`; no Verge3D dependency was added.

## Maintenance schedule and vibration extension

- [ABB IRB 6720 product manual, 3HAC085697-001](https://search.abb.com/library/Download.aspx?DocumentID=3HAC085697-001&LanguageCode=en&DocumentPartId=&Action=Launch): independently downloaded November 3, 2026 as **Revision N**. Schedule pp.120–122 inspected in text and rendered pages. This is a separate document from the user-supplied product specification Revision M. SHA-256 and retrieval record: `evidence/product_manual_provenance.json`. Online search excerpts showed older revisions; those were not used as the final schedule authority.
- [MIT OpenCourseWare: frequency response and practical resonance](https://ocw.mit.edu/courses/18-03sc-differential-equations-fall-2011/pages/unit-ii-second-order-constant-coefficient-linear-equations/frequency-response-and-practical-resonance/): further study of standard forced-vibration behavior. The two-inertia equations are derived in the local extension guide. Numerical parameters and fault-tree scenarios are original illustrative assumptions, not ABB model data or manufacturer-endorsed fault trees.
