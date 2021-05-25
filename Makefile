BUILD_DIR=website/build
VENV=venv

.PHONY: build clean clean-venv love server 

# Start a development server that reloads

server: $(VENV)
	(. $(VENV)/bin/activate && flask run -p 5001 --reload)

# Virtual environments

$(VENV):
	python3 -m venv $(VENV)
	(. $(VENV)/bin/activate && pip install -r requirements.txt)

clean-venv:
	rm -rf $(VENV)

# Building a static version of the website

build: $(BUILD_DIR)

$(BUILD_DIR):
	python3 freezer.py

# Misc.

clean:
	rm -rf $(BUILD_DIR)

love:
	@echo "<3"
