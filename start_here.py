#!/usr/bin/python3.5

import subprocess
import re
import os
from distutils import dir_util
from distutils import file_util
#import json
#from pprint import pprint


# Default values for variables
DockerVerMinRequired = float(112.3)
# DockerFilePath_siteapp = 'docker_siteapp'
DockerFilePath_siteapp = '/afranky_site_data/docker_kitchen'
# DockerImageName = 'mytestsite'
DockerContainerName = 'afranky'
WebLocalPortForBind = '18080'
HostDataVolume = '/afranky_site_data'
SiteSourcePlace = '/home/mike/mywiki34/wiki20'
SiteSourcePlaceGit = 'https://github.com/mvutsk/mytestpysite'
SetupSiteContext = 'y'


def check_dock_file(DockerFilePath):
    """Checking if docker files are presented (at least...)"""
    if os.path.isdir(DockerFilePath):
        # if os.path.isfile(DockerFilePath + "/dck_mongodb" + "/Dockerfile"):
        #    print("Docker file for MongoDB: ", str(os.path.abspath(DockerFilePath + "/dck_mongodb" + "/Dockerfile")), "\n")
        # else:
        #    print("Cannot find Dockerfile in", str(os.path.abspath(DockerFilePath + "/dck_mongodb")), "\n")
        #    exit(1)
        if os.path.isfile(DockerFilePath + "/dck_nginx" + "/Dockerfile"):
            print("Docker file for Nginx: ", str(os.path.abspath(DockerFilePath + "/dck_nginx" + "/Dockerfile")), "\n")
        else:
            print("Cannot find Dockerfile in", str(os.path.abspath(DockerFilePath + "/dck_nginx")), "\n")
            exit(1)
        if os.path.isfile(DockerFilePath + "/dck_py3" + "/Dockerfile"):
            print("Docker file for Python3: ", str(os.path.abspath(DockerFilePath + "/dck_py3" + "/Dockerfile")), "\n")
        else:
            print("Cannot find Dockerfile in", str(os.path.abspath(DockerFilePath + "/dck_py3")), "\n")
            exit(1)
        if os.path.isfile(DockerFilePath + "/dck_py3_spd" + "/Dockerfile"):
            print("Docker file for Python3 spider: ", str(os.path.abspath(DockerFilePath + "/dck_py3_spd" + "/Dockerfile")), "\n")
        else:
            print("Cannot find Dockerfile in", str(os.path.abspath(DockerFilePath + "/dck_py3_spd")), "\n")
            exit(1)
    else:
        print("It is not a directory: ", DockerFilePath, "\n")
        exit(1)


def RepresentsInt(s):
    """Checking if value is int"""
    try:
        int(s)
        return True
    except ValueError:
        return False


def ask_value(question, val, vtype):
    """
    Asking and verifying values during preparation for installation
    :param question:
    :param val:
    :param vtype: d - dir, n - integer, v - any value
    :return:
    """

    okgo = False
    tinp = None
    while not okgo:
        qwe = question + " [" + val + "]:"
        tinp = input(qwe)
        if vtype == "d":
            if tinp:
                if os.path.isdir(tinp):
                    if os.access(tinp, os.W_OK):
                        okgo = True
                    else:
                        print("No write permissions to folder {} \n".format(tinp))
                else:
                    print("It is not a folder {} \n".format(tinp))
            elif val:
                tinp = val
                okgo = True
        elif vtype == "v":
            if tinp:
                okgo = True
            elif val:
                tinp = val
                okgo = True
        elif vtype == "n":
            if RepresentsInt(tinp):
                if 1024 < int(tinp) <= 65535:
                    print("Value {} is true.".format(tinp))
                    okgo = True
                else:
                    print("Value out of range 1024 < {} <=65535".format(tinp))
            elif not tinp and val:
                tinp = val
                okgo = True
            else:
                print("Must be int number in range 1024 < Value <= 65535")
    return tinp


def install_init():
    """Gathering information required for installation"""
    tinfo = """
    This script will build docker image from https://github.com/mvutsk/mytestpysite
    Will be asked for some additional information required for this installation,
    you can accept [DefaulValue] by pressing enter or type new value.
    Note, docker build command requires sudo access, you will be prompted to enter the password.
    Required installed docker and git.
    """
    print(tinfo)
    print('Ready to go? (y/n): ', end='')
    goyn = str(input())
    print("your choise: >>", goyn, "<<")
    if goyn not in ("y", "Y"):
        print("Ok, exiting from script.")
        exit()
    okgo = False
    while not okgo:
        print("Let's check necessary data.\n")
        global SiteSourcePlaceGit
        global SiteSourcePlace
        SiteSourcePlaceGit = ask_value("Source of kitchen", SiteSourcePlaceGit, "v")
        global DockerFilePath_siteapp
        DockerFilePath_siteapp = ask_value("Folder to place kitchen, will be created if absent", DockerFilePath_siteapp, "d")
