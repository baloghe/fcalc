from .polform import symlist_to_string, to_polish_form, eval_fn, eval_inop, eval_polish_form

class MalformedExpression(Exception):
    pass

class Calculator:

    maxopnum = 20     # max number of operators
    
    state = {}        # state
    symlist = []      # symbols as typed by the user
    brackets = []     # separate stack to ensure proper bracketing
    opcount = 0       # number of operators in stack
    
    
    """resets calculator and populates helper variables
    k: key, p: precedence, s: symbol, t: type, v: value
    within type: dig: digit, inop: inorder operator, fn: function, number: a specific value
    """
    symbols = {
         "B0": {"k":"B0","p":0,"s":"0","t":"dig"}
        ,"B1": {"k":"B1","p":0,"s":"1","t":"dig"}
        ,"B2": {"k":"B2","p":0,"s":"2","t":"dig"}
        ,"B3": {"k":"B3","p":0,"s":"3","t":"dig"}
        ,"B4": {"k":"B4","p":0,"s":"4","t":"dig"}
        ,"B5": {"k":"B5","p":0,"s":"5","t":"dig"}
        ,"B6": {"k":"B6","p":0,"s":"6","t":"dig"}
        ,"B7": {"k":"B7","p":0,"s":"7","t":"dig"}
        ,"B8": {"k":"B8","p":0,"s":"8","t":"dig"}
        ,"B9": {"k":"B9","p":0,"s":"9","t":"dig"}
        ,"OB": {"k":"OB","p":3,"s":"(","t":"bracket"}
        ,"CB": {"k":"CB","p":3,"s":")","t":"bracket"}
        ,"MU": {"k":"MU","p":2,"s":"*","t":"inop"}
        ,"DI": {"k":"DI","p":2,"s":"/","t":"inop"}
        ,"PL": {"k":"PL","p":1,"s":"+","t":"inop"}
        ,"MI": {"k":"MI","p":1,"s":"-","t":"inop"}
        ,"PO": {"k":"PO","p":4,"s":"^","t":"inop"}
        ,"LN": {"k":"LN","p":4,"s":"LN","t":"fn"}
        ,"SQ": {"k":"SQ","p":4,"s":"&sqrt;","t":"fn"}
        ,"DC": {"k":"DC","p":0,"s":".","t":"dig"}
        ,"NUMBER": {"k":"NUMBER","p":0,"s":"","t":"number"}
        ,"EQU": {"k":"EQU","p":10,"s":"=","t":"equ"}
    }
    
    # further helpers
    all_inops_fns = []
    all_digs = []
    all_ops = []
    all_fns = []
    
    def reset(self):
        """resets calculator state and everything
        """
        self.symlist = []
        self.brackets = []
        self.opcount = 0
        self.dccount = 0
        
        self.state = {
             "B0": True, "B1": True, "B2": True
            ,"B3": True, "B4": True, "B5": True
            ,"B6": True, "B7": True, "B8": True
            ,"B9": True
            ,"OB": True, "CB": False
            ,"MU": False, "DI": False, "PL": False, "MI": False
            ,"PO": False, "LN": True, "SQ": True, "DC": True
            ,"EQU": False
            ,"RESULT": ""
            ,"EXPRESSION": ""
            ,"STATE": "type something!"
        }
    
    def __init__(self):
        """resets calculator and populates helper variables
        """
        
        self.reset()
    
        for x in self.symbols.keys():
            if (self.symbols[x]["t"] == "inop" and x != "MI") or self.symbols[x]["t"] == "fn":
                self.all_inops_fns.append(x)
            if self.symbols[x]["t"] == "dig":
                self.all_digs.append(x)
            if self.symbols[x]["t"] == "inop":
                self.all_ops.append(x)
            if self.symbols[x]["t"] == "fn":
                self.all_fns.append(x)

    def enable_symbol(self, symarr):
        """enables buttons in list
        """
        for s in symarr:
            self.state[s] = True
        
    def disable_symbol(self, symarr):
        """disables buttons in list
        """
        for s in symarr:
            self.state[s] = False
            
    def handle_brackets(self, sym):
        """keeps track of balanced bracketing
        """
        if len(self.brackets) > 0 and    self.brackets[-1] == "OB" and sym == "CB":
            self.brackets.pop()
            # print(f"brackets: top OB removed -> len={len(brackets)}")
        else:
            self.brackets.append(sym)
            # print(f"brackets: append {sym} -> len={len(brackets)}")
        
    def get_symbol(self, sym):
        """copies a symbols from symbols
        """
        return { "k":self.symbols[sym]["k"]
                ,"p":self.symbols[sym]["p"]
                ,"s":self.symbols[sym]["s"]
                ,"t":self.symbols[sym]["t"]
        }

    def calc_state(self):
        """calculates button states
        """
        
        # empty stack
        if len(self.symlist) == 0:
            self.enable_symbol(["OB","SQ","LN","MI"] + self.all_digs)
            self.disable_symbol(["CB"] + self.all_ops)
            # print("    calc_state: stack is empty")
            return
            
        # max number of operators reached => disable further operators, functions and opening brackets
        if self.opcount >= self.maxopnum:
            self.disable_symbol(["OB","MI"] + self.all_inops_fns)
            self.enable_symbol(["CB"] + self.all_digs)
        else: # at least one element in stack
            last = self.symlist[-1]
            tpt = last["t"]
            tpk = last["k"]
            if tpt == "number":
                # enable operators + functions + closing bracket
                self.enable_symbol(["CB","EQU"] + self.all_ops + self.all_fns)
                self.disable_symbol(["OB"])
            elif tpt == "fn" or tpt == "inop":
                self.enable_symbol(["OB","EQU"] + self.all_digs + self.all_fns)
                self.disable_symbol(["CB"] + self.all_ops)
            elif tpk == "CB":
                # no immediate opening bracket or number may follow
                self.disable_symbol(["OB","EQU"] + self.all_digs)
                self.enable_symbol(["CB"] + self.all_ops + self.all_fns)
            elif tpk == "OB":
                # all symbols enabled except for closing bracket
                self.enable_symbol(["OB","EQU"] + self.all_ops + self.all_fns + self.all_digs)
                self.disable_symbol(["OB"])

    def add_symbol(self, sym, numliteral):
        """add a symbol (+ eventual number) to the current expression
        The expression gets evaluated (if possible), buttons leading to a malformed expression get disabled
        """
        
        print(f"addsymbol: {sym}:p{self.symbols[sym]['p']}, lit: {numliteral}")
        
        # tolerate (and correct) some malformed expressions
        # handle NUM+SYM combination
        append_sym = True
        if sym != "NUMBER" and numliteral != "" and self.symbols[sym]["t"] == "fn" and self.state["RESULT"] == "":
            # we assume <fn>(<numliteral>)
            self.symlist.append(self.get_symbol( sym ))
            nn = self.get_symbol( 'NUMBER' )
            nn['s'] = numliteral
            self.symlist.append( nn )
            append_sym = False
            print(f"add_symbol spec #1 : {symlist_to_string(self.symlist)}")
        elif sym != "NUMBER" and numliteral != "" and self.symbols[sym]["t"] == "inop" and self.state["RESULT"] == "":
            # we assume <numliteral> <inop>
            nn = self.get_symbol( 'NUMBER' )
            nn['s'] = numliteral
            self.symlist.append( nn )
            self.symlist.append(self.get_symbol( sym ))
            append_sym = False
            print(f"add_symbol spec #2 : symlist len={len(self.symlist)}")
            print(f"add_symbol spec #2 : {symlist_to_string(self.symlist)}")
        elif sym != "NUMBER" and self.symbols[sym]["t"] == "fn" and self.state["RESULT"] != "":
            # we assume the User wants to evaluate this function with the previous result
            # FN ( . ) added
            self.symlist.insert(0, self.get_symbol('OB'))
            self.symlist.insert(0, self.get_symbol(sym))
            self.symlist.append(self.get_symbol('CB'))
            append_sym = False
            print(f"add_symbol spec #3 : {symlist_to_string(self.symlist)}")
        elif sym == "CB" and self.state["RESULT"] != "":
            # we assume the User wants to put the previous expression into brackets
            # ( . ) added
            self.symlist.insert(0, self.get_symbol('OB'))
            self.symlist.append(self.get_symbol('CB'))
            append_sym = False
            print(f"add_symbol spec #4 : {symlist_to_string(self.symlist)}")
        elif sym == "EQU" and self.state["RESULT"] != numliteral:
            # we assume the User has typed a number at the end of the expression and wants to evaluate it
            nn = self.get_symbol( 'NUMBER' )
            nn['s'] = numliteral
            self.symlist.append( nn )
            append_sym = False
            print(f"add_symbol spec #5 : {symlist_to_string(self.symlist)}")
        elif sym != "NUMBER" and self.symbols[sym]["t"] != "fn" and not self.state[sym]:
            # no idea what the user might have wanted
            print(f"    unexpected symbol {sym}, do nothing")
            return
        
        # add to the operational (+ eventually bracket) stack
        expr_res = None # {state, value}
        if append_sym:
            expr_res = self.handle_symbol(sym, numliteral)
        else:
            expr_res = self.eval_symlist()
            
        # print(f"    expr_res: {expr_res}")
            
        # expression
        self.state["EXPRESSION"] = symlist_to_string(self.symlist)
            
        # decide on button states
        self.calc_state()
        
        # find out if a result is available
        if expr_res["state"] == "empty":
            self.state["RESULT"] =""
            self.state["STATE"] = "type something!"
        elif expr_res["state"] == "malformed expression":
            self.state["RESULT"] =""
            self.state["STATE"] = "complete/modify the expression!"
        elif expr_res["state"] == "unexpected value during evaluation":
            self.state["RESULT"] =""
            self.state["STATE"] = expr_res["state"]
        else:
            self.state["RESULT"] = expr_res["value"]
            self.state["STATE"] = "result"

    def handle_symbol(self, sym, numliteral):
        
        sss = self.symbols[sym]
        
        # count brackets
        if sss["t"] == "bracket":
            self.handle_brackets(sym)
            
        # expand symlist
        elem = None
        if sss["t"] == "number":
            elem = self.get_symbol("NUMBER")
            elem["s"] = numliteral
        else:
            # simply add to the end and reset the dec.sep. counter
            elem = self.get_symbol(sym)
        
        self.symlist.append(elem)
        # print(f"handle_symbol: added {elem}")
        
        # operation counter
        if sss["t"] == "fn" or sss["t"] == "inop":
            self.opcount += 1
            
        # evaluate new symlist
        return self.eval_symlist() # {state, value}

    def print_state(self):
        e = []
        d = []
        for k in self.state.keys():
            if k != "STATE" and k != "RESULT" and k != "EXPRESSION":
                if self.state[k]:
                    e.append(k)
                else:
                    d.append(k)
        print(f"EXPR: {self.state['EXPRESSION']} --> {self.state['RESULT']} --> state: {self.state['STATE']}")
        print(f"enabled: {','.join(e)} , disabled: {','.join(d)}")

    def eval_symlist(self):
        if len(self.symlist) == 0:
            return {"state": "empty", "value": None}
            
        if len(self.symlist) == 1:
            if self.symlist[-1]["t"] == "number":
                return {"state": "ok", "value": self.symlist[-1]["s"]}
            else:
                return {"state": "malformed expression", "value": None}
            
        # transform to polish form and evaluate
        val = None
        error = ""
        try:
            pf = to_polish_form(self.symlist)
            print(f"pf: {symlist_to_string(pf)}")
            val = eval_polish_form(pf)
        except ZeroDivisionError:
            val = None
            error = "unexpected value during evaluation"
        except ValueError:
            val = None
            error = "unexpected value during evaluation"
        except IndexError:
            val = None
            error = "malformed expression"
        except MalformedExpression:
            val = None
            error = "malformed expression"
        finally:
            if error != "":
                return {"state": error, "value": None}
            else:
                return {"state": "ok", "value": val}



