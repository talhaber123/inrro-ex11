class Node:
	def __init__(self, data, positive_child = None, negative_child = None):
		self.data = data
		self.positive_child = positive_child
		self.negative_child = negative_child
		
class Record:
	def __init__(self, illness, symptoms):
		self.illness = illness
		self.symptoms = symptoms
	
			
def parse_data(filepath):
	with open(filepath) as data_file:
		records = []
		for line in data_file:
			words = line.strip().split()
			records.append(Record(words[0], words[1:]))
		return records
		
		
class Diagnoser:
	def __init__(self, root):
		self.root = root
		
	def diagnose(self, symptoms):
		return self.diagnose_helper(root, symptoms)

	def diagnose_helper(self,node, symptoms):
		if (node.positive_child == None) and node.negative_child == None:
			return node.data

		if node.data in symptoms:
			return self.diagnose_helper(node.positive_child, symptoms)
		else:
			return self.diagnose_helper(node.negative_child, symptoms)

	def calculate_success_rate(self, records):
	#Record (illness, symptoms)
		counter = 0
		for record in records:
			if self.diagnose(record[1]) == record[0]:
				counter += 1
		success_rate = counter/len(records)
		return success_rate

	def all_illnesses(self):
		list_all_disease = self.all_illnesses_helper(root)
		d = dict()
		for illnesse in list_all_disease:
			if illnesse not in d:
				d[illnesse] = 1
			else:
				d[illnesse] += 1

		items = list(d.items())

		items.sort(key =lambda item:item[1], reverse = True)

		return items


	def all_illnesses_helper(self, node):
		if (node.positive_child == None) and node.negative_child == None:
			return [node.data]

		x = self.all_illnesses_helper(node.positive_child)
		y = self.all_illnesses_helper(node.negative_child)
		return x+y

	def paths_to_illness(self, illness):
		return self.paths_to_illness_helper(illness,self.root)


	def paths_to_illness_helper(self, illness,node):
		if ((node.positive_child == None) and node.negative_child == None):
			if illness == node.data:
				return []
			else:
				return None

		x = self.paths_to_illness_helper(illness,node.positive_child)
		y = self.paths_to_illness_helper(illness,node.negative_child)

		if x != None:
			if x == []:
				x = [[True]]
			else:
				for i in x:
					i.insert(0,True)
		if y != None:
			if y == []:
				y = [[False]]
			else:
				for i in y:
					i.insert(0,False)

		if x == None and y == None:
			return []
		if y == None and x != None:
			return x
		if x == None and y != None:
			return y
		else:
			return x+y



def build_tree(records, symptoms):
	pass
	
def optimal_tree(records, symptoms, depth):
	pass
	
if __name__ == "__main__":
	
	# Manually build a simple tree.
	#                cough
	#          Yes /       \ No
	#        fever           healthy
	#   Yes /     \ No
	# influenza   cold
	
	
	flu_leaf = Node("influenza", None, None)
	cold_leaf = Node("cold", None, None)
	inner_vertex = Node("fever", flu_leaf, cold_leaf)
	healthy_leaf = Node("healthy", None, None)
	root = Node("cough", inner_vertex, healthy_leaf)
	
	diagnoser = Diagnoser(root)
	print(diagnoser.paths_to_illness("cold"))


	# Simple test
	diagnosis = diagnoser.diagnose(["cough"])
	if diagnosis == "cold":
		print("Test passed")
	else:
		print("Test failed. Should have printed cold, printed: ", diagnosis)
		
	# Add more tests for sections 2-7 here.