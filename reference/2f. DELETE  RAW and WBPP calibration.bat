@echo Deleting RAW bias, darks and flats...
@taskkill /IM Dropbox.exe /F
@REM be careful, calibration dir is WIPED
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\prepare-delete-calibration.py" --input_dir="%DROPBOX%\Family Room\Astrophotography\RAW\BIAS" --calibration_dir="C:\tmp_pi\WBPP\_calibration"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\prepare-delete-calibration.py" --input_dir="%DROPBOX%\Family Room\Astrophotography\RAW\DARK" --calibration_dir="C:\tmp_pi\WBPP\_calibration"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\prepare-delete-calibration.py" --input_dir="%DROPBOX%\Family Room\Astrophotography\RAW\FLAT" --calibration_dir="C:\tmp_pi\WBPP\_calibration"
@echo Done!
@start /d "C:\Program Files (x86)\Dropbox\Client\" Dropbox.exe
@pause
