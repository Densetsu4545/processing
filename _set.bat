@echo off
rd /q /s oshareKabegami
python convert.py
python svg.py
copy oshareKabegami.pde oshareKabegami/oshareKabegami.pde