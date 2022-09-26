<!---------------------- GNU General Public License 2.0 ------------------------
--                                                                            --
-- Copyright (C) 2022 Kevin Matthes                                           --
--                                                                            --
-- This program is free software; you can redistribute it and/or modify       --
-- it under the terms of the GNU General Public License as published by       --
-- the Free Software Foundation; either version 2 of the License, or          --
-- (at your option) any later version.                                        --
--                                                                            --
-- This program is distributed in the hope that it will be useful,            --
-- but WITHOUT ANY WARRANTY; without even the implied warranty of             --
-- MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              --
-- GNU General Public License for more details.                               --
--                                                                            --
-- You should have received a copy of the GNU General Public License along    --
-- with this program; if not, write to the Free Software Foundation, Inc.,    --
-- 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.                --
--                                                                            --
------------------------------------------------------------------------------->

<!------------------------------------------------------------------------------
--
--  AUTHOR      Kevin Matthes
--  BRIEF       Important information regarding this project.
--  COPYRIGHT   GPL-2.0
--  DATE        2022
--  FILE        README.md
--  NOTE        See `LICENSE' for full license.
--
------------------------------------------------------------------------------->

# matlab-ephemeris-py

## Summary

Add initial positions and velocities from Matlab to a given scene file.

## License

This project's license is **GPL-2.0** (as of June 1991).  The whole license text
can be found in `LICENSE` in the main directory of this repository.  The brief
version is as follows:

> Copyright (C) 2022 Kevin Matthes
>
> This program is free software; you can redistribute it and/or modify
> it under the terms of the GNU General Public License as published by
> the Free Software Foundation; either version 2 of the License, or
> (at your option) any later version.
>
> This program is distributed in the hope that it will be useful,
> but WITHOUT ANY WARRANTY; without even the implied warranty of
> MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
> GNU General Public License for more details.
>
> You should have received a copy of the GNU General Public License along
> with this program; if not, write to the Free Software Foundation, Inc.,
> 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

## Software Requirements

| Requirement       | Type          | Role                                  |
|:------------------|:-------------:|:--------------------------------------|
| Doxygen           | application   | source code documentation             |
| Git               | application   | build artifact removal                |
| Just              | Rust binary   | execution of the build instructions   |
| Latexmk           | application   | LaTeX compilation of Doxygen manual   |
| Matlab            | application   | interfaced application                |
| Numpy             | library       | Python maths library                  |
| Pylint            | application   | Python linter                         |
| Python            | environment   | source code interpreter               |
| TeX Live (full)   | package       | LaTeX environment for Doxygen manual  |

Since the script is written in *Python 3*, an appropriate Python interpreter is
required for its execution.  The script uses functionalities of both *Matlab*
and *Numpy*.  These dependencies need to be installed in order to ensure the
script being working.

Various checks of the source code will be invoked automatically by *Just*.  All
required steps are defined in the `.justfile` and explained in the corresponding
section below.

A code quality check with *Pylint* is configured.

Any build artifacts will be removed by *Git*.

The source code contains docstrings to be processed by *Doxygen*.  By default,
both an HTML and a LaTeX manual will be compiled.  They are saved in dedicated
directories in the repository's root.  The LaTeX manual needs to be finalised
with according compilers.  Their invocation is managed by Doxygen itself by the
provision of multiple build scripts.  Instead of relying on them, this project
defines an equal finalisation routine based upon *Latexmk*.  This finalisation
will be called automatically by Just.  Please note that the compilation of a
LaTeX project requires the installation of a LaTeX distribution.  The
recommended distribution is the *full* installation of *TeX Live*.

## Description

[StarSimVR](https://github.com/StarSimVR/godot) is a simulator for the behaviour
of astronomical objects.  The corresponding setups can be defined in JSON files
to be read by the application.  These setups also include an initial position as
well as an initial velocity for each astronomical object.

In order to define realistic scenes, real positions and velocities can be freely
added to the scene files.  In order to avoid mistakes due to copying and pasting
the numbers to the JSON files by hand, an automation therefore will come in
handy.

Matlab provides several functionalities to query such astronomical data for a
fixed set of astronomical objects.  This script will interface the local Matlab
installation in order to add the queried astronomical data to the respective
scene file(s).

## Command Line Options

### Date to Query

```
-d <day>
-m <month>
-y <year>
```

The interface to Matlab requires the specification of the date to query the data
for.  The order of the date components can be passed to this script in arbitrary
order.  All components need to be integers.

All three information are mandatory.

### Files to Edit

```
-f <pattern>
```

The script requires the specification of a file pattern.  All existing,
readable, writable and valid StarSimVR scene files which the pattern can be
matched against successfully will be edited.

This information is mandatory.

### Objects

```
-o <object 1> [<object 2> [<object 3> ...]]
-r <object>
```

When calling the script, the astronomical objects to query the data for need to
be passed with `-o`.  The number of queried objects is arbitrary.  Hence, all
configured objects can be queried with just one call to this script.

Furthermore, a reference point is needed.  It is set to the sun, by default, and
can be altered with `-r`.  Here, the same objects are possible as for `-o`.

The flag `-o` is mandatory while `-r` is optional.

### Scalar

```
-s <float>
```

If one wishes to scale the retrieved data from Matlab, this can be done with
this flag.  It requires the specification of a floating point number.  This flag
is set to `1.0`, by default.

This information is optional.

### Unit of the Data

```
-u <unit>
```

The data queried from Matlab can be converted to various units.  Possible are
both kilometres as well as Astronomical Units.  Kilometres are the default.

This information is optional.

## Build Instructions

All build instructions are configured as Just recipes in the `.justfile` located
in the repository root.  An overview about all defined recipes can be requested
by calling the following command in a terminal.

```
just --list
```

### Default Recipe

```
just
```

When calling Just without any recipe, the default recipe will be executed.  This
is the Doxygen manual compilation as well as the linting with Pylint.

### All Recipes

```
just a
just all
```

This recipe is designed to invoke all meaningful other recipes.  This utility
recipe is intended as an abbreviation during the development of this project.
All meaningful recipes are executed in the following order.  The purposes of
the recipes are explained in subsequent sections.

1. `just clear`
2. `just check`

### Code Quality Check

```
just c
just check
```

This is an abbreviation for the compilation of the Doxygen manual and the
linting of the source code.  The Doxygen manual compilation will identify
undocumented symbols and is, hence, considered a check, as well.  The linting is
obviously a quality check.

### Removal of Build Artifacts

```
just clr
just clear
```

All build artifacts will be removed from the whole repository.  The selection of
the files and directories to remove is controlled by the `.gitignore` as the
respective Git command is invoked by this recipe.

### Doxygen Manual

```
just d
just doxygen
```

All source files are equipped with docstrings in order to explain the code.
Doxygen will compile these docstrings to manuals in the following formats:

* HTML
* PDF

The finalisation of the LaTeX manual is defined as a hard coded part of this
recipe.  The compiled LaTeX manual will be copied to the repository root.

### Linting

```
just l
just lint
```

Lint the source code with Pylint.  This ensures a good code quality.

<!----------------------------------------------------------------------------->
