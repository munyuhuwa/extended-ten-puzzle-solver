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

def printNodes(nodes):
	for node in nodes:
		print('value: %d,\ttex: %s,\tcost: %d' % (node.value, node.tex, node.cost,))

# 設定
COST_LIMIT = 20
VALUE_LIMIT = 1000
VALUE_NEG_LIMIT = -1000

# 探索用のデータ構造
nodeArray = np.zeros((VALUE_LIMIT-VALUE_NEG_LIMIT+1,), dtype=PuzzleNode)
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
nodeArray[(334-VALUE_NEG_LIMIT)] = node

def searchOnce(nodeArray, min_cost, max_cost):
	#後から追加したノードはその場では探索しない
	# arrayからnodeが存在する要素だけ抜き出す
	nodeListSortedByCost = sorted(list(nodeArray[np.nonzero(nodeArray)]), key=lambda node: node.cost)
	# print('---')
	# printNodes(nodeListSortedByCost)
	# print('/---')
	nNodes = len(nodeListSortedByCost)
	for i in range(nNodes):
		nodeI = nodeListSortedByCost[i]
		for j in range(i, nNodes):
			nodeJ = nodeListSortedByCost[j]
			# 第一引数と第二引数は、同じか第二引数のほうがより後ろの組み合わせだけ探索する
			for op in BINARY_OPERATION_LIST:
				# コストの計算・条件
				newCost = nodeI.cost + nodeJ.cost + op.cost
				if newCost < min_cost:
					continue
				if max_cost < newCost:
					break
				# 値の計算・条件
				try:
					newValue = op.func_op(nodeI.value, nodeJ.value)
				except:
					continue
				if newValue < VALUE_NEG_LIMIT:
					continue
				if VALUE_LIMIT < newValue:
					continue
				# すでに同じ値がある
				idx = newValue-VALUE_NEG_LIMIT
				if nodeArray[idx] != 0:
					continue
				# TeXの生成
				newTex = op.func_tex(nodeI.tex, nodeJ.tex)
				# nodeの生成
				newNode = PuzzleNode(newValue, newTex, newCost)
				nodeArray[idx] = newNode
				# printNodes([newNode,])
	return len(nodeListSortedByCost)# 実行前の個数

nNodeListAtLoop = []
for i in range(1, 9):
	cnt = searchOnce(nodeArray, i, COST_LIMIT)
	print('loop %d:\tfound %d' % (i, cnt,))
	nNodeListAtLoop.append(cnt)
finalNodeList = list(nodeArray[np.nonzero(nodeArray)])
nNodeListAtLoop.append(len(finalNodeList))

# 検索状況の出力
with open('./sandbox/log.txt', 'w', encoding='utf8') as f:
	for i in range(len(nNodeListAtLoop)):
		f.write('%d\t%d\n' % (i, nNodeListAtLoop[i]))
# TeXの出力
with open('./sandbox/log_tex.txt', 'w', encoding='utf8') as f:
	for node in finalNodeList:
		equation = '$$ %d = %s $$\n' % (node.value, node.tex,)
		f.write(equation)

# 画像出力サンプル
rnd_node = random.choice(finalNodeList)
sympy.init_printing()
equation = '$$ %d = %s $$' % (rnd_node.value, rnd_node.tex,)
# sympy.preview(equation, viewer='file', filename='./sandbox/sample.png', euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600", "-bg", "Transparent"])
sympy.preview(equation, viewer='file', filename='./sandbox/sample.png', euler=False, dvioptions=["-T", "tight", "-z", "0", "--truecolor", "-D 600",])
