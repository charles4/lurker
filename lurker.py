try:
	import wmi
except Exception, e:
	print e, "Unable to import wmi package"

import pythoncom
import threading
import time

class Lurker(threading.Thread):

	def __init__(self):
		threading.Thread.__init__ (self)
		self.targets = self.get_my_ips()

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
				target_ips.append("{0}.{1}.{2}.{3}".format(parts[0],parts[1],parts[2],n))

		return target_ips

	def get_processes(self, remote_console):
		for p in remote_console.Win32_Process():
			print p.ProcessId, p.Name

	def remote_lurk(self):
		for ip in self.targets:
			pythoncom.CoInitialize()
			try:
				print "[+] Connecting to {0}".format(ip)
				temp_console = wmi.WMI(
						computer=str(ip),
						user="csteinke",
						password="6andromeda9"
					)
				self.get_processes(temp_console)
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