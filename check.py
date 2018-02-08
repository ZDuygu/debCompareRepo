#!/usr/bin/python

import sys
import re

######
# https://github.com/nyucel/pardus-check/blob/master/get_package_info.py
######

def get_package_info(package_info, info):
    return re.search(info+":(.*)", package_info).group(1)

def get_package_sha256sum(package_info):
    return get_package_info(package_info, 'SHA256')

def get_package_version(package_info):
    return get_package_info(package_info, 'Version')

def get_package_name(package_info):
    return get_package_info(package_info, 'Package')

def get_package_filename(package_info):
    return './' + '/'.join(get_package_info(package_info, 'Filename').split('/')[2:])
###

packages_file_path1 = sys.argv[1]
packages_file1 = file(packages_file_path1).read()
packages_list1 = packages_file1.split('\n\n')

sha256_1 = {}
version_1 = {}

for package_info in packages_list1:
    if len(package_info) < 10:
        continue
    package_name = get_package_name(package_info)
    package_filename = get_package_filename(package_info)
    package_sha256sum = get_package_sha256sum(package_info)
    package_version = get_package_version(package_info)
    sha256_1[package_filename] = package_sha256sum
    version_1[package_filename] = package_version


sha256_2 = {}
version_2 = {}

packages_file_path2 = sys.argv[2]
packages_file2 = file(packages_file_path2).read()
packages_list2 = packages_file2.split('\n\n')

for package_info in packages_list2:
    if len(package_info) < 10:
        continue
    package_name = get_package_name(package_info)
    package_filename = get_package_filename(package_info)
    package_sha256sum = get_package_sha256sum(package_info)
    package_version = get_package_version(package_info)
    sha256_2[package_filename] = package_sha256sum
    version_2[package_filename] = package_version

samePkg = {}
diffVer = {}

for key in dict.keys(sha256_1):
    if sha256_2.has_key(key):
        if sha256_1[key] == sha256_2[key]:
            samePkg[key] = version_1[key]
        else:
            diffVer.setdefault(key,[]).append(version_1[key])
            diffVer.setdefault(key,[]).append(version_2[key])
        del sha256_1[key]
        del sha256_2[key]
        
for key in dict.keys(sha256_2):
    if sha256_1.has_key(key):
        if sha256_1[key] == sha256_2[key]:
            samePkg[key] = version_2[key]
        else:
            diffVer.setdefault(key,[]).append(version_1[key])
            diffVer.setdefault(key,[]).append(version_2[key])
        del sha256_1[key]
        del sha256_2[key]
    
print 'Ayni Surume Ait Paket Sayisi: ', len(samePkg)
print '\nFarkli Surume Sahip Paketler: ', len(diffVer)
for key in dict.keys(diffVer):
    print "Paket adi: ", key, "\t1. Depo Ver.: ", diffVer[key][0], "\t2. Depo ver.: ", diffVer[key][1]
print '\n1. Depo Farkli Paketler: ', len(sha256_1)
for key in dict.keys(sha256_1):
    print "Paket adi: ", key, "\t1. Depo Ver.: ", version_1[key]
print '\n2. Depo Farkli Paketler: ', len(sha256_2)
for key in dict.keys(sha256_2):
    print "Paket adi: ", key, "\t2. Depo Ver.: ", version_2[key]
