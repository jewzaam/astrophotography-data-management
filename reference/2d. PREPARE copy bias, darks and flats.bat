@echo Copying bias, darks and flats...
@python.exe "%DROPBOX%\Family Room\Astrophotography\Data\scripts\copycalibration.py" --src_bias_dir="C:\tmp_pi\WBPP\_calibration\master"  --src_dark_dir="C:\tmp_pi\WBPP\_calibration\master" --src_flat_dir="C:\tmp_pi\WBPP\_calibration\master"  --dest_bias_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Bias Library" --dest_dark_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Dark Library" --dest_flat_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Flat Stash"

@echo for C8E@f10+ZWO ASI2600MM Pro...
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\copycalibration.py" --src_dark_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Dark Library" --src_flat_dir="C:\tmp_pi\WBPP\_calibration\master" --dest_light_dir="F:\Astrophotography\Data\C8E@f10.0+ZWO ASI2600MM Pro\10_Blink" --darks_required_properties="exposureseconds,settemp,camera,gain,offset,type" --flats_required_properties="date,optic,filter,settemp,camera,gain,offset,type"

@echo for SQA55@f5.3+ATR585M...
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\copycalibration.py" --src_dark_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Dark Library" --src_flat_dir="C:\tmp_pi\WBPP\_calibration\master" --dest_light_dir="F:\Astrophotography\Data\SQA55@f5.3+ATR585M\10_Blink" --darks_required_properties="exposureseconds,settemp,camera,gain,offset,type,readoutmode" --flats_required_properties="date,optic,filter,settemp,camera,gain,offset,type,readoutmode"

@echo for DWARFIII@f4.3+DWARFIII...
@python.exe "%DROPBOX%\Family Room\Astrophotography\Data\scripts\copycalibration.py" --src_dark_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Dark Library\DWARFIII" --src_flat_dir="C:\Users\jewza\Dropbox\Family Room\Astrophotography\Data\_Flats Stash\DWARFIII" --dest_light_dir="F:\Astrophotography\Data\DWARFIII@f4.3+DWARFIII\10_Blink" --darks_required_properties="exposureseconds,camera,gain,type" --flats_required_properties="date,optic,filter,camera,gain,type"


@echo Done!
@pause



