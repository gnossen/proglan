import os
from ..lexer.lexeme import *
from ..parser.parser import *
import time
import sys

class Environment:
    def __init__(self, input=None, file=None):
        self.env = self.create_env()
        if input is not None:
            self.load_str(input)
        elif file is not None:
            self.load_file(file)
        else:
            self.input = None
    
    def load_file(self, filename):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        filepath = os.path.join(cur_dir, filename)
        with open(filepath, 'r') as f:
            self.input = f.read()

    def load_str(self, str):
        self.input = str

    def extend_env(self, var_names, vals, definingEnv):
        join2 = Lexeme(Lexeme.gen_purp, left=definingEnv)
        join1 = Lexeme(Lexeme.gen_purp, left=vals, right=join2)
        return Lexeme(Lexeme.env, left=var_names, right=join1)

    def create_env(self):
        env = self.extend_env(None, None, None)
        self.insert(Lexeme(Lexeme.IDENTIFIER, value="print"),
                    Lexeme(Lexeme.builtIn, left=self.printFunc),
                    env)
        self.insert(Lexeme(Lexeme.IDENTIFIER, value="println"),
                    Lexeme(Lexeme.builtIn, left=self.printlnFunc),
                    env)
        self.insert(Lexeme(Lexeme.IDENTIFIER, value="append"),
                    Lexeme(Lexeme.builtIn, left=self.array_append),
                    env)
        self.insert(Lexeme(Lexeme.IDENTIFIER, value="len"),
                    Lexeme(Lexeme.builtIn, left=self.len_func),
                    env)

        return env

    def insert(self, identifier, val, env):
        ids = env.left
        vals = env.right.left

        id_join = Lexeme(Lexeme.gen_purp, left=ids, right=identifier)
        val_join = Lexeme(Lexeme.gen_purp, left=vals, right=val)

        env.left = id_join
        env.right.left = val_join

    def assign(self, identifier, val, env):
        ids = env.left
        vals = env.right.left
        defining_env = env.right.right.left

        while ids is not None:
            cur_id = ids.right
            if identifier.value == cur_id.value:
                vals.right = val
                return val

            ids = ids.left
            vals = vals.left

        if defining_env is not None:
            return self.assign(identifier, val, defining_env)
        else:
            raise Exception("Attempted to assign to undefined variable %s." % identifier)

    def lookup(self, identifier, env):
        ids = env.left
        vals = env.right.left
        defining_env = env.right.right.left

        while ids is not None:
            cur_id = ids.right
            cur_val = vals.right
            if identifier.value == cur_id.value:
                return cur_val

            ids = ids.left
            vals = vals.left
        else:
            if defining_env is not None:
                return self.lookup(identifier, defining_env)

            raise Exception("Undefined variable %s." % identifier)

    def varDefined(self, identifier, env):
        ids = env.left

        while ids is not None:
            if identifier.value == ids.right.value:
                return True

            ids = ids.left
            
        return False

    def printlnFunc(self, arg_tree, env):
        res = self.printFunc(arg_tree, env)
        sys.stdout.write("\n")
        return res

    def printFunc(self, arg_tree, env):
        if arg_tree is None:
            return Lexeme(Lexeme.NULL)

        car = arg_tree.left
        cdr = arg_tree.right

        sys.stdout.write(self.pretty_print(car, env))
        return self.printFunc(cdr, env)

    def array_append(self, args, env):
        if args is None:
            raise Exception("No argument to append.")

        car = args.left
        cdr = args.right

        if cdr is None or cdr.left is None:
            raise Exception("Must supply element to be appended.")

        arr = self.eval(car, env)
        val = self.eval(cdr.left, env)

        if arr.type != Lexeme.array:
            raise Exception("Attempted to append to non-array.")

        arr.value.append(val)
        return val

    def len_func(self, args, env):
        if args is None:
            raise Exception("No arguments to len.")

        car = args.left
        cdr = args.right
        
        if cdr is not None:
            raise Exception("Too many arguments to len.")
        
        val = self.eval(args.left, env)
        if val.type == Lexeme.STRING or val.type == Lexeme.array:
            return Lexeme(Lexeme.NUMBER, value=len(val.value))

    def pretty_print(self, arg, env):
        val = self.eval(arg, env)
        if val.type == Lexeme.NUMBER:
            return str(val.value)
        elif val.type == Lexeme.STRING:
            return val.value
        elif val.type == Lexeme.BOOL:
            if val.value == True:
                return "true"
            else:
                return "false"
        elif val.type == Lexeme.NULL:
            return "null"
        elif val.type == Lexeme.array:
            s = "["
            for i, elem in enumerate(val.value):
                s += self.pretty_print(elem, env)
                if i != len(val.value) - 1:
                    s += ", "

            s += "]"
            return s
        else:
            return str(val)

    def evaluate(self):
        root = Parser(input=self.input).parse()
        return self.eval(root, self.env)

    def eval(self, pt, env):
        primitives = [Lexeme.NUMBER, Lexeme.STRING, Lexeme.BOOL, Lexeme.array]
        if pt.type in primitives:
            return pt
        elif pt.type == Lexeme.exprList:
            return self.evalExprList(pt, env)
        elif pt.type == Lexeme.primExpr:
            return self.evalPrimExpr(pt, env)
        elif pt.type == Lexeme.varDecl:
            return self.evalVarDecl(pt, env)
        elif pt.type == Lexeme.varAssign:
            return self.evalVarAssign(pt, env)
        elif pt.type == Lexeme.IDENTIFIER:
            return self.lookup(pt, env)
        elif pt.type == Lexeme.ifExpr:
            return self.evalIfExpr(pt, env)
        elif pt.type == Lexeme.whileExpr:
            return self.evalWhileExpr(pt, env)
        elif pt.type == Lexeme.funcDef:
            return self.evalFuncDef(pt, env)
        elif pt.type == Lexeme.anonFunc:
            return self.evalAnonFunc(pt, env)
        elif pt.type == Lexeme.funcCall:
            return self.evalFuncCall(pt, env)
        elif pt.type == Lexeme.arrayLiteral:
            return self.evalArrayLiteral(pt, env)
        elif pt.type == Lexeme.arrayAccess:
            return self.evalArrayAccess(pt, env)
        elif pt.type == Lexeme.returnExpr:
            return make_returnExpr(self.eval(pt.left, env))
        else:
            raise Exception("Cannot evaluate %s" % str(pt))

    def evalExprList(self, pt, env):
        if pt.right is None:
            return self.eval(pt.left, env)
        else:
            cur = self.eval(pt.left, env)
            if cur.type == Lexeme.returnExpr:
                return cur

            return self.eval(pt.right, env)

    def evalVarDecl(self, pt, env):
        if self.varDefined(pt.left, env):
            raise Exception("Variable %s already declared." % str(pt.left))

        right = self.eval(pt.right, env)
        self.insert(pt.left, right, env)
        return right

    def evalVarAssign(self, pt, env):
        new_val = right = self.eval(pt.right, env)
        lval = pt.left
        if lval.type == Lexeme.arrayAccess:
            arr = self.eval(lval.left, env)
            index = self.eval(lval.right, env)
            arr.value[index.value] = new_val
        elif lval.type == Lexeme.IDENTIFIER:
            self.assign(lval, new_val, env)
        else:
            raise Exception("Attempted to use %s as lvalue in assignment." % pt)

        return right

    def evalPrimExpr(self, pt, env):
        left = self.eval(pt.left, env)
        op = pt.right.left
        right = self.eval(pt.right.right, env)
        if op.type == Lexeme.PLUS:
            return self.evalPlus(left, op, right, env)
        elif op.type == Lexeme.MINUS:
            return self.evalMinus(left, op, right, env)
        elif op.type == Lexeme.TIMES:
            return self.evalTimes(left, op, right, env)
        elif op.type == Lexeme.DIVIDE:
            return self.evalDivide(left, op, right, env)
        elif op.type == Lexeme.DOUBLE_EQUAL:
            return self.evalDoubleEqual(left, op, right, env)
        elif op.type == Lexeme.GREATER_THAN:
            return self.evalGreaterThan(left, op, right, env)
        elif op.type == Lexeme.LESS_THAN:
            return self.evalLessThan(left, op, right, env)
        elif op.type == Lexeme.AND:
            return self.evalAnd(left, op, right, env)
        elif op.type == Lexeme.OR:
            return self.evalOr(left, op, right, env)
        elif op.type == Lexeme.XOR:
            return self.evalXor(left, op, right, env)
        elif op.type == Lexeme.BITWISE_AND:
            return self.evalBitwiseAnd(left, op, right, env)
        elif op.type == Lexeme.BITWISE_OR:
            return self.evalBitwiseOr(left, op, right, env)
        elif op.type == Lexeme.BITWISE_XOR:
            return self.evalBitwiseXor(left, op, right, env)
        elif op.type == Lexeme.LEQ:
            return self.evalLeq(left, op, right, env)
        elif op.type == Lexeme.GEQ:
            return self.evalGeq(left, op, right, env)
        elif op.type == Lexeme.NEQ:
            return self.evalNeq(left, op, right, env)

        raise Exception("Unrecognized binary operator %s" % op)

    def binOpError(self, left, op, right):
        raise Exception("Attempted %s + %s. (%s)" % (left, right, op))

    def evalPlus(self, left, op, right, env):
        if left.type == Lexeme.NUMBER:
            if right.type == Lexeme.NUMBER:
                return Lexeme(Lexeme.NUMBER, value=(left.value + right.value))
        elif left.type == Lexeme.STRING:
            if right.type == Lexeme.STRING:
                return Lexeme(Lexeme.STRING, value=(left.value + right.value))
            elif right.type == Lexeme.NUMBER:
                return Lexeme(Lexeme.STRING, value=(left.value + str(right.value)))
            elif right.type == Lexeme.BOOL:
                return Lexeme(Lexeme.STRING, value=(left.value + str(right.value)))
        
        self.binOpError(left, op, right)

    def evalMinus(self, left, op, right, env):
        if left.type == Lexeme.NUMBER:
            if right.type == Lexeme.NUMBER:
                return Lexeme(Lexeme.NUMBER, value=(left.value - right.value))

        self.binOpError(left, op, right)

    def evalTimes(self, left, op, right, env):
        if left.type == Lexeme.NUMBER:
            if right.type == Lexeme.NUMBER:
                return Lexeme(Lexeme.NUMBER, value=(left.value * right.value))
        
        self.binOpError(left, op, right)


    def evalDivide(self, left, op, right, env):
        if left.type == Lexeme.NUMBER:
            if right.type == Lexeme.NUMBER:
                return Lexeme(Lexeme.NUMBER, value=(left.value / right.value))
        
        self.binOpError(left, op, right)

    def evalDoubleEqual(self, left, op, right, env):
        if left.type != right.type:
            return Lexeme(Lexeme.BOOL, value=False)

        if left.value != right.value:
            return Lexeme(Lexeme.BOOL, value=False)
        
        return Lexeme(Lexeme.BOOL, value=True)

    def evalGreaterThan(self, left, op, right, env):
        if left.type != Lexeme.NUMBER:
            raise Exception("%s not comparable" % str(left))

        if right.type != Lexeme.NUMBER:
            raise Exception("%s not comparable" % str(right))

        if left.value > right.value:
            return Lexeme(Lexeme.BOOL, value=True)
        else:
            return Lexeme(Lexeme.BOOL, value=False)

    def evalLessThan(self, left, op, right, env):
        if left.type != Lexeme.NUMBER:
            raise Exception("%s not comparable" % str(left))

        if right.type != Lexeme.NUMBER:
            raise Exception("%s not comparable" % str(right))

        if left.value < right.value:
            return Lexeme(Lexeme.BOOL, value=True)
        else:
            return Lexeme(Lexeme.BOOL, value=False)

    def coerceBool(self, pt):
        if pt.type == Lexeme.BOOL:
            return pt

        if pt.type == Lexeme.NUMBER:
            if pt.value == 0:
                return Lexeme(Lexeme.BOOL, value=False)
            else:
                return Lexeme(Lexeme.BOOL, value=True)
    
        if pt.type == Lexeme.STRING:
            if pt.value == "":
                return Lexeme(Lexeme.BOOL, value=False)
            else:
                return Lexeme(Lexeme.BOOL, value=True)

        if pt.type == Lexeme.NULL:
            return Lexeme(Lexeme.BOOL, value=False)
        
        return Lexeme(Lexeme.BOOL, value=True)


    def evalAnd(self, left, op, right, env):
        left = self.coerceBool(left)
        right = self.coerceBool(right)

        if left.value == True and right.value == True:
            return Lexeme(Lexeme.BOOL, value=True)
        else:
            return Lexeme(Lexeme.BOOL, value=False)

    def evalOr(self, left, op, right, env):
        left = self.coerceBool(left)
        right = self.coerceBool(right)

        if left.value == True or right.value == True:
            return Lexeme(Lexeme.BOOL, value=True)
        else:
            return Lexeme(Lexeme.BOOL, value=False)

    def evalXor(self, left, op, right, env):
        left = self.coerceBool(left)
        right = self.coerceBool(right)

        if left.value != right.value:
            return Lexeme(Lexeme.BOOL, value=True)
        else:
            return Lexeme(Lexeme.BOOL, value=False)

    def evalBitwiseAnd(self, left, op, right, env):
        if left.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(left))

        if right.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(right))

        return Lexeme(Lexeme.NUMBER, value=(left.value & right.value))

    def evalBitwiseOr(self, left, op, right, env):
        if left.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(left))

        if right.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(right))

        return Lexeme(Lexeme.NUMBER, value=(left.value | right.value))

    def evalBitwiseXor(self, left, op, right, env):
        if left.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(left))

        if right.type != Lexeme.NUMBER:
            raise Exception("Cannot perform bit operations on %s" % str(right))

        return Lexeme(Lexeme.NUMBER, value=(left.value ^ right.value))

    def evalLeq(self, left, op, right, env):
        less_than = self.evalLessThan(left, op, right, env)
        equal = self.evalDoubleEqual(left, op, right, env)

        if less_than.value == True or equal.value == True:
            return Lexeme(Lexeme.BOOL, value=True)

    def evalGeq(self, left, op, right, env):
        greater_than = self.evalGreaterThan(left, op, right, env)
        equal = self.evalDoubleEqual(left, op, right, env)

        if greater_than.value == True or equal.value == True:
            return Lexeme(Lexeme.BOOL, value=True)

    def evalNeq(self, left, op, right, env):
        equal = self.evalDoubleEqual(left, op, right, env)

        if equal.value == True:
            return Lexeme(Lexeme.BOOL, value=False)
        else:
            return Lexeme(Lexeme.BOOL, value=True)

    def evalIfExpr(self, pt, env):
        cond = self.coerceBool(self.eval(pt.left, env))
        body = pt.right.left
        else_expr = pt.right.right

        if cond.value == True:
            return self.eval(body, env)
        elif else_expr is not None:
            return self.evalElseExpr(else_expr, env)
        else:
            return Lexeme(Lexeme.NULL)

    def evalElseExpr(self, pt, env):
        body = pt.left
        if_expr = pt.right

        if if_expr is not None:
            return self.evalIfExpr(if_expr, env)
        else:
            return self.eval(body, env)

    def evalWhileExpr(self, pt, env):
        cond_expr = pt.left
        body = pt.right

        res = Lexeme(Lexeme.NULL)
        while self.coerceBool(self.eval(cond_expr, env)).value == True:
            new_env = self.extend_env(None, None, env)
            res = self.eval(body, new_env)
            if res.type == Lexeme.returnExpr:
                return res

        return res

    def evalFuncDef(self, pt, env):
        name = pt.left
        param_list = pt.right.left
        func_param = pt.right.right.left
        body = pt.right.right.right

        func = self.make_function(param_list, func_param, body, env)
        self.insert(name, func, env)
        return func

    def evalFuncCall(self, pt, env):
        func = self.eval(pt.left, env)
        
        if func.type == Lexeme.builtIn:
            return func.left(pt.right.left, env)

        if func.type != Lexeme.function:
            raise Exception("Attempted to call non-function %s." % str(func))

        param_list = func.left
        arg_list = pt.right.left
        defining_env = func.right.right.right
        new_env = self.extend_env(None, None, defining_env)
        while param_list is not None:
            if arg_list is None:
                raise Exception("Not enough arguments supplied to %s" % str(pt))

            param = param_list.left
            arg = self.eval(arg_list.left, env)

            self.insert(param, arg, new_env)
            param_list = param_list.right
            arg_list = arg_list.right

        if arg_list is not None:
            raise Exception("Too many arguments supplied to %s" % str(pt))

        func_param = func.right.left
        func_arg = pt.right.right
        if func_param is not None:
            if func_arg is None:
                raise Exception("No function parameter supplied to %s" % str(pt))
            
            func_name = func_param.left
            func_param_params = func_param.right
            arg_func = self.make_function(func_param_params, None, func_arg, env)
            self.insert(func_name, arg_func, new_env)

        body = func.right.right.left
        res = self.eval(body, new_env)

        if res.type == Lexeme.returnExpr:
            return res.left

        return res

    def evalArrayLiteral(self, pt, env):
        arr = []
        elems = pt.left
        while elems is not None:
            arr.append(self.eval(elems.left, env))
            elems = elems.right

        return Lexeme(Lexeme.array, value=arr)

    def evalArrayAccess(self, pt, env):
        arr = self.eval(pt.left, env)
        index = self.eval(pt.right, env)

        if arr.type != Lexeme.array:
            raise Exception("Attempted to index non-array %s." % arr)

        if index.type != Lexeme.NUMBER:
            raise Exception("Attempted to index array with non-number %s." % index)

        if index.value < 0 or index.value >= len(arr.value):
            raise Exception("Array index out of bounds %s." % index)

        return arr.value[index.value]

    def evalAnonFunc(self, pt, env):
        params = pt.left
        func_param = pt.right.left
        body = pt.right.right
        return self.make_function(params, func_param, body, env) 

    def make_function(self, param_list, func_param, body, env):
        join2 = Lexeme(Lexeme.gen_purp, left=body, right=env)
        join = Lexeme(Lexeme.gen_purp, left=func_param, right=join2)
        return Lexeme(Lexeme.function, left=param_list, right=join)
    
