.PHONY: test reportes upload_reports reporte_calificacion descargar_planos all

test:
	coverage run -m pytest tests/ -v
	coverage report
	coverage html

download_antecedentes_complementarios:
	python scripts/load/antecedentes_complementarios.py

descargar_planos:
	python scripts/load/descargar_planos.py

setup_database:
	python -m scripts.setup

run_workflow:
	python -m scripts.workflow

all:
	python -m scripts.setup
	python -m scripts.workflow

montaje:
	python -m scripts.montaje.load_cuadrillas
	python -m scripts.montaje.componentes
	python -m scripts.montaje.montaje
