import math

def symlist_to_string(slist):
    if slist == None or len(slist) == 0:
        return ""
        
    tmp = []
    for e in slist:
        tmp.append(e["s"])
    
    return " ".join(tmp)



def to_polish_form(slist):
    error = 0
    polform = []
    opstack = []
    ptr = 0
    while ptr < len(slist) and error == 0:
        act = slist[ptr]
        # print(f"to_polish_form :: act={act}")
        if act["t"] == "number":
            polform.append(act)
        else:
            if len(opstack) == 0:
                opstack.append(act)
            elif act["k"] == "OB":
                opstack.append(act)
            elif act["k"] == "CB":
                oppop = opstack.pop()
                while oppop["k"] != "OB":
                    polform.append(oppop)
                    oppop = opstack.pop()
            elif act["p"] > opstack[-1]["p"]:
                opstack.append(act)
            else:
                top = opstack[-1]
                while len(opstack) > 0 and top["p"] >= act["p"] and top["k"] != "OB":
                    top = opstack.pop()
                    polform.append(top)
                    if len(opstack) > 0:
                        top = opstack[-1]
                    else:
                        top = None
                    
                opstack.append(act)
        # print(f"to_polish_form: {symlist_to_string(opstack)}    ;    pf={symlist_to_string(polform)}")
        ptr += 1
    
    while len(opstack) > 0:
        oppop = opstack.pop()
        polform.append(oppop)
        
    return polform

def eval_fn(fn, arglist):
    if fn == "LN" and len(arglist) > 0 and arglist[0] > 0:
        return math.log(arglist[0])
    elif fn == "SQ" and len(arglist) > 0 and arglist[0] >= 0:
        return math.sqrt(arglist[0])
    else:
        return None
        
def eval_inop(fn, arglist):
    if fn == "PL" and len(arglist) > 1:
        return arglist[0] + arglist[1]
    elif fn == "MI" and len(arglist) > 1:
        return arglist[0] - arglist[1]
    elif fn == "MU" and len(arglist) > 1:
        return arglist[0] * arglist[1]
    elif fn == "DI" and len(arglist) > 1:
        return arglist[0] / arglist[1]
    elif fn == "PO" and len(arglist) > 1:
        return math.pow(arglist[0] , arglist[1])
    else:
        return None

def eval_polish_form(pf):
    args = []
    ptr = 0
    
    while ptr < len(pf):
        act = pf[ptr]
        if act["t"] == "number":
            num = float(act["s"])
            args.append(num)
        elif act["t"] == "fn":
            act1 = args.pop()
            value = eval_fn(act["k"], [act1])
            args.append(value)
        elif act["t"] == "inop":
            act2 = args.pop()
            act1 = args.pop()
            value = eval_inop(act["k"], [act1,act2])
            args.append(value)
        else:
            print(f"    ERR: ptr={ptr} -> type={act['t']}")
            raise MalformedExpression
        print(f"    ptr={ptr} -> args={args}")
        ptr += 1
    
    print(f"eval_polish_form :: args[0]={args[0]}")
    return args[0]
    