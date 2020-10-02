#!/usr/bin/env python3
# DO NOT DELETE!!!!!!
# API KEY: SE278IZQK3CR4WEXGLUBYJCVF4OPMSAX7Z96F8J6BXAYNHK1H2TSYU3U52IP7VSQ
import vulners
import os
import json
import platform

vulners_api = vulners.Vulners(api_key="SE278IZQK3CR4WEXGLUBYJCVF4OPMSAX7Z96F8J6BXAYNHK1H2TSYU3U52IP7VSQ")
print('''
The Hound of Baskerville
____________________________
\n
\n
“It is not what we know, but what we can prove.”
― Arthur Conan Doyle, The Hound of the Baskervilles
\n
\n
''')

# takes os and turns it into a list we need indexes [2] for name and [4] for version
os_list = []
cmd_os = os.system('hostnamectl | grep "Operating System" > tmp.txt')
os_lines = open("tmp.txt", "r")
line = os_lines.readline()
for item in line.strip().split(" "):
    os_list.append(item)
# print(os_list)

os_name = os_list[2]
os_version = os_list[4]
# print("os name: {}  os ver: {}".format(os_name,os_version))


# Command to Query system's package manager
# -- Linux command to list installed packages & details
# -----> apt list --installed
# lists the installed packages of the system & save to text file

# detect os & adjust accordingly
'''
OS System List:
Ubuntu = apt
    sudo apt-get install python3-pip
    pkg_name [0], pkg_ver [1], pkg_arch [2] 
Debian = apt     
    sudo apt-get install python3-pip.
    pkg_name [0], pkg_ver [1], pkg_arch [2]
CentOS = yum
    pkg_name [], pkg_ver [], pkg_arch []

'''

print('''
\n
Please wait while we check to see if all necessary components are installed properly and up to date.
\n
''')
# pip install -U vulners
# install_ubuntu_pip =
# install_cent_pip =
# install_deb_pip =


def os_type():
    if os_name.lower() == "ubuntu":
        os.system("sudo apt-get install python3-pip > /dev/null && pip3 install -U vulners > /dev/null")
    elif os_name.lower() == "centos":
        os.system("sudo yum install python-pip > /dev/null && pip3 install -U vulners > /dev/null")
    elif os_name.lower() == "debian":
        os.system("sudo apt-get install python3-pip > /dev/null && pip3 install -U vulners > /dev/null")


os_type()




def installed_pkgs():
    if os_name.lower() == "ubuntu":
        os.system("sudo apt list --installed > installed_pkgs.txt")
    elif os_name.lower() == "centos":
        os.system("sudo yum list installed > installed_pkgs.txt")
    elif os_name.lower() == "debian":
        os.system("sudo apt list --installed > installed_pkgs.txt")
    else:
        print("Sorry this program is not supported by this Operating System")


installed_pkgs()

tmp_file = open("installed_pkgs.txt", "r")
pkg_filter_file = open("filtered_list.txt", "w")
pkg_to_test = open("filtered_list.txt", "r")


def detective():
    for pkg_line in tmp_file.readlines():
        if pkg_line != "\n":
            # strip line
            pkg_line.strip()
            # split on space
            parsed_lines = pkg_line.split(" ")
        if len(parsed_lines) > 2:
            # create delimeter
            temp = parsed_lines[0]
            # print(temp)
            delimeter = temp.find("/", 0)
            # seperate out the name from the rest in column 1 of pkg list
            pkg_name = temp[0:delimeter]
            # seperate out version
            pkg_ver = parsed_lines[1]  # !!! need to include the 'amd64' in index [2]
            # seperate out architecture version
            pkg_arch = parsed_lines[2]

            # print("package name: {} package version: {}".format(pkg_name, pkg_ver))
            package = ('{} {} {}'.format(pkg_name, pkg_ver, pkg_arch))
            pkg_filter_file.write(package)

            os_vulnerabilities = vulners_api.audit(os=os_name, os_version=os_version, package=[package])
            vulnerable_packages = os_vulnerabilities.get('packages')
            missed_patches_ids = os_vulnerabilities.get('vulnerabilities')
            cve_list = os_vulnerabilities.get('cvelist')
            how_to_fix = os_vulnerabilities.get('cumulativeFix')
            if len(cve_list) > 0:
                print('Package Scanned:    {} \n    CVE\'s found:\n    {}\n'.format(package, cve_list))
                # print('how to fix: {}'.format(how_to_fix))


detective()
