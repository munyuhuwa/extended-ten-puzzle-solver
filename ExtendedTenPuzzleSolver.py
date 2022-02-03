# -*- coding: utf8 -*-
import numpy as np


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
# nodesSortedByValue = list()
nodesWithIndexValue = np.zeros((VALUE_LIMIT-VALUE_NEG_LIMIT+1,), dtype=PuzzleNode)
# インデックスはVALUE_NEG_LIMITだけずらして考える

# 探索は計算結果が整数であるような範囲で行う

# 演算
# 2項演算
# def op_add(a, b):
# 	return (a + b)
# def op_sub(a, b):
# 	return (a - b)
# def op_sub_rev(a, b):
# 	return (b - a)
# def op_mul(a, b):
# 	return (a * b)
# def op_div_floor(a, b):
# 	return int(a / b)
# def op_div_rev_floor(a, b):
# 	return int(b / a)
# def tex_add(a, b):
# 	return str(a) + ' + ' + str(b)

# 演算子のリスト
class BinaryOperation:
	def __init__(self, func_op, func_tex, cost):
		self.func_op = func_op
		self.func_tex = func_tex
		self.cost = cost

BINARY_OPERATION_LIST = [
	BinaryOperation(lambda a, b: a+b,		lambda a, b: '(%s + %s)' % (a, b,),		1),
	BinaryOperation(lambda a, b: a-b,		lambda a, b: '(%s - %s)' % (a, b,),		1),
	BinaryOperation(lambda a, b: a*b,		lambda a, b: '(%s \\times %s)' % (a, b,),	1),
	BinaryOperation(lambda a, b: int(a/b),	lambda a, b: '(\lfloor %s / %s \\rfloor)' % (a, b,),		2),
]

# 探索用配列の初期化
node = PuzzleNode(334, '334', 0)
nodesSortedByCost.append(node)
# nodesSortedByValue.append(node)
nodesWithIndexValue[(334-VALUE_NEG_LIMIT)] = node

# def searchOnce(nodesSortedByCost, nodesSortedByValue, min_cost, max_cost):
def searchOnce(nodesSortedByCost, nodesWithIndexValue, min_cost, max_cost):
	#後から追加したノードはその場では探索しない
	nNodes = len(nodesSortedByCost)
	nodesSortedByCostExtra = list()
	# nodesSortedByValueExtra = list()
	for i in range(nNodes):
		nodeI = nodesSortedByCost[i]
		for j in range(i, nNodes):
			nodeJ = nodesSortedByCost[j]
			# 第一引数と第二引数は、同じか第二引数のほうがより後ろの組み合わせだけ探索する
			# print(nodeI)
			# print(nodeJ)
			for op in BINARY_OPERATION_LIST:
				# print(op)
				cost_sum = nodeI.cost + nodeJ.cost + op.cost
				# print(cost_sum)
				if cost_sum < min_cost:
					# print('NG1')
					continue
				if max_cost < cost_sum:
					# print('NG2')
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
				# hasSameValue = False
				# for node in nodesSortedByValue:
				# 	if node.value <= value:
				# 		if node.value == value:
				# 			hasSameValue = True
				# 		break
				# if hasSameValue:
				# 	continue
				# for node in nodesSortedByValueExtra:
				# 	if node.value == value:
				# 		hasSameValue = True
				# 		break
				# if hasSameValue:
				# 	continue
				# 同じ値のチェックは時間がかかるので、全部終わった後に重複を削除する形のほうが良いかも
				tex = op.func_tex(nodeI.tex, nodeJ.tex)
				newNode = PuzzleNode(value, tex, cost_sum)
				nodesSortedByCostExtra.append(newNode)
				# nodesSortedByValueExtra.append(newNode)
				nodesWithIndexValue[value-VALUE_NEG_LIMIT] = newNode
	nodesSortedByCost += nodesSortedByCostExtra
	nodesSortedByCost.sort(key=lambda x: x.cost) # コストのソートは追加分だけに削減できるかも
	# nodesSortedByValue += nodesSortedByValueExtra
	# nodesSortedByValue.sort(key=lambda x: x.value)

	# print(nodesSortedByCost)
	# print(nodesSortedByValue)

# searchOnce(nodesSortedByCost, nodesSortedByValue, 0, COST_LIMIT)# 計算後の最小コストは1
# searchOnce(nodesSortedByCost, nodesSortedByValue, 2, COST_LIMIT)# 計算後の最小コストは1+0+1=2
# searchOnce(nodesSortedByCost, nodesWithIndexValue, 1, COST_LIMIT)# 計算後の最小コストは1
# searchOnce(nodesSortedByCost, nodesWithIndexValue, 2, COST_LIMIT)# 計算後の最小コストは1+0+1=2
# searchOnce(nodesSortedByCost, nodesWithIndexValue, 3, COST_LIMIT)# 計算後の最小コストは1+0+2=3
# searchOnce(nodesSortedByCost, nodesWithIndexValue, 4, COST_LIMIT)# 計算後の最小コストは1+0+3=4
for i in range(1, 6):
	searchOnce(nodesSortedByCost, nodesWithIndexValue, i, COST_LIMIT)

def printNodes(nodes):
	for node in nodes:
		print('value: %d,\ttex: %s,\tcost: %d' % (node.value, node.tex, node.cost,))

# print(nodesSortedByCost)
# print(nodesSortedByValue)
# printNodes(nodesSortedByValue)
nodes = [node for node in list(nodesWithIndexValue) if node != 0]
# printNodes(nodes)
print(len(nodes))