#        global DockerImageName
#        DockerImageName = ask_value("Name of Docker image", DockerImageName, "v")
#        global DockerContainerName
#        DockerContainerName = ask_value("Name of Docker Container", DockerContainerName, "v")
        global HostDataVolume
        HostDataVolume = ask_value("Host folder for docker VOLUME mapping, will be created if absent", HostDataVolume, "d")
        global WebLocalPortForBind
        WebLocalPortForBind = ask_value("Local port number for binding with web server in docker", WebLocalPortForBind, "n")
        global SetupSiteContext
        SetupSiteContext = ask_value("Initial context (users/pages) setup for site (y/n) (recommended - y)", SetupSiteContext, "v")
        aokgo = None
        while not aokgo:
            aokgo = input("Confirm to start building: c - continue, e - edit, x - exit: ")
            if aokgo not in ("c", "x", "e"):
                aokgo = None
        if aokgo == "c":
            okgo = True
        elif aokgo == "e":
            okgo = False
        elif aokgo == "x":
            print("Exiting from script.")
            exit()
        if not os.path.exists(DockerFilePath_siteapp) and not os.path.isfile(DockerFilePath_siteapp):
            try:
                dir_util.mkpath(DockerFilePath_siteapp)
            except IOError as e:
                print("Cannot create folder in {}".format(DockerFilePath_siteapp), ", provide another path.")
                print(e)
                okgo = False


