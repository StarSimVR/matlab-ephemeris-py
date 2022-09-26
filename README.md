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

## Description

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
