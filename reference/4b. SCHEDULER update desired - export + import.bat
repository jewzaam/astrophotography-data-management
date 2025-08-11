@echo Exporting CSVs
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\scheduledb-export-csv.py"
@echo Importing CSVs
@python "%DROPBOX%\Family Room\Astrophotography\Data\scripts\scheduledb-import-csv.py"
@pause
