SRC = main.py
NUITKA = nuitka
OUTPUT_DIR = build
MSVC_VERSION = latest
EXECUTABLE = main.exe
RESOURCES_DIR = resources

NUITKA_OPTS = --standalone \
			  --enable-plugin=pyqt6 \
			  --enable-plugin=upx \
			  --output-dir=$(OUTPUT_DIR) \
			  --msvc=$(MSVC_VERSION) \
			  --show-progress \
			  --follow-imports \
			  --windows-icon-from-ico=$(RESOURCES_DIR)/icon.ico \
			  --no-pyi-file \
			  --windows-console-mode=disable \
			  --include-data-dir=$(RESOURCES_DIR)=$(RESOURCES_DIR)/ \
			  -o $(EXECUTABLE)

all: build

build:
	@echo "Building project..."
	python.exe -m $(NUITKA) $(NUITKA_OPTS) $(SRC)

clean:
	@echo "Cleaning up..."
	rm -rfv $(OUTPUT_DIR)

run: build
	./$(EXECUTABLE)

.PHONY: all build clean run
