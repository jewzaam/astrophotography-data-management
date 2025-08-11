@taskkill /IM Dropbox.exe /F

@REM @python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\\open-next-pixinsight-instance.py"
@REM @python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\\open-next-pixinsight-instance.py"

@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\prepare-raw.py"
@start /d "C:\Program Files (x86)\Dropbox\Client\" Dropbox.exe


@echo "C8Ef10, HFR>4.6, RMS>2, auto=30%"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\cull.py" --srcdir "F:\Astrophotography\Data\C8E@f10.0+ZWO ASI2600MM Pro\10_Blink" --rejectdir "C:\tmp" --max_hfr=4.6 --max_rms=2 --auto_yes_percent=30
@echo "C8Ef10, HFR>5.5, RMS>2, auto=100%"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\cull.py" --srcdir "F:\Astrophotography\Data\C8E@f10.0+ZWO ASI2600MM Pro\10_Blink" --rejectdir "C:\tmp" --max_hfr=5.5 --max_rms=2 --auto_yes_percent=101
@echo "R135, HFR>4, RMS>2 auto=30%"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\cull.py" --srcdir "F:\Astrophotography\Data\R135@f2.8+AP26CC\10_Blink" --rejectdir "C:\tmp" --max_hfr=4 --max_rms=2 --auto_yes_percent=30

@pause
