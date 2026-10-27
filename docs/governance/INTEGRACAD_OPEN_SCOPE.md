PLAN

::Document Adherence::
URS: User Requirement Specification
FDS: Functional Design Specification
CN: Control Narrative
I/O: I/O List
BOM: Bill of Materials
CS: Cable Schedule
C&E: Cause and Effect Matrix
RATS: Range, Alarm and Trip Schedule
RA: Machinery Risk Assessment and Safety Requirements
SDS: Software Design Specification
ALM: Alarm List and Rationalisation Record
FAT: Factory Acceptance Test Protocol
COMM: Commissioning Checklist
SAT: Site Acceptance Test Protocol
HO: Handover and As-Built Pack
O&M: Operation and Maintenance Manual
MOC: Change Control Record

::Design basis::
Answered once here, and read by every document this project produces.

-Goal and scope


Project goal
The FreeCAD Workbench IntegraCAD Open will be able to assist engineers in creating parametrically defined drawings with true circuit paths on 2d and 3d representations on the panels and systems in design.
Process or machine
The workbench helps the engineer gather the needed information and CAD files, then aids in creating 2D and 3D cad drawings of control systems with true to life circuits that land on the devices where they land on the actual project.  The workbench aids the engineer in selecting the appropriate wire (size, type, sheath color) and creates a wire schedule, compiles the I/O and creates ladder rungs for all of the projects sensors and controlled devices.  Additionally,  the workbench assists the engineer create a complete set of control drawings including schematics, diagrams, bill of materials, wire schedule, safety circuit, ect..
In scope
The BOM will be handeled by the BOM workbench, the wire runs will be done in the cables workbench, the drawing pages and title block will be dont in al drawing workbench.   The system will be put together to make a complete panel in the components workbench 2D and 3D (and ported to the tech drawing workbench).  A parts library will be updated and maintained in the CADBase Library workbench.  Any fasteners modeled in these projects will be done so in the fasteners workbench.  Future plugins may include, thermal consideration package, em considerations package.
By others
Stated explicitly, because this is what arguments at handover are about.

-Control platform
The hardware the documents describe and the BOM has to match.

Controller
Siemens S7-1200 is assumed.  Support for importing a personal library must be implemented.
HMI and SCADA
HMI support must be implemented.  HMI Programming will remain another package (Just like PLC programming).
I/O count
DI, DO, AI, AO will be asked by a form.  20% added for future consideration.  PLC model selected based on this count.
Networks and protocols
Networks and protocols will be selected by the user.
Drives and instruments
Comprehensive I\O list must be maintained to include any devices that carry large loads.  This is done so power delivery can be mapped and fault current calculated.

-Electrical and environment
What the panel is fed from and what it has to survive.

Electrical supply
Drop down selects commonvoltage/phase pairs.
Panels and protection
Enclosure rating selected by user.  Standard panel size will be added.  Larger panels must be added manually to accommodate large amounts of equipment.
Environment and area classification
Environmental factors selected by user.

-Safety
The safety functions, what they have to achieve, and where that came from.

Safety functions
Safety is not in the scope of this workbench.  It will be able to model the safety relay circuit though.
Required PL or SIL
PLD, Cat 3 ot SIL selected by user.  For documentation purposes only.  Additional CAD is up to the user.
Risk assessment reference
The document the safety requirements derive from, and who owns it.

-Opertaion and performance
How it is run, what it has to hit, and what it has to talk to.

Operating modes
Programming package. Not used.
Performance targets
Programming package. Not used.
Interfaces and handshakes
Programming package. Not used.

-Compliance and security
The rules the job is run against, including the OT network.

Standards
Selectable by user: IEC 60204-4 and 61131-3, ISO 13849-1, ISA 18.2, and ENG
OT security
Security Package. Not considered.

-Acceptance and dates
What finished means, and when it is due.

Acceptance criteria
documentation package. Not considered.
Key dates
{project management package. Not included.