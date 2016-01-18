#!/usr/bin/python
import os
import sys
def read_war_files(path):
    wars = []
    for file in os.listdir(path):
        if is_war(file):
            wars.append(path + file)

    return wars

def is_war(file):
    return file.endswith('.war')

def prepare_deploy_statement(war_file, tag=None):
    if tag == None:
        tag = "notag"

    archive_name = war_file.split('/')[-1]
    deployment_name = archive_name.replace(".war", "") + "-" + tag

    return "deploy " + war_file + " --runtime-name=" + archive_name + " --name=" + deployment_name

def print_deploy_script(wars, tag):

        batch = len(wars)

        if  batch > 1:
            print "batch"

        for war in wars:
            print prepare_deploy_statement(war, tag)

        if batch > 1:
            print "run-batch"

def usage():
    print "Please provide the full path where the war files are located"
    print "Example:"
    print "  $ " + sys.argv[0] + " /path/to/deployment/"
    exit(1)

def extract_tag(path):
    if path.endswith("/"):
        path = path[:-1]

    return path.split("/")[-1]

def main():
    if len(sys.argv) <= 1:
        usage()

    path = sys.argv[1]
    wars = read_war_files(path)
    tag = extract_tag(path)

    print_deploy_script(wars, tag)

if __name__ == "__main__": main()
