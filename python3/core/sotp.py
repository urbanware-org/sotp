#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# SOTP - Simple tool for reading, modifying and writing INI-like config files
# Main core module
# Copyright (C) 2017 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/sotp
# ============================================================================

__version__ = "1.0.3"

import configparser

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def read_option(file_path, section, option, fallback=None):
    """
        Parse config file and read out the value of a certain option.
    """
    try:
        # For details see the notice in the header
        from . import paval as pv

        pv.path(file_path, "config", True, True)
        pv.string(section, "section string")
        pv.string(option, "option string")
    except NameError:
        pass

    c = configparser.RawConfigParser()
    c.read(file_path)

    value = ""
    try:
        value = c.get(section, option)
    except configparser.NoSectionError:
        if fallback:
            return str(fallback)
        else:
            raise Exception("This section does not exist in the given " \
                            "config file.")
    except configparser.NoOptionError:
        if fallback:
            return str(fallback)
        else:
            raise Exception("This option does not exist in the given " \
                            "section.")

    return str(value)

def remove_option(file_path, section, option):
    """
        Remove a certain option from a section inside the config file.
    """
    try:
        # For details see the notice in the header
        from . import paval as pv

        pv.path(file_path, "config", True, True)
        pv.string(section, "section string")
        pv.string(option, "option string")
    except NameError:
        pass

    c = configparser.RawConfigParser()
    c.read(file_path)

    c.remove_option(section, option)
    with open(file_path, 'w') as fh_config:
        c.write(fh_config)

def remove_section(file_path, section):
    """
        Remove a certain section from the config file.
    """
    try:
        # For details see the notice in the header
        from . import paval as pv

        pv.path(file_path, "config", True, True)
        pv.string(section, "section string")
    except NameError:
        pass

    c = configparser.RawConfigParser()
    c.read(file_path)

    c.remove_section(section)
    with open(file_path, 'w') as fh_config:
        c.write(fh_config)

def write_option(file_path, section, option, value="", new_section=False,
                 new_file=False, force=False):
    """
        Write an option into a config file.
    """
    try:
        # For details see the notice in the header
        from . import paval as pv

        if not force:
            if new_file:
                pv.path(file_path, "config", True, False)
                new_section = True
            else:
                pv.path(file_path, "config", True, True)
            pv.string(section, "section string")
            pv.string(option, "option string")
    except NameError:
        if new_file:
            new_section = True

    c = configparser.RawConfigParser()
    c.read(file_path)

    if force:
        # This makes the parameters "new_section" and "new_file" obsolete, so
        # they will be ignored
        if not section in c.sections():
            c.add_section(section)
    else:
        if new_section:
            if section in c.sections():
                raise Exception("This section cannot be created, because " \
                                "it already exists.")
            c.add_section(section)
        else:
            if not section in c.sections():
                raise Exception("This section does not exist.")

    c.set(section, option, value)
    with open(file_path, 'w') as fh_config:
        c.write(fh_config)

# EOF
