# -*- coding: utf8 -*-
import numpy as np
import sympy
import random

# テンパズルの数式を探索するためのノード
class PuzzleNode:
	def __init__(self, value, tex, cost):
		self.value = value # 計算結果
		self.tex = tex # 数式のtex
		self.cost = cost # 数式の複雑度

# 設定
COST_LIMIT = 20
VALUE_LIMIT = 1000000
VALUE_NEG_LIMIT = -1000000

# 探索用のデータ構造
nodesSortedByCost = list()
nodesWithIndexValue = np.zeros((VALUE_LIMIT-VALUE_NEG_LIMIT+1,), dtype=PuzzleNode)
# インデックスはVALUE_NEG_LIMITだけずらして考える

# 探索は計算結果が整数であるような範囲で行う

# 演算子のリスト
class BinaryOperation:
	def __init__(self, func_op, func_tex, cost):
		self.func_op = func_op
		self.func_tex = func_tex
		self.cost = cost

BINARY_OPERATION_LIST = [
	BinaryOperation(lambda a, b: a+b,		lambda a, b: '(%s + %s)' % (a, b,),		1),
	BinaryOperation(lambda a, b: a-b,		lambda a, b: '(%s - %s)' % (a, b,),		1),
	BinaryOperation(lambda a, b: b-a,		lambda a, b: '(%s - %s)' % (b, a,),		1),
	BinaryOperation(lambda a, b: a*b,		lambda a, b: '(%s \\times %s)' % (a, b,),	1),
	BinaryOperation(lambda a, b: int(a/b),	lambda a, b: '(\lfloor %s / %s \\rfloor)' % (a, b,),		2),
	BinaryOperation(lambda a, b: int(b/a),	lambda a, b: '(\lfloor %s / %s \\rfloor)' % (b, a,),		2),
	# BinaryOperation(lambda a, b: a%b,		lambda a, b: '(%s \\bmod %s)' % (a, b),	1),
	# BinaryOperation(lambda a, b: b%a,		lambda a, b: '(%s \\bmod %s)' % (b, a),	1)
]

# 探索用配列の初期化
node = PuzzleNode(334, '334', 0)
nodesSortedByCost.append(node)
nodesWithIndexValue[(334-VALUE_NEG_LIMIT)] = node

def searchOnce(nodesSortedByCost, nodesWithIndexValue, min_cost, max_cost):
	#後から追加したノードはその場では探索しない
	nNodes = len(nodesSortedByCost)
	nodesSortedByCostExtra = list()
	for i in range(nNodes):
		nodeI = nodesSortedByCost[i]
		for j in range(i, nNodes):
			nodeJ = nodesSortedByCost[j]
			# 第一引数と第二引数は、同じか第二引数のほうがより後ろの組み合わせだけ探索する
			for op in BINARY_OPERATION_LIST:
				cost_sum = nodeI.cost + nodeJ.cost + op.cost
				if cost_sum < min_cost:
					continue
				if max_cost < cost_sum:
					break
				try:
					value = op.func_op(nodeI.value, nodeJ.value)
				except:
					continue
				if value < VALUE_NEG_LIMIT:
					continue
				if VALUE_LIMIT < value:
					continue
				if nodesWithIndexValue[value-VALUE_NEG_LIMIT] != 0:
					continue
				tex = op.func_tex(nodeI.tex, nodeJ.tex)
				newNode = PuzzleNode(value, tex, cost_sum)
				nodesSortedByCostExtra.append(newNode)
				nodesWithIndexValue[value-VALUE_NEG_LIMIT] = newNode
	nodesSortedByCost += nodesSortedByCostExtra
	nodesSortedByCost.sort(key=lambda x: x.cost) # コストのソートは追加分だけに削減できるかも


for i in range(1, 5):
	searchOnce(nodesSortedByCost, nodesWithIndexValue, i, COST_LIMIT)

def printNodes(nodes):
	for node in nodes:
		print('value: %d,\ttex: %s,\tcost: %d' % (node.value, node.tex, node.cost,))

# print(nodesSortedByCost)
# print(nodesSortedByValue)
# printNodes(nodesSortedByValue)
nodes = [node for node in list(nodesWithIndexValue) if node != 0]
# printNodes(nodes)
# print(len(nodes))
rnd_node = random.choice(nodes)
sympy.init_printing()
equation = '$$ %d = %s $$' % (rnd_node.value, rnd_node.tex,)
# sympy.preview(equation, viewer='file', filename='./sandbox/sample.png', euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
sympy.preview(equation, viewer='file', filename='./sandbox/sample.png', euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600",])