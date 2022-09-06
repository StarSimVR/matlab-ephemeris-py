#!/usr/bin/env python3

################################################################################
##
## \copyright
##      Copyright (C) 2022 Kevin Matthes
##
##      This program is free software; you can redistribute it and/or modify
##      it under the terms of the GNU General Public License as published by
##      the Free Software Foundation; either version 2 of the License, or
##      (at your option) any later version.
##
##      This program is distributed in the hope that it will be useful,
##      but WITHOUT ANY WARRANTY; without even the implied warranty of
##      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##      GNU General Public License for more details.
##
##      You should have received a copy of the GNU General Public License along
##      with this program; if not, write to the Free Software Foundation, Inc.,
##      51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
##
################################################################################

################################################################################
##
## \author  Kevin Matthes
## \brief   The main source file.
## \date    2022
## \file    matlab_ephemeris.py
## \note    See `LICENSE' for full license.
##          See `README.md' for project details.
##
## This script is intended to update a given scene file with data queried from
## a Matlab installation.
##
################################################################################

'''
This script is intended to update a given scene file with data queried from a
Matlab installation.
'''

#
# Resources.
#

from argparse import ArgumentParser
from argparse import Namespace
from pathlib import Path
import json
from matlab import engine as Matlab



################################################################################
##
## \brief   The possible astronomical objects.
##
## The astronomical objects to choose from.
##
## Both the ephemeris reference point as well as the object the data is queried
## for require one value of this list.
##
################################################################################

CHOICES =   [ 'Sun'
            , 'Mercury'
            , 'Venus'
            , 'Earth'
            , 'Moon'
            , 'Mars'
            , 'Jupiter'
            , 'Saturn'
            , 'Uranus'
            , 'Neptune'
            , 'Pluto'
            , 'SolarSystem'
            , 'EarthMoon'
            ]



################################################################################
##
## \brief   Query the data from Matlab.
## \param   arguments   The command line arguments to process the query with.
## \return  Position and velocity.
##
################################################################################

def ephemeris (arguments: Namespace) -> ([float], [float]):
    '''
    This function will perform the actual query.

    The given command line arguments contain all required data in order to call
    the respective Matlab function.  Therefore, Matlab is invoked as a process
    on its own and given the required values.

    At the end, a 2-tuple of position and velocity will be returned.  Both are
    lists of three float components.
    '''

    engine = Matlab.start_matlab ()

    julian_date = engine.JulianDate ( arguments.year
                                    , arguments.month
                                    , arguments.day
                                    )

    return engine.planetEphemeris   ( julian_date
                                    , arguments.reference_point
                                    , arguments.object
                                    , units = arguments.unit
                                    )



################################################################################
##
## \brief   The main function.
## \return  Nothing.
##
################################################################################

def main () -> None:
    '''
    This function will handle the control flow of this scipt.

    This script requires at least the following data:

    * the path to the file to edit;
    * the object to query the ephemeris data for;
    * the day to query the ephemeris data for;
    * the month to query the ephemeris data for; and
    * the year to query the ephemeris data for.

    At option, the following data can be set, as well:

    * the reference point;
    * the scalar; and
    * the unit.

    The reference point is the centre point from which the ephemeris data shall
    be queried.  It is set to 'Sun', by default.

    The scalar is the floating point constant to multiply the resulting vectors
    of the query with.  It is set to 1.0, by default.

    The unit controls how the dimension of length will be measured.  It can be
    set either to kilometres or astronomical units.  The default value is
    kilometres.

    This script provides a help option in order to request a quick summary of
    the configured command line options.

    When the configuration by the command line options is completed, the
    arguments are used in order to perform the query.  After that, the results
    will be multiplied by the scalar.  Finally, the results are written to the
    scene file.

    When writing to the scene file, there will be a backup created, by default.
    Then, the object the ephemeris data was queried for is going to fetched from
    the scene file by name.  Its values for both position and velocity will be
    set to the ephemeris data received from Matlab.  Finally, the new scene will
    be written to the original file path.  The backup ensures that this
    procedure is not going to destroy any settings.

    It is also possible to give this script a file pattern.  Then, all files
    matching this pattern will be set accordingly.
    '''

    parser = ArgumentParser ()
    parser.add_argument ( '-d'
                        , '--day'
                        , dest = 'day'
                        , help = 'The day to query the ephemeris data for.'
                        , required = True
                        , type = int
                        )
    parser.add_argument ( '-f'
                        , '--file'
                        , dest = 'file'
                        , help = 'The file to edit.'
                        , required = True
                        , type = str
                        )
    parser.add_argument ( '-m'
                        , '--month'
                        , dest = 'month'
                        , help = 'The month to query the ephemeris data for.'
                        , required = True
                        , type = int
                        )
    parser.add_argument ( '-o'
                        , '--object'
                        , choices = CHOICES
                        , dest = 'object'
                        , help = 'The object to request the ephemeris data for.'
                        , required = True
                        )
    parser.add_argument ( '-r'
                        , '--reference-point'
                        , choices = CHOICES
                        , default = 'Sun'
                        , dest = 'reference_point'
                        , help = 'The ephemeris reference point.'
                        , type = str
                        )
    parser.add_argument ( '-s'
                        , '--scalar'
                        , default = 1.
                        , dest = 'scalar'
                        , help = 'The value to scale the queried data by.'
                        , type = float
                        )
    parser.add_argument ( '-u'
                        , '--unit'
                        , choices = ['km', 'AU']
                        , default = 'km'
                        , dest = 'unit'
                        , help = 'The unit of position and velocity.'
                        )
    parser.add_argument ( '-y'
                        , '--year'
                        , dest = 'year'
                        , help = 'The year to query the ephemeris data for.'
                        , required = True
                        , type = int
                        )
    arguments = parser.parse_args ()

    position, velocity = ephemeris (arguments)
    position = [element * arguments.scalar for element in position]
    velocity = [element * arguments.scalar for element in velocity]

    update (arguments, position, velocity)



################################################################################
##
## \brief   Write the results to the scene file.
## \param   arguments   The command line arguments to take into account.
## \param   position    The position vector to assign.
## \param   velocity    The velocity vector to assign.
## \return  Nothing.
##
################################################################################

def update (arguments: Namespace, position: [float], velocity: [float]) -> None:
    '''
    This function will update the scene file.  If a file pattern is passed to
    this function, all files matching this pattern will be updated.

    The scene file is a JSON file with the held astronomical objects in the
    array objects.  In there, there are multiple objects defined with a certain
    name.  The first object whose name matches the object name the ephemeris
    data was queried for from Matlab will be updated with the given position and
    velocity vectors.

    For each updated scene file, a backup will be created.  This shall ensure
    that no data will be lost.

    All scene files need to exist and to be readable.
    '''

    for element in Path ().cwd ().glob (arguments.file):
        backup = element.with_suffix ('.bak')
        element.rename (backup)

        with open (backup, 'rt') as in_file, open (element, 'wt') as out_file:
            scene = json.load (in_file)
            astobjs = scene['objects']

            for astobj in astobjs:
                if astobj['name'].lower () == arguments.object.lower ():
                    astobj['position'] = position
                    astobj['velocity'] = velocity
                    break

            scene['objects'] = astobjs
            out_file.write (json.dumps (scene, indent = 4) + '\n')



#
# Invocation of the main function.
#

if __name__ == "__main__":
    main ()

################################################################################
