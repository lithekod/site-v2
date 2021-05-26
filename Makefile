BUILD_DIR := website/build
VENV := venv

.DEFAULT_GOAL := server
.PHONY: build clean clean-venv love server 

build: $(BUILD_DIR)

$(BUILD_DIR):
	python3 freezer.py

clean:
	rm -rf $(BUILD_DIR)

clean-venv:
	rm -rf $(VENV)

love:
	@echo "<3"

server: $(VENV)
	@(. $(VENV)/bin/activate && flask run -p 5001 --reload)

$(VENV):
	python3 -m venv $(VENV)
	@(. $(VENV)/bin/activate && pip install -r requirements.txt)

