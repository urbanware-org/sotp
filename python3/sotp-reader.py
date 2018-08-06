#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# SOTP - Simple tool for reading, modifying and writing INI-like config files
# Config reader script
# Copyright (C) 2017 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# GitHub: https://github.com/urbanware-org/sotp
# GitLab: https://gitlab.com/urbanware-org/sotp
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import sotp

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Parse a config file and return the value of a " \
                      "requested option.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_avalue("-c", "--config-file", "config file to parse", "config_file",
                 None, True)
    p.add_avalue("-o", "--option", "option to read out", "option", None, True)
    p.add_avalue("-s", "--section", "section that contains the option",
                 "section", None, True)

    # Optional arguments
    p.add_avalue("-f", "--fallback", "value to return in case the given " \
                 "section or option does not exist", "fallback", None, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print(sotp.get_version())
        sys.exit(0)

    args = p.parse_args()
    try:
        value = sotp.read_option(args.config_file, args.section, args.option,
                                 args.fallback)
        print(value)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

