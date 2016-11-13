# Tree('S', [Tree('N', ['I']), Tree('VP', [Tree('VP', [Tree('V', ['went']), Tree('ADV', ['yesterday'])]), Tree('PP', [Tree('PREP', ['to']), Tree('NP', [Tree('DET', ['the']), Tree('N', ['mall'])])])])])

from flask import Flask
from flask import request
from flask import render_template

from nltk.tree import Tree

from stat_parser import Parser
parser = Parser()

import language_check
tool = language_check.LanguageTool('en-US')

app = Flask(__name__)

# if __name__ == '__main__':
# 	app.run(host='0.0.0.0',port=5000,debug=False)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/', methods=['POST'])
def toboard():
	sent = request.form['field']
	tree = parser.parse(sent)
	tree.pretty_print()
	#tree = create_corpus(sent)
	#tree = fix_tree(tree)
	perms = permute_tree(tree)
	return trees_to_string(perms)

####################
# TREE STUFF #
####################

def trees_to_string(tree_lst):
	# lst is a list of Trees
	str_lst = []
	for t in tree_lst:
		string = ''
		for leaf in t.leaves():
			string += leaf + ' '
		string = string[0].upper() + string[1:]
		if len(tool.check(string)) == 0:
			str_lst.append(string)
		else:
			[print(match) for match in tool.check(string)]
			print('wrong! ' + string)
	final_str = ''
	for s in str_lst:
		final_str += (s + '<br>')
	return final_str

# def print_trees(lst):
# 	formatted = ''
# 	for tree in lst:
# 		for word in tree.leaves():
# 			formatted += word + ' '
# 		formatted = formatted[:-1] # remove last space
# 		formatted += '.<br>'
# 	return formatted

def permute_tree(t):
	if type(t) != Tree:
		return [t]
	if is_leaf(t):
		return [Tree(t.label(), list(t))]
	# elif all([all([is_leaf(r) for r in list(s)]) for s in list(t)]):
	# 	return [Tree(t.label(), list(t))]
	else:
		subperms = permute([permute_tree(s) for s in list(t)])
		subtree_permutations = []
		for subperm in subperms:
			subtree_permutations.extend(permute_lists(subperm))
		return [Tree(t.label(), s) for s in subtree_permutations]

def is_leaf(t):
	return len(t) == 0 or not type(t[0])==Tree

def permute_lists(lst):
	if len(lst) == 1:
		return [[elem] for elem in lst[0]]
	all_perms = []
	for elem in lst[0]:
		all_perms.extend([[elem] + perm for perm in permute_lists(lst[1:])])
	return all_perms

def permute(lst):
	if not lst:
		return [[]]
	else:
		ret = []
		for i in range(len(lst)):
			ret.extend([[lst[i]] + rst for rst in permute(lst[0:i] + lst[i+1:])])
	return ret
