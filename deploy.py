#!/usr/bin/python
from os import *

def read_war_files(path):
    wars = []
    for file in listdir(path):
        if is_war(file):
            wars.append(path + file)

    return wars

def is_war(file):
    return file.endswith('.war')

def prepare_deploy_statement(war_file):
    tag = "tag"
    archive_name = war_file.split('/')[-1]
    deployment_name = archive_name.replace(".war", "") + "-" + tag

    return "deploy " + war_file + " --runtime-name=" + archive_name + " --name=" + deployment_name

def main():
    path = "/home/raphaelpaiva/Scripts/test/"
    wars = read_war_files(path)

    for war in wars:
        print prepare_deploy_statement(war)


if __name__ == "__main__": main()