def pre_check():
    """ Checking installed docker version [and other params] """
    print("Checking docker version\n")
    docker_iver = None
    try:
        pp = subprocess.Popen('docker -v', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        docker_iver = pp.stdout.readline()
        docker_iver = re.search('(\d)+\.(\d)+\.(\d)+', str(docker_iver))
        print("Installed docker version: ", docker_iver.group(0))
        dc = docker_iver.group(0)
        docker_iver = re.subn('\.', '', str(dc), 1, 0)
    except ValueError as e:
        print("Something went wrong..\n")
        print(e)
    if float(docker_iver[0]) >= DockerVerMinRequired:
        print("Installed version is fine.\n")
    else:
        print("Installed version is lower than minimal required 1.12.3")


# def build_docker_image(DockerFilePath, DockerImage):
def build_docker_image(DockerFilePath):
    """Building docker images"""
    print("\nWill be used mongo:latest, downloading it.\n")
    subprocess.call(["sudo", "docker", "run", "--rm", "mongo:latest", "/bin/bash exit"])
    # print("\nBuilding MongoDB dck_mongodb.\n")
    # subprocess.call(
    #    ["sudo", "docker", "build", "-t", "dck_mongodb", str(os.path.abspath(DockerFilePath + "/dck_mongodb"))])
    print("\nImage mongo:latest downloaded.")
    print("\nBuilding Nginx dck_nginx.\n")
    subprocess.call(
        ["sudo", "docker", "build", "-t", "dck_nginx", str(os.path.abspath(DockerFilePath + "/dck_nginx"))])
    print("\nImage dck_nginx build completed.\nBuilding Python3 dck_py3.\n")
    subprocess.call(
        ["sudo", "docker", "build", "-t", "dck_py3", str(os.path.abspath(DockerFilePath + "/dck_py3"))])
    print("\nImage dck_py3 build completed.\n")
    subprocess.call(
        ["sudo", "docker", "build", "-t", "dck_py3_spd", str(os.path.abspath(DockerFilePath + "/dck_py3_spd"))])
    print("\nImage dck_py3_spd build completed.\n")

    #subprocess.call(["sudo", "docker", "images", "dck_mongodb"])
    subprocess.call(["sudo", "docker", "images", "mongo:latest"])
    subprocess.call(["sudo", "docker", "images", "dck_nginx"])
    subprocess.call(["sudo", "docker", "images", "dck_py3"])
    subprocess.call(["sudo", "docker", "images", "dck_py3_spd"])
    print("\n")


def create_start_stop_container_script():
    """Creating start|stop scripts for containers and init script for first run"""
    sInitCmd = "#!/bin/bash\n"
    sInitCmd += "if [[ `whoami` == 'root' ]]; then \n"

    # docker run -d --name dckmongo -v /my_site_data:/data -v /my_site_data/db:/data/db -p 27017:27017 mongo:latest mongod --logpath /data/logs/mongo/mongo1.log --logRotate reopen --logappend
    cmdMdb = " docker run -d --name dckmongo"
    cmdMdb += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdMdb += " -v " + str(os.path.abspath(HostDataVolume)) + "/db:/data/db"
    cmdMdb += " -p 27017:27017 mongo:latest mongod --logpath /data/logs/mongo/mongo1.log --logRotate reopen --logappend"
    cmdMdb += "\n"
    sInitCmd += cmdMdb
    sInitCmd += "sleep 3\n"

    # sudo docker run --rm --name dckpysite_tmp -v /my_site_data:/data -p 8080:8080 --link dckmongo:dckmongodb -ti dck_py3  init_db
    cmdPyInit = " docker run --rm --name dckpysite_tmp"
    cmdPyInit += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    if SetupSiteContext in ['y', 'Y']:
        cmdPyInit += " -p 18888:18888 --link dckmongo:dckmongodb -ti dck_py3 set_context"
    else:
        cmdPyInit += " -p 18888:18888 --link dckmongo:dckmongodb -ti dck_py3 set_site"
    #cmdPyInit += " -p 18888:18888 --link dckmongo:dckmongodb -ti dck_py3 init_db"
    cmdPyInit += "\n"
    sInitCmd += cmdPyInit
    sInitCmd += "sleep 3\n"

    # sudo docker run -d --name dckpysite -v /my_site_data:/data -p 8080:8080 --link dckmongo:dckmongodb dck_py3 start
    cmdPyStart = " docker run -d --name dckpysite"
    cmdPyStart += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdPyStart += " -p 18888:18888 --link dckmongo:dckmongodb dck_py3 start"
    cmdPyStart += "\n"
    sInitCmd += cmdPyStart
    sInitCmd += "sleep 3\n"

    # docker run -d --name dcknginx -v /my_site_data:/data -p 18080:80 --link dckpysite:dckpysite dck_nginx
    cmdNginx = " docker run -d --name dcknginx"
    cmdNginx += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdNginx += " -p " +str(WebLocalPortForBind) + ":80"
    cmdNginx += " --link dckpysite:dckpysite dck_nginx"
    cmdNginx += "\n"
    sInitCmd += cmdNginx

    # sudo docker run --name dckpyspider_xml -ti -v /afranky_site_data:/data --link dcknginx:dcknginx dck_py3_spd xml
    cmdPySpdStart = " docker run --name dckpyspider_csv -ti -v"
    cmdPySpdStart += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdPySpdStart += ' --network="host" dck_py3_spd csv\n'
    # cmdPySpdStart += " --link dcknginx:dcknginx dck_py3_spd csv\n"
    cmdPySpdStart += " docker run --name dckpyspider_xml -ti -v "
    cmdPySpdStart += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdPySpdStart += ' --network="host" dck_py3_xml xml\n'
    # cmdPySpdStart += " --link dcknginx:dcknginx dck_py3_spd xml\n"
    cmdPySpdStart += " docker run --name dckpyspider_json -ti -v "
    cmdPySpdStart += " -v " + str(os.path.abspath(HostDataVolume)) + ":/data"
    cmdPySpdStart += ' --network="host" dck_py3_json json\n'
    # cmdPySpdStart += " --link dcknginx:dcknginx dck_py3_spd json\n"
    sInitCmd += cmdPySpdStart
    sInitCmd += "sleep 3\n"

    sInitCmd += "else\n echo 'Please run me as root.'\nfi\n"
    try:
        with open(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_create_site_init', 'w') as dinit_start:
            dinit_start.write(sInitCmd)
            dinit_start.close()
            print("Script for first init created ", dinit_start.name)
    except IOError as e:
        print(e)
        exit(1)

    startContCmd = "#!/bin/bash\n"
    startContCmd += "if [[ `whoami` == 'root' ]]; then \n"
    cmd =  " docker start dckmongo\n"
    cmd += " sleep 3\n"
    cmd += " echo 'Started.'\n"
    cmd += " docker start dckpysite\n"
    cmd += " sleep 3\n"
    cmd += " echo 'Started.'\n"
    cmd += " docker start dcknginx\n"
    cmd += " echo 'Started.'\n"
    startContCmd += cmd
    startContCmd += "else\n echo 'Please run me as root.'\nfi\n"
    try:
        with open(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.start', 'w') as d_start:
            d_start.write(startContCmd)
            d_start.close()
            print("Script for starting containers created ", d_start.name)
    except IOError as e:
        print(e)
        exit(1)

    stopContCmd = "#!/bin/bash\n"
    stopContCmd += "if [[ `whoami` == 'root' ]]; then \n"
    cmd = " docker stop -t 3 dcknginx\n"
    cmd += " docker stop dckpysite\n"
    cmd += " docker stop dckmongo\n"
    cmd += " echo 'All stopped.'\n"
    stopContCmd += cmd
    stopContCmd += "else\n echo 'Please run me as root.'\nfi\n"
    try:
        with open(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.stop', 'w') as d_stop:
            d_stop.write(stopContCmd)
            d_stop.close()
            print("Script for stopping containers created ", d_stop.name)
    except IOError as e:
        print(e)
        exit(1)

    os.chmod(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_create_site_init', mode=0o744)
    os.chmod(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.start', mode=0o744)
    os.chmod(str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.stop', mode=0o744)


def get_site_from(destination, source, stype):
    """Getting site from git or from local source"""
    if stype == "local":
        print("Copying data from {} to {}".format(source, destination))
        if not os.path.exists(destination):
            dir_util.mkpath(destination)
        try:
            dir_util.copy_tree(source, destination)
        except IOError as e:
            print(e)

    elif stype == "git":
        print("Making clone of repo from {} to {}".format(source, destination))
        try:
            # subprocess.call(["git", "clone", source, destination])
            subprocess.check_call(["git", "clone", source, destination])
        except ValueError as e:
            print(e)
            print("\n Cannot proceed with it.")
            exit(1)


def create_work_folders():
    """Makes necessary steps before starting live"""
    print("  Creating necessary folders in {}".format(HostDataVolume))
    print("   {}/db\n   {}/logs/mongo\n   {}/logs/nginx\n   {}/logs/uwsgi\n   {}/site"
          .format(HostDataVolume, HostDataVolume, HostDataVolume, HostDataVolume, HostDataVolume))
    try:
        if not os.path.exists(HostDataVolume) and not os.path.isfile(HostDataVolume):
            os.mkdir(HostDataVolume)
        os.mkdir(HostDataVolume + '/db')
        os.chmod(HostDataVolume + '/db', mode=0o777)
        os.mkdir(HostDataVolume + '/site')
        os.mkdir(HostDataVolume + '/logs')
        os.chmod(HostDataVolume + '/logs', mode=0o777)
        os.mkdir(HostDataVolume + '/logs/mongo')
        os.chmod(HostDataVolume + '/logs/mongo', mode=0o777)
        os.mkdir(HostDataVolume + '/logs/nginx')
        os.chmod(HostDataVolume + '/logs/nginx', mode=0o777)
        os.mkdir(HostDataVolume + '/logs/uwsgi')
        os.chmod(HostDataVolume + '/logs/uwsgi', mode=0o777)
    except IOError as e:
        print(e)
        exit(1)

def first_init_run():
    """First run to initialize db and site"""
    print("Ok, executing init script to make all ready.")
    init_script = str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_create_site_init'
    subprocess.call(["sudo", init_script])
    os.chmod(init_script, mode=0o444)


def final_info():
    """Final information about what was done here and where to find it"""
    info = """\n\n\n\n    If all went without error, you are ready to start with it.
    Was done:
    1. Created docker containers from public images:
        dckmongo    - just latest public
        dcknginx    - public 1.11.10 + nginx config
        dckpysite   - public python 3.5.3 + necessary for work addons
        dckpyspider - public python 3.5.3 + addons + spider script
    2. Site context, if you have requested it (users/pages):
        login:password - userX:userXpass
    2.1. If not, you need to create users and pages manually...
    3. Scripts for maintaining containers (not docker compose solution):
     """
    info += "        " + str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.start\n'
    info += "        " + str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_containers.stop\n'
    info += "        " + str(os.path.abspath(HostDataVolume)) + "/" + DockerContainerName + '_create_site_init  - already executed\n'
    info += "\n    4. Site initialized and running.\n"
    info += "         You can access it on http://127.0.0.1:" + WebLocalPortForBind
    info += """
    5. Created containers for web spider with output in csv, xml, json, they will ask some info during execution:
       docker start -i dckpyspider_csv
       docker start -i dckpyspider_xml
       docker start -i dckpyspider_json
    """
    info += "Output in format afranky_output_YYYY-MM-DD-HHMISS.(csv|xml|json) will be available in "
    info += str(os.path.abspath(HostDataVolume)) + "/ folder."
    info += "\nEnjoy..."
    print(info)


def main():
    """ Go main """
    pre_check()
    install_init()
    get_site_from(DockerFilePath_siteapp, SiteSourcePlaceGit, "git")
    check_dock_file(DockerFilePath_siteapp)
    build_docker_image(DockerFilePath_siteapp)
    create_start_stop_container_script()
    create_work_folders()
    get_site_from(HostDataVolume + '/site/afranky', DockerFilePath_siteapp + '/site/afranky', "local")
    first_init_run()
    final_info()

if __name__ == '__main__':
    main()
