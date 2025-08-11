@echo Updating database from Data folders.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\database-update.py" --fromdir "F:\Astrophotography\Data\C8E@f10.0+ZWO ASI2600MM Pro\20_Data" --modeCreate
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\database-update.py" --fromdir "F:\Astrophotography\Data\SQA55@f5.3+ATR585M\20_Data" --modeCreate
@echo "SKIPPING Archive until it handles .zip files"
@REM @echo Updating database from Archive data.
@REM @python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\database-update.py" --fromdir "F:\Astrophotography\Data" --createOnly
@echo Updating accepted counts.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\scheduledb-update-accepted.py"
@echo Updating CSV and totals.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\summary.py" --fromdir "F:\Astrophotography\Data\C8E@f10.0+ZWO ASI2600MM Pro\20_Data"
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\summary.py" --fromdir "F:\Astrophotography\Data\SQA55@f5.3+ATR585M\20_Data"
@REM @python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\summary.py" --fromdir "F:\Astrophotography\Data"

@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\report.py"

@pause
