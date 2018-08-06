#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# SOTP - Simple tool for reading, modifying and writing INI-like config files
# Config writer script
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

    p.set_description("Modify an existing or create new config file.")
    p.set_epilog("Further information and usage examples can be found " \
                 "inside the documentation file for this script.")

    # Required arguments
    p.add_predef("-a", "--action", "action to perform", "action",
                 ["remove", "write", "force-write"], True)
    p.add_avalue("-c", "--config-file", "config file to modify",
                 "config_file", None, True)
    p.add_avalue("-s", "--section", "section for the option", "section", None,
                 True)

    # Optional arguments
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch(None, "--new-file", "create a new config file", "new_file",
                 True, False)
    p.add_switch(None, "--new-section", "create a new section",
                 "new_section", True, False)
    p.add_avalue("-o", "--option", "option to write", "option", None,
                 False)
    p.add_avalue("-v", "--value", "value to set for the option", "value",
                 None, False)
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
        if "write" in args.action:
            if args.option == None:
                raise Exception("An option is required.")

            force = False
            if args.action == "force-write":
                force = True

            sotp.write_option(args.config_file, args.section, args.option,
                              args.value, args.new_section, args.new_file,
                              force)
        else:
            if args.new_file:
                raise Exception("The '--new-file' argument does not make " \
                                "sense when deleting contents.")
            elif args.new_section:
                raise Exception("The '--new-section' argument does not " \
                                "make sense when deleting contents.")

            if args.option == None:
                sotp.remove_section(args.config_file, args.section)
            else:
                sotp.remove_option(args.config_file, args.section,
                                   args.option)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

