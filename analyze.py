import redis



class Analyzer():

	def __init__(self):
		self.db = redis.StrictRedis(host='10.1.5.12', port=6379, db=5)
		self.reportfile = open("report.txt", 'w')

	def processes_by_count(self):

		processess = self.db.smembers("processess")
		p_tmp = []
		for p in processess:
			p_tmp.append({"name":p, "count":0})

		processess = p_tmp

		machines = self.db.smembers("machines")
		for machine in machines:
			ps = self.db.smembers(machine+":processess")
			for p in ps:
				for dic in processess:
					if dic['name'] == p:
						dic['count'] += 1


		processess = sorted(processess, key= lambda k:k['count'], reverse=True)

		for p in processess:
			self.reportfile.write('\r\n')
			self.reportfile.write(str(p)+'\r\n')
			for machine in self.db.smembers(p['name']+":machines"):
				print machine+":"+p['name']+":path"
				try:
					path = machine + ":" + str(self.db.get(machine+":"+p['name']+":path"))
					self.reportfile.write(path+'\r\n')
				except TypeError:
					self.reportfile.write(machine)

	def close_report(self):
		self.reportfile.close()

if __name__ == "__main__":
	a = Analyzer()
	a.processes_by_count()
	a.close_report()


