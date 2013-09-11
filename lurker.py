try:
	import wmi
except Exception, e:
	print e, "Unable to import wmi package"

import pythoncom
import threading
import time
import redis

class Lurker(threading.Thread):

	def __init__(self):
		threading.Thread.__init__ (self)
		self.targets = self.get_my_ips()
		self.db = redis.StrictRedis(host='10.1.5.12', port=6379, db=5)
		self.db.flushdb()

	def get_my_ips(self):
		c = wmi.WMI()
		ip_addresses = []
		target_ips = []

		for interface in c.Win32_NetworkAdapterConfiguration(IPEnabled=1):
			for ip_address in interface.IPAddress:
				ip_addresses.append(ip_address)
		
		for ip in ip_addresses:
			for n in range(255):
				parts = ip.split(".")
				print "parts = " , parts
				try:
					target_ips.append("{0}.{1}.{2}.{3}".format(parts[0],parts[1],parts[2],n))
				except IndexError:
					### if index error, then was ipv6 address
					continue

		return target_ips

	def get_processes(self, remote_console, ip):
		for p in remote_console.Win32_Process():
			self.db.sadd("machines", ip)
			self.db.sadd("processess", p.Name)
			self.db.set(ip+":"+p.name+":path", p.ExecutablePath)
			self.db.sadd(p.Name+":machines", ip)
			self.db.sadd(ip+":processess", p.Name)
			print p.ProcessId, p.Name, p.ExecutablePath

	def remote_lurk(self):
		for ip in self.targets:
			pythoncom.CoInitialize()
			try:
				print "[+] Connecting to {0}".format(ip)
				temp_console = wmi.WMI(
						computer=str(ip),
						user="southside\csteinke",
						password="6andromeda9"
					)
				self.get_processes(temp_console, ip)
			except Exception, e:
				print "[-] Failed to connect to {0}".format(ip)
				print e
				print ""
			finally:
				pythoncom.CoUninitialize()

	def local_lurk(self):
		c = wmi.WMI()
		get_processes(c)




if __name__ == "__main__":
	lurker = Lurker()
	lurker.remote_lurk()