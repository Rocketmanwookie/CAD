# IntegraCAD Open workbench workflow

This workflow records the project owner's revised sequence of 2026-10-06 and
refines the supplied [product scope](INTEGRACAD_OPEN_SCOPE.md). It governs the
workflow redesign; implementation status remains in
[Project status](../PROJECT_STATUS.md).

The streamlined presentation groups this sequence into six stages:
**Project & Plant → Controls Circuit → Safety Circuit → Parts & CAD →
Cabinet & Routing → Generate Package**. The
[workflow milestones](../WORKFLOW_MILESTONES.md) track their implementation.
Parts availability can be checked during circuit configuration; bulk CAD
collection uses the combined equipment list after both circuits are defined.
Drawings and BOM may be previewed during construction; the final package and
wire schedule follow routing.

## Engineer's sequence

| Stage | Engineer's action | Result used by the next stage |
|---|---|---|
| 1. Plant questionnaire | Describe the plant, supply, environment, enclosure, platform preferences, networks, and referenced requirements | Saved project design basis and unresolved questions |
| 2. I/O count | Enter required DI, DO, AI, and AO counts | Demand by type, with calculated 20% additional capacity |
| 3. PLC configurator | Review/select the CPU and compatible modules against the enlarged demand | Selected hardware configuration and available channels |
| 4. Define I/O | Label and describe actual points, or import their definitions; identify devices, electrical signal characteristics, and endpoints | Detailed I/O list mapped to the configured channels |
| 5. Complete controls circuit | Define the control-circuit components, terminals, and logical connections | Controls equipment and endpoint requirements |
| 6. Complete safety circuit | Follow the safety requirements/count/configure/define sequence below and define its connections | Safety equipment and endpoint requirements |
| 7. Parts & CAD | Resolve the combined parts list to personal or CADbase library assets; collect models and connection information for both circuits | Component set ready for the shared cabinet |
| 8. Construct shared cabinet | Size/select the enclosure and place the combined controls and safety equipment | Shared cabinet assembly realizing both circuits |
| 9. BOM and drawings | Produce the combined BOM, 2D and 3D representations, and cabinet drawing sheets from the assembly | Coordinated bill of materials and drawing package |
| 10. Wire schedule | Complete wire routes and attributes, then generate the combined schedule | Wire records tied to both circuits' devices, terminals, and paths |

BOM and drawing production share the panel model and may be revised together.
The wire schedule is the final output in this sequence; connection information
must already exist during panel construction so drawings and routing can use it.
Cabinet construction depends on both circuit definitions being complete,
including selected equipment, CAD references, and endpoints. Preliminary
enclosure preferences may be captured in the questionnaire; final cabinet
selection and layout must account for equipment from both circuits.

## Capacity and I/O definition

For each I/O type, required capacity is `ceil(required_count * 1.20)`.
Keep actual demand, required spare capacity, and installed capacity separate.
Unused installed channels are spare channels rather than invented field devices.
Module selection must satisfy each type and the selected platform's compatibility
and expansion limits. Electrical signal characteristics identified in stage 4
may require a revised module selection even when the numeric count fits.

If imported or edited I/O exceeds the demand used to select hardware, return to
the configurator with the revised counts. Preserve defined tags, device
identities, and existing connections during review; identify any assignments
that need resolution before regenerating dependent outputs.

## Workbench presentation

Present the stages as one workflow with a current-stage indicator and direct
access to earlier stages. Save progress in the project so work can resume after
reopening FreeCAD. Show unresolved inputs at the stage where they are needed.

The stage navigation follows the six-stage sequence above. Supporting actions
include **Plant Questionnaire**, **I/O Count**, **PLC Configurator**,
**Define I/O**, **Controls Circuit**, **Safety Circuit**, **Gather CAD**,
**Construct Shared Cabinet**, and **Generate Package**, which includes
**BOM & Drawings** and **Wire Schedule**. **Import I/O** is an alternative entry
within Define I/O. The previously proposed **POC CAD Files** action belongs in
Gather CAD. Existing allocation, path, validation, and export commands support
these stages; their current availability does not establish stage completion.

The plant questionnaire captures design-basis information once. Detailed signal
labels belong in Define I/O, after hardware sizing, rather than being required
to submit the initial questionnaire.

## Integration and document ownership

CADbase owns reusable part assets; the personal-library import links assets to
selected parts. Components/assembly tools realize the panel, Fasteners handles
fasteners, Cables handles physical routing, the BOM workbench produces the BOM,
and drawing tools/TechDraw produce sheets and title blocks. IntegraCAD Open
coordinates shared identities, endpoint data, updates, and schedule inputs.

The [controls document package](../../ControlForgeCAD/templates/controls-document-package/README.md)
provides source templates and reference drawings for future outputs. Its I/O,
BOM, and cable records require explicit mappings from project data; merely
copying a template does not produce a completed project document. Plant inputs
support URS/FDS and design-basis references; defined I/O supplies the I/O list;
the assembly supplies BOM and drawings; the connection/routing model supplies
wire and cable schedules. PLC/HMI programming and safety engineering retain
the ownership boundaries stated in the product scope.

## Safety-circuit workflow before cabinet construction

After defining the controls circuit, provide a similar sequence for defining
the safety circuit. Both feed the subsequent shared cabinet construction:

1. Capture supplied safety requirements, risk-assessment references, circuit
   boundaries, and the required PL/SIL/category information.
2. Count and classify safety inputs and outputs, including channel requirements
   and any specified spare allowance.
3. Select the safety relay/controller and compatible modules from those
   requirements.
4. Define or import the safety points, device tags, channels, and terminal
   connections.
5. Complete the safety-circuit components, terminals, and logical connection model.
6. Hand both circuits' equipment to the combined Parts & CAD stage, then
   to shared cabinet construction together
   with the controls circuit. Produce the combined BOM, drawings, and wire
   schedule through the common downstream stages.

Reuse component, terminal, and wire identities from the controls circuit where they
refer to the same physical occurrences. Identify safety-related records so
their drawings and schedules can be reviewed separately while contributing
to the combined package. A safety-circuit change marks dependent panel
drawings, BOM, and wiring outputs for regeneration.

This sequence implements the scope's safety-relay circuit modeling boundary.
Required PL/SIL/category and circuit requirements are supplied design inputs;
modeling does not calculate or approve achieved safety performance. The main
I/O sizing rule of 20% does not automatically set safety channel redundancy or
architecture; record the safety requirements and spare allowance explicitly.

## Delivery sequence

1. Separate the plant questionnaire from I/O sizing and PLC selection, preserving
   existing projects and the current allocation/path regression coverage.
2. Provide the ordered count/configure/define flow, including imported I/O,
   spare-channel handling, and review after demand or signal-type changes.
3. Complete controls and safety circuit definition in the same project.
4. Add combined CAD collection and library matching against selected parts and endpoints.
5. Construct the shared cabinet from both circuits and connect it to BOM and
   drawing adapters.
6. Generate the final combined wire schedule from both circuits' defined and
   routed paths.

The open FreeCAD save/reopen/recompute acceptance run remains a persistence
check within this delivery sequence. Stage acceptance must include actual
outputs and desktop evidence for the integrated workflow.
