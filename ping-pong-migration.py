mport commands
import subprocess
import re
import sys
import time
import signal

prog_name = sys.argv[0]

usage_msg = """
usage: python %s <guest name> <destion host ip> <migration times>
When do ping-pong migration, run this scripts on both src and des hots.
""" % prog_name

def err(s):
    print("ERROR: " + s)
    sys.exit(1)

def usage():
    print(usage_msg)
    sys.exit(1)

args = sys.argv
if len(args) != 4:
    usage()

guest_name = sys.argv[1]
des_ip = sys.argv[2]
ping_pong_times = sys.argv[3]

cmd = "rm -rf /root/migration_time.log"
status, output = commands.getstatusoutput(cmd)

def writelog(log):
    f = open("/root/migration_time.log",'a')
    f.write(log)
    f.close()

num = 0
while num < int(ping_pong_times):
    cmd = "virsh list"
    status, output = commands.getstatusoutput(cmd)
    if guest_name not in output:
        print "guest %s is not running and can not migrate" % guest_name
        time.sleep(20)
        continue

    # do migration
    cmd = "virsh migrate --timeout 120  --verbose --live %s qemu+ssh://%s/system" % (guest_name, des_ip)
    print cmd
    process = subprocess.Popen(cmd, shell=True)
    
    # check migration info when completed
    active_flag = True
    while active_flag:
        cmd = "virsh qemu-monitor-command %s --hmp \"info migrate\"" % guest_name
        status, output = commands.getstatusoutput(cmd)
        if "Migration status: completed" in output:
	    print "ping-pong No.%d" %num
            status = re.search(
                "Migration\sstatus:\scompleted",
                output,
                re.M | re.I)
            if status:
                print status.group()
            total_time = re.search(
                "total\stime:\s[0-9]+\smilliseconds",
                output,
                re.M | re.I)
            if total_time:
                print total_time.group()
                total_time = re.search(
                    "[0-9]+",
                    total_time.group(),
                    re.M | re.I)
                print total_time.group()
            downtime = re.search(
                "downtime:\s[0-9]+\smilliseconds",
                output,
                re.M | re.I)
            if downtime:
                print downtime.group()
                downtime = re.search(
                    "[0-9]+",
                    downtime.group(),
                    re.M | re.I)
                print downtime.group()
                if downtime.group() is not "0":
                    log = "%s %s\n" %(total_time.group(), downtime.group())
                    writelog(log)
            active_flag = False
            time.sleep(10)
    num = num + 1

sys.exit(0)

