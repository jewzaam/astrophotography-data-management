# Astrophotography Data Management Requirements

## Overview
This document outlines the requirements for a **new tool** to manage astrophotography data across multiple years and projects, providing visibility into project states and workflow management.

## Project Scope
**This is a clean-slate project.** The new tool will be built from scratch without referencing or depending on existing code. Current Python scripts serve only as requirements analysis input and will be replaced entirely by the new implementation.

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

### RAW Data Processing (Initial Scope)
**Process Flow**: Move first, then cull - executed as single batch operation.

1. **NINA File Parsing**: Parse NINA-generated filenames to extract metadata including:
   - Equipment: optic, camera, focal ratio
   - Target: target name, panel info (from FITS headers)
   - Session: date, filter, exposure time, temperature
   - Quality: HFR, RMS, star count, sensor temperature

2. **Rig-based Organization**: Sort files into appropriate rig directories using pattern `<Optics>@f<FocalRatio>+<Camera>`

3. **File Movement**: Move files from RAW directory to `10_Blink` workflow directories
   - Create target directory structure as needed
   - Create `accept` subdirectories during move process
   - Delete only empty RAW directories after successful moves

4. **Filename Normalization**: Rename files to standardized format preserving all metadata

5. **Quality-based Culling**: Filter images based on configurable thresholds per rig+target+panel+filter grouping:
   - HFR threshold filtering
   - RMS arcsec threshold filtering
   - Group-based evaluation (not global bucket review)

6. **Auto-rejection Logic**: Automatically reject poor images when rejection percentage below configurable threshold

7. **Reject Management**: Move rejected files to parallel reject directory structure preserving the same relative directory organization for potential recovery

### Project State Management (Future Scope)
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

## Open Questions

### Configuration Management Strategy
**Question**: How should rig-specific culling configurations be stored and managed?

**Current State**: Configuration parameters are passed as batch script arguments:
- `max_hfr`: Maximum Half Flux Radius threshold
- `max_rms`: Maximum RMS arcseconds threshold  
- `auto_yes_percent`: Auto-reject if rejects < this percentage
- `srcdir`: Source directory path
- `rejectdir`: Reject directory path

**Options**:
1. **Configuration Files**: YAML/JSON files per rig or global config file
2. **Database Storage**: Add configuration tables to astrophotography.sqlite (matches existing schema pattern)
3. **Hybrid Approach**: Database for dynamic configs, files for static settings

**Considerations**:
- Existing database has `camera`, `optic`, `profile` tables that could be extended
- Configuration may vary by rig (optic+camera combination)
- Need to maintain compatibility with current workflow

**Impact**: Affects maintainability, sharing configurations between tools, and runtime flexibility.

### File Conflict Handling
**Question**: How should the system handle potential filename conflicts during file movement?

**Current Assumption**: Conflicts are extremely unlikely due to:
- NINA enforces uniqueness during capture
- Timestamps and metadata in filenames provide natural uniqueness
- Files are moved (not copied) from source

**Consideration**: Should the system include conflict detection and resolution mechanisms as defensive programming, or rely on the assumption that conflicts cannot occur?

**Options**:
1. **No conflict handling** - Rely on NINA uniqueness guarantees
2. **Detection only** - Detect and error on conflicts
3. **Resolution strategies** - Timestamp suffixes, user prompts, etc.

### FITS Header Enhancement
**Question**: Should quality metrics from NINA filename be written to FITS headers during file movement?

**Current State**: NINA captures quality metrics (HFR, RMS, star count) in filename but NOT in FITS/XISF headers.

**Enhancement Opportunity**: During RAW→Blink movement, extract quality metrics from filename and write them to FITS headers.

**Benefits**:
- Quality data preserved even if file is renamed
- Complete reconstruction of directory path and filename from FITS headers alone
- Metadata survives file operations and workflow changes
- Better integration with FITS-aware tools

**Considerations**:
- FITS header standardization (which keywords to use)
- File modification during move operation
- Backward compatibility with existing tools
- Performance impact of FITS header writing

**Impact**: Enhances data durability and tool independence, but adds complexity to file movement process.

## Future Considerations
- Integration with PixInsight workflow
- Automated project progression
- Metadata extraction from image files
- Integration with astronomical databases
- Backup and archival management