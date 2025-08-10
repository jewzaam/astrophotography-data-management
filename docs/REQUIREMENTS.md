# Astrophotography Data Management Requirements

## Overview
This document outlines the requirements for a tool to manage astrophotography data across multiple years and projects, providing visibility into project states and workflow management.

## Data Organization Structure

### Root Directory Structure
- **Root Directory**: `Data` - Contains all astrophotography data
- **Rig Directories**: Subdirectories organized by optical setup (rig)

### Rig Naming Convention
Each rig directory follows the pattern:
```
<Optics Name>@f<Focal Ratio>+<Camera Name>
```

Where:
- **Optics Name**: User-defined short acronym representing the lens or telescope
- **Focal Ratio**: Actual focal ratio with 1 decimal precision (e.g., 4.0, 2.8, 10.0)
- **Camera Name**: Camera name as reported by ASCOM drivers or manual entry when no ASCOM driver exists

### Project Workflow Directories
Each rig directory contains workflow-based subdirectories following the template structure:

#### Standard Workflow Directories
- `00_Misc/` - Special case directory (equivalent to Dark Library at camera level)
- `10_Blink/` - Images awaiting visual inspection
- `20_Data/` - Data logging and organization phase
- `30_Master/` - Master file creation and storage
- `40_Process/` - Active image processing
- `50_Bake/` - Processing complete, pending final review
- `60_Done/` - Completed and published projects

#### Directory Flexibility Requirements
- Additional directories may exist (e.g., `99_Abandoned/`)
- Some standard directories may be missing
- System must gracefully handle variations in directory structure

### Detailed Directory Structure

#### Dark Library (`00_Misc/`)
- Temperature-based subdirectories
- Gain-based subdirectories (`GAIN_0`, `GAIN_100`)
- Flat darks directory (`FLATS`)

#### Target Directories (All workflow stages)
Each target has:
- `accept/` - Light frames that survived blink process
  - `DATE_CCYY-MM-DD/` - Date-organized subdirectories
    - `FILTER_<filter>_EXP_<seconds>/` - Filter and exposure organized files
    - Master darks and flats for the session
- `master/` - Processed master files
  - `CCYY-MM-DD/` - Date of master creation
    - `1x/` - Non-drizzled masters
    - `2x/` - 2x drizzled masters (when applicable)

#### Mosaic Support
- `PANEL_N/` subdirectories in `accept/` for mosaic panels
- Compatible with WBPP PANEL keyword grouping

## Functional Requirements

### Project State Management
1. **State Visibility**: Provide clear indication of project status across all workflow stages
2. **Work Queue Identification**: Identify projects ready for the next workflow step
3. **Progress Tracking**: Track project movement through workflow stages

### Directory Structure Handling
1. **Template Compliance**: Support the standard template directory structure
2. **Graceful Degradation**: Handle missing or additional directories
3. **Flexible Organization**: Adapt to user's organizational variations

### Data Integrity
1. **Reference Preservation**: Maintain master darks and flats in each date directory
2. **Non-destructive Workflow**: Preserve raw data throughout the process
3. **Temporary File Management**: Handle calibrated files in temporary locations

### Workflow Support
1. **Multi-year Data**: Handle data spanning multiple years
2. **Multiple Rigs**: Support multiple optical setups simultaneously
3. **Batch Operations**: Enable efficient management of multiple projects

## Technical Requirements

### File System Operations
- Read and analyze directory structures
- Identify project states based on file locations
- Handle large datasets efficiently

### Data Processing
- Parse rig naming conventions
- Extract metadata from directory structures
- Generate project status reports

### User Interface
- Present project status in human-readable format
- Provide actionable workflow recommendations
- Support batch operations on multiple projects

## Future Considerations
- Integration with PixInsight workflow
- Automated project progression
- Metadata extraction from image files
- Integration with astronomical databases
- Backup and archival management