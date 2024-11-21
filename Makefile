.PHONY: setup run clear reset demo

run: setup
	@python .

setup:
	@bash setup.sh

clean:
	@echo "Cleaning __pycache__"

	@find . -type d -name '__pycache__' -exec rm -rf {} +

reset: clean
	@echo "Cleaning face_data ......"
	@find "./identify_face/face_data/" -type f -name '*.png' -exec rm -f {} +

	@echo "Cleaning label Data......"
	@find "./database/" -type f -name '*.pkl' -exec rm -f {} +

demo: reset
	@echo "Preparing for demo ...."
	@cp ./demo/*.png ./identify_face/face_data/
