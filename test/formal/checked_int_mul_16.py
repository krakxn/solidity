from opcodes import AND, SDIV, SGT, SLT, MUL, EQ, ISZERO, NOT, OR
from rule import Rule
from util import BVSignedMax, BVSignedMin, BVSignedUpCast
from z3 import BVMulNoOverflow, BVMulNoUnderflow, BitVec, BitVecVal, Not, Or

"""
Overflow checked signed integer multiplication.
"""

# Approximation with 16-bit base types.
n_bits = 16

for type_bits in [4, 8, 12, 16]:

	rule = Rule()

	# Input vars
	X_short = BitVec('X', type_bits)
	Y_short = BitVec('Y', type_bits)

	# Z3's overflow and underflow conditions
	actual_overflow = Not(BVMulNoOverflow(X_short, Y_short, True))
	actual_underflow = Not(BVMulNoUnderflow(X_short, Y_short))

	# cast to full n_bits values
	X = BVSignedUpCast(X_short, n_bits)
	Y = BVSignedUpCast(Y_short, n_bits)
	product = MUL(X, Y)

	# Constants
	bitMask = (BitVecVal(1, n_bits) << type_bits) - 1
	signMask = BitVecVal(1, n_bits) << type_bits - 1

	# Overflow and underflow checks in YulUtilFunction::overflowCheckedIntMulFunction
	overflow_check_1 = AND(
		ISZERO(AND(product, signMask)),
		AND(ISZERO(ISZERO(X)), ISZERO(EQ(Y, SDIV(AND(product, bitMask), X))))
	)
	overflow_check_2 = AND(
		ISZERO(ISZERO(AND(product, signMask))),
		AND(ISZERO(ISZERO(X)), ISZERO(EQ(Y, SDIV(OR(product, NOT(bitMask)), X))))
	)
	underflow_check_1 = overflow_check_1
	underflow_check_2 = overflow_check_2

	rule.check(actual_overflow, Or(overflow_check_1 != 0, overflow_check_2 != 0))
	rule.check(actual_underflow, Or(underflow_check_1 != 0, underflow_check_2 != 0))
