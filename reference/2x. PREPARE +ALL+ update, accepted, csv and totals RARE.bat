@echo ===== WARNING =====
@echo All targets and accepted data will be reset and reconstructed.
@echo Cancel script if you do not want to do this!
@echo ===================
@pause
@echo Deleting target and accepted data...
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\database-reset.py"
@echo Updating database from data.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\database-update.py" --fromdir "F:\Astrophotography\Data" --modeCreate --modeUpdate --modeDelete
@echo Updating accepted counts.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\scheduledb-update-accepted.py"
@echo Updating CSV and totals.
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\summary.py" --fromdir "F:\Astrophotography\Data"
@pause
