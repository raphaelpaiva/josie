#!/usr/bin/python
import os
import sys
import argparse
import cli_output

def main():
    args = parse_args()
    path = os.path.abspath(args.path) + "/"
    domain = args.domain
    undeploy_pattern = args.undeploy_pattern

    if undeploy_pattern:
        skip_undeploy = True
    else:
        skip_undeploy = args.skip_undeploy

    wars = read_war_files(path)
    tag = extract_tag(path)

    if not skip_undeploy:
        cli_output.print_undeploy_script(wars)

    if undeploy_pattern:
        cli_output.print_undeploy_pattern(undeploy_pattern)

    cli_output.print_deploy_script(wars, tag)

def parse_args():
    parser = argparse.ArgumentParser(description="Generates [un]deploy commands which you can pipe through jboss-cli script.")
    parser.add_argument("path", help="the path where the .war packages are stored")
    parser.add_argument("--skip-undeploy",
                        help="do not generate undeploy commands",
                        action="store_true")
    parser.add_argument("--undeploy-pattern", help="specify a regex pattern for the undeploy cammand. This implies --skip-undeploy.")
    parser.add_argument("--domain",
                        help="prepare statements for domain mode, instead of standalone",
                        action="store_true")
    return parser.parse_args()


def usage():
    print "Please provide the full path where the war files are located"
    print "Example:"
    print "  $ " + sys.argv[0] + " /path/to/deployment/"
    exit(1)

def error(message=None, code=1):
    if message != None:
        print "[ERROR]: " + message

    usage()
    exit(code)

def read_war_files(path):
    wars = []
    for file in os.listdir(path):
        if is_war(file):
            wars.append(path + file)

    return wars

def is_war(file):
    return file.endswith('.war')

def extract_tag(path):
    if path.endswith("/"):
        path = path[:-1]

    return path.split("/")[-1]

if __name__ == "__main__": main()
