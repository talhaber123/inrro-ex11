class Node:
    def __init__(self, data, positive_child=None, negative_child=None):
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
        return self.diagnose_helper(self.root, symptoms)

    def diagnose_helper(self, node, symptoms):
        if (node.positive_child == None) and node.negative_child == None:
            return node.data

        if node.data in symptoms:
            return self.diagnose_helper(node.positive_child, symptoms)
        else:
            return self.diagnose_helper(node.negative_child, symptoms)

    def calculate_success_rate(self, records):
        # Record (illness, symptoms)
        counter = 0
        for record in records:
            if self.diagnose(record.symptoms) == record.illness:
                counter += 1
        success_rate = counter / len(records) if records else 0
        return success_rate

    def all_illnesses(self):
        list_all_disease = self.all_illnesses_helper(self.root)
        d = dict()
        for illnesse in list_all_disease:
            if illnesse not in d:
                d[illnesse] = 1
            else:
                d[illnesse] += 1
        items = list(d.keys())
        items.sort(key=lambda item: d[item], reverse=True)
        return items

    def all_illnesses_helper(self, node):
        if (node.positive_child is None):
            return [node.data] if node.data else []
        x = self.all_illnesses_helper(node.positive_child)
        y = self.all_illnesses_helper(node.negative_child)

        return x + y

    def paths_to_illness(self, illness):
        all_paths = []
        self.paths_to_illness_helper(illness, self.root, [], all_paths)
        return all_paths

    def paths_to_illness_helper(self, illness, node, path_till_here,
                                    list_of_paths):
        if node.positive_child is None or node.positive_child is None:
            if illness == node.data:
                list_of_paths.append(path_till_here)
            return

        self.paths_to_illness_helper(illness, node.positive_child,
                                         path_till_here + [True] ,
                                         list_of_paths)
        # path_till_here.pop()
        # path_till_here.append(False)

        self.paths_to_illness_helper(illness, node.negative_child,
                                         path_till_here + [False],
                                         list_of_paths)
        # path_till_here.pop()

    #         if ((node.positive_child == None) and node.negative_child == None):
    #     if illness == node.data:
    #         return []
    #     else:
    #         return None


#
# x = self.paths_to_illness_helper(illness, node.positive_child)
# y = self.paths_to_illness_helper(illness, node.negative_child)
#
# if x != None:
#     if x == []:
#         x = [[True]]
#     else:
#         for i in x:
#             i.insert(0, True)
# if y is not None:
#     if not y:
#         y = [[False]]
#     else:
#         for i in y:
#             i.insert(0, False)
#
# if x is None and y is None:
#     return []
# if y is None and x is not None:
#     return x
# if x == None and y != None:
#     return y
# else:
#     return x + y


def build_tree_helper(records, symptoms, index=0):
    if index == len(symptoms):
        illnesses = [record.illness for record in records]
        most_common = sorted(illnesses, key=illnesses.count, reverse=True)
        illness = most_common[0] if most_common else None
        return Node(illness, None, None)
    positive_records = [
        record for record in records if symptoms[index] in record.symptoms]
    negative_record = [
        record for record in records if record not in positive_records]
    positive_child = build_tree_helper(positive_records, symptoms, index + 1)
    negative_child = build_tree_helper(negative_record, symptoms, index + 1)
    node = Node(symptoms[index], positive_child, negative_child)
    return node


def build_tree(records, symptoms):
    return build_tree_helper(records, symptoms)


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
