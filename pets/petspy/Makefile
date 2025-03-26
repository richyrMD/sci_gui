# Compiler
FC  = gfortran
# FPC = f2py
FPC = python3 -m numpy.f2py

# Include-Pfad für pets.h
INCLUDE_PATH = /home/richy/Schreibtisch/post-processing/sci_gui/pets/petspy

# Compile flags
FCFLAGS  = -shared -fdefault-real-8 -fdefault-double-8 -ffree-line-length-0 -fPIC -I$(INCLUDE_PATH)
FPCFLAGS = -c --fcompiler=gnu95 --f90flags="-fdefault-real-8 -fdefault-double-8 -ffree-line-length-0" -I$(INCLUDE_PATH)

# Zielmodule
PYMODULE = petspy
SOURCE   = pets.F90
LIB      = libpets.so

# Ziel: petspy.so
petspy.so: pywrappets.F90 
	$(FC) $(FCFLAGS) -o $(LIB) $(SOURCE)
	$(FPC) $(FPCFLAGS) -L$(INCLUDE_PATH) -I. -lpets -m $(PYMODULE) $^

# Ziel: Clean
clean: 
		rm -f libpets.so petspy.so pets.mod
