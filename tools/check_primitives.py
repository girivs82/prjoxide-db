import json,re,sys
P=json.load(open(sys.argv[1]))["primitives"]
def enums(files, prefix):
    E={}
    for f in files:
        t=open(f).read()
        for m in re.finditer(r'"(%s\.[A-Z0-9_.]+)": \(\s*options: \{(.*?)\n\s*\},'%re.escape(prefix), t, re.S):
            E[m.group(1)[len(prefix)+1:]]=set(re.findall(r'"([A-Z0-9_]+)": \[',m.group(2)))
        for m in re.finditer(r'"(%s\.[A-Z0-9_.]+)": \(\s*bits:'%re.escape(prefix), t):
            E.setdefault(m.group(1)[len(prefix)+1:],"WORD")
    return E
sites={"IOLOGIC":(["SYSIO_B3_0.ron","SYSIO_B3_0_DQS1.ron"],"IOLOGICA"),"DQSBUF":(["SYSIO_B3_1_DQS0.ron","SYSIO_B3_0_DQS1.ron","SYSIO_B3_1_DQS2.ron"],"DQSBUF"),"DDRDLL":(["DDR_OSC_R.ron"],"DDRDLL"),"ECLKDIV":(["BMID_1_ECLK_2.ron"],"ECLKDIV3A"),"ECLKSYNC":(["BMID_1_ECLK_2.ron"],"ECLKSYNC3A")}
cache={}; bad=0
for name,p in P.items():
    files,prefix=sites[p["site"]]
    E=cache.setdefault(p["site"],enums(files,prefix))
    allset=list(p["settings"])
    for pin in p["pins"].values(): allset+=pin.get("settings",[])
    for c in p.get("connection_settings",{}).values():
        for v in c.values(): allset+=v
    for par in p.get("parameters",{}).values():
        if "values" in par:
            for v in par["values"].values(): allset+=v
        if "word" in par and par["word"] not in E: print(name,"missing word",par["word"]); bad+=1
    for s in allset:
        k,o=s.rsplit(".",1)
        if k not in E: print(name,"missing enum",k); bad+=1
        elif E[k]!="WORD" and o not in E[k]: print(name,"bad option",s,sorted(E[k])); bad+=1
print("problems:",bad)
