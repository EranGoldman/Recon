import subprocess
import multiprocessing
import os
import errno
from IPy import IP

def checkpath(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def multProc(targetin, scanip, port):
    jobs = []
    p = multiprocessing.Process(target=targetin, args=(scanip, port))
    jobs.append(p)
    p.start()
    return

def getIp():
    """ Defines the ip range to be scanned """
    try:
        ip_start = raw_input("Please enter the ip's to scan (example 192.168.0.1/24)  : ")
        ip = IP(ip_start)
        return ip
    except Exception as e:
        raise Exception(e)

def dnsEnum(ip_address, port):
    print "INFO: Detected DNS on " + ip_address + ":" + port
    if port.strip() == "53":
        SCRIPT = "./dnsrecon.py %s" % (ip_address)  # execute the python script
        subprocess.call(SCRIPT, shell=True)
    return


def httpEnum(ip_address, port):
    print "INFO: Detected http on " + ip_address + ":" + port
    print "INFO: Performing nmap web script scan for " + ip_address + ":" + port
    checkpath("./results/nmap")
    HTTPSCAN = "nmap -sV -Pn -vv -p %s --script-args=unsafe=1 --script=*http*vuln*.nse,http-vhosts,http-userdir-enum,http-apache-negotiation,http-backup-finder,http-config-backup,http-default-accounts,http-methods,http-method-tamper,http-passwd,http-robots.txt -oN ./results/%s_http.nmap.%s %s" % (
    port, ip_address, port, ip_address)
    results = subprocess.check_output(HTTPSCAN, shell=True)
    DIRBUST = "./dirbust.py http://%s:%s %s" % (ip_address, port, ip_address)  # execute the python script
    subprocess.call(DIRBUST, shell=True)
    NIKTOSCAN = "nikto -host %s -p %s > ./results/%s.%s_nikto" % (ip_address, port, ip_address, port)
    subprocess.call(NIKTOSCAN, shell=True)
    return


def mssqlEnum(ip_address, port):
    print "INFO: Detected MS-SQL on " + ip_address + ":" + port
    print "INFO: Performing nmap mssql script scan for " + ip_address + ":" + port
    checkpath("./results/nmap")
    MSSQLSCAN = "nmap -vv -sV -Pn -p %s --script-args=unsafe=1 --script=mysql-vuln-cve2012-2122.nse,ms-sql-info,ms-sql-config,ms-sql-dump-hashes --script-args=mssql.instance-port=1433,smsql.username=sa,mssql.password=sa -oX ./results/nmap/%s_mssql.xml %s" % (
    port, ip_address, ip_address)
    results = subprocess.check_output(MSSQLSCAN, shell=True)
    return

def sshEnum(ip_address, port):
    print "INFO: Detected SSH on " + ip_address + ":" + port
    SCRIPT = "./sshrecon.py %s %s" % (ip_address, port)
    subprocess.call(SCRIPT, shell=True)
    return


def snmpEnum(ip_address, port):
    print "INFO: Detected snmp on " + ip_address + ":" + port
    SCRIPT = "./snmprecon.py %s" % (ip_address)
    subprocess.call(SCRIPT, shell=True)
    return


def smtpEnum(ip_address, port):
    print "INFO: Detected smtp on " + ip_address + ":" + port
    if port.strip() == "25":
        SCRIPT = "./smtprecon.py %s" % (ip_address)
        subprocess.call(SCRIPT, shell=True)
    else:
        print "WARNING: SMTP detected on non-standard port, smtprecon skipped (must run manually)"
    return


def smbEnum(ip_address, port):
    print "INFO: Detected SMB on " + ip_address + ":" + port
    if port.strip() == "445":
        SCRIPT = "./smbrecon.py %s 2>/dev/null" % (ip_address)
        subprocess.call(SCRIPT, shell=True)
    return


def ftpEnum(ip_address, port):
    print "INFO: Detected ftp on " + ip_address + ":" + port
    SCRIPT = "./ftprecon.py %s %s" % (ip_address, port)
    subprocess.call(SCRIPT, shell=True)
    return