# astrophotography-data-management
Tool to manage my astrophotography data.

## Directory Structure Notes

I have one "Data" directory everything is put into. Under that I have a directory per **rig** (optical setup). Each rig directory follows a specific naming pattern that captures the complete optical configuration.

### Rig Directory Naming Convention

Each rig directory uses the format: `<Optics Name>@f<Focal Ratio>+<Camera Name>`

- **Optics Name**: A short acronym I've assigned to the telescope or lens (e.g., "RC8", "TMB130", "Redcat51")
- **Focal Ratio**: The actual focal ratio with one decimal place precision (e.g., "4.0", "2.8", "10.0")  
- **Camera Name**: The camera name as reported by ASCOM drivers, or manually entered when no ASCOM driver exists

**Examples:**
- `RC8@f8.0+ZWO ASI2600MM Pro` - RC8 telescope at f/8.0 with ASI2600MM camera
- `Redcat51@f4.9+AP26CC` - Redcat 51 lens at f/4.9 with AP26CC camera
- `TMB130@f7.0+Canon T2i` - TMB 130mm refractor at f/7.0 with Canon T2i camera

### Workflow Directory Structure

Inside each rig directory, I have folders for each stage of a target's lifecycle, ordered by prefixing with a number so I can't miss a step. I use 2 digits so I could slot in something new if needed without changing anything else.

- **00_Misc**: Special case directory (equivalent to Dark Library at camera level) for miscellaneous files and calibration frames
- **10_Blink**: Anything I have not yet done a visual inspection of yet - need to blink through and accept/reject frames
- **20_Data**: Add to Data Log - I maintain a database of all the data I have with goals per filter. Adding the data to the database after blink makes it easy to decide what I want to shoot next
- **30_Master**: Done collecting data, time to cut master lights. Projects can pile up so this way I don't forget I haven't done this step
- **40_Process**: Working on processing a final image. I tend to think about the final image as well for a bit and keep the project around for PixInsight in case I want to fiddle with things after I'm "done"
- **50_Bake**: I think I'm done processing but I probably am not. I put it here to remind me later to move it on to "done". I have not published this on astrobin yet
- **60_Done**: Really really done, published on astrobin. From here I'd move it to long term backup

In the dark library dir I have sub dirs for each temp and gain and a special one for flat darks.  I generally have darks for my flats and darks at gain 0 and 100, so dirs FLATS, GAIN\_0, GAIN\_100.

In every other dir each sub-dir is the target name.  Inside that I have "accept" and "master".  “Accept” has all the lights that survived blink.  Historically I would keep all the rejected subs but I just delete them now.  “Master” is all the processed master lights, organized by the date created.  I've occasionally found it useful to review older masters if a new master shows some problem.  In "accept" the structure is sub-dir per day formatted as "DATE\_CCYY-MM-DD" with sub-dir for each filter \+ exposure time, "FILTER\_\<filter name\>\_EXP\_\<exposure seconds\>".

The master darks and flats for each night go into the DATE directory.  This means duplicating master darks and master flats.  The upside is I never have to worry about deleting reference data.  My dark library can be deleted and it doesn't matter because all the masters are copied to where they are needed.  And when loading in PixInsight I literally just load the whole "accept" directory in WBPP and am done.

In the "master" directory I create a sub-dir for the date I created the master, i.e. "CCYY-MM-DD".  Under this directory I have a sub-dir for each level of drizzle.  Many times this just means a "1x" directory (no drizzle) but I still do this so it's consistent when I do a "2x" drizzle.

I never keep calibrated files, those are stuffed into a temporary directory and deleted when I don't need them.  I prefer having the raw lights with master darks and flats.  I thought about keeping raw data for the darks and flats but the amount of data adds up and I didn't have any need to re-process them to date.

If a target is a mosaic I add a “PANEL\_N” sub-dir in “accept” for each panel and use the “PANEL” keyword in WBPP for grouping.  This lets me manage either each panel or the mosaic in one consistent way.

Here's an example screenshot of the dir structure which closely follows what is stated above:

[https://www.dropbox.com/s/t26ysvcgsc2xrrt/ExampleFileStructure.JPG?dl=0](https://www.dropbox.com/s/t26ysvcgsc2xrrt/ExampleFileStructure.JPG?dl=0) 