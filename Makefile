# Use G++ compiler
CXX := g++

# Set the value of the debug flag
DEBUG ?= 0
BUILDTYPE := $(if $(filter 1,$(DEBUG)),debug,release)

# Set the default target for make
.DEFAULT_GOAL := all

# ----- PREPROCESSOR FLAGS -----
# Include src/ directory with all builds
# Generate dependency lists and add phony rules for headers
# Set DEBUG macro from Makefile instead of in code
CPPFLAGS += -iquote src -MMD -MP -DDEBUG=$(DEBUG)

# ----- COMPILER FLAGS -----
# Enforce strict (pedantic) C++17 standard
# Enable common and extra warnings and use descriptive debug information (-g)
CXXFLAGS += -std=c++17 -pedantic -Wall -Wextra -g 
# Optimize for debug or release builds
CXXFLAGS += $(if $(filter 1,$(DEBUG)),-Og,-O2)

# ----- LINKER FLAGS -----
# Paths and linker settings
LDFLAGS :=
# Libraries
LDLIBS :=

# ----- BUILD TREES -----
BUILDDIR := build
OBJDIR := $(BUILDDIR)/$(BUILDTYPE)/obj
DEPDIR := $(BUILDDIR)/$(BUILDTYPE)/dep
BINDIR := $(BUILDDIR)/bins

# ----- ALL BUILDS -----
CORE_INC := $(filter %/,$(wildcard src/*/ src/*/*/ src/*/*/*/))
CPPFLAGS += $(addprefix -iquote ,$(CORE_INC))

CORE_SRC := $(wildcard src/*.cpp src/*/*.cpp src/*/*/*.cpp)

CORE_OBJDIR := $(OBJDIR)/core
CORE_OBJ := $(patsubst src/%.cpp,$(CORE_OBJDIR)/%.o,$(CORE_SRC))

CORE_DEPDIR := $(DEPDIR)/core
CORE_DEP := $(patsubst $(CORE_OBJDIR)/%.o,$(CORE_DEPDIR)/%.d,$(CORE_OBJ))

# Create directory for dependency lists, if it does not already exist
# Compile core modules
$(CORE_OBJDIR)/%.o: src/%.cpp
	@mkdir -p $(dir $@) $(dir $(CORE_DEPDIR)/$*.d)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MF $(CORE_DEPDIR)/$*.d -c -o $@ $<

# ----- NORMAL/DEBUG BUILDS -----
# main function is compiled separately in case we decide to add a test build
APP_INC := app
APP_SRC := app/main.cpp
APP_OBJ := $(OBJDIR)/app/main.o
APP_DEP := $(DEPDIR)/app/main.d

$(APP_OBJ): CPPFLAGS += -iquote $(APP_INC)

# Compile main.cpp
$(APP_OBJ): $(APP_SRC)
	@mkdir -p $(dir $@) $(dir $(APP_DEP))
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -MF $(APP_DEP) -c -o $@ $<
	
# ----- LINK -----
BIN := $(BINDIR)/prog_$(BUILDTYPE)

# Build both on plain `make`
all: build_release build_debug
	@echo "To run normal (release) build, use \"make run\""
	@echo "To run debug build, use \"make debug\""
	@echo "To check normal build for memory leaks, use \"make valgrind\""
.PHONY: all

build_release:
	$(MAKE) DEBUG=0 $(BINDIR)/prog_release
	@echo "Release build done."

build_debug:
	$(MAKE) DEBUG=1 $(BINDIR)/prog_debug
	@echo "Debug build done."

$(BIN): $(CORE_OBJ) $(APP_OBJ)
	@mkdir -p $(dir $@)
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS)

# Include generated dependencies
-include $(CORE_DEP) $(APP_DEP)

.PHONY: clean run debug valgrind

clean:
	$(RM) -r $(BUILDDIR)

run:
	./$(BINDIR)/prog_release

debug:
	./$(BINDIR)/prog_debug

valgrind: $(BIN)
	valgrind --leak-check=full \
			 --track-origins=yes \
			 --show-leak-kinds=all \
			 ./$(BIN)