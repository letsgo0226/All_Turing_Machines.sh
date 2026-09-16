#!/usr/bin/env python3
"""Evidence-first analyzer for every public repository owned by a GitHub account.
Classifies source text; names are metadata, never proof. No claim of completeness,
RH, physical realization, or an attained infinite limit is made.
"""
import os,re,json,base64,urllib.request,urllib.error
OWNER=os.getenv("GITHUB_OWNER","letsgo0226")
TOKEN=os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN","")
MAX=int(os.getenv("MAX_FILE_BYTES","200000"))
EXT={".py",".sh",".js",".ts",".c",".cc",".cpp",".h",".hpp",".rs",".go",".java",".rb",".pl",".lua",".hs",".lean",".v",".sv",".md",".txt",".yml",".yaml",".json"}

def api(path):
    r=urllib.request.Request("https://api.github.com"+path,headers={"Accept":"application/vnd.github+json","User-Agent":"account-reflection","Authorization":"Bearer "+TOKEN} if TOKEN else {"Accept":"application/vnd.github+json","User-Agent":"account-reflection"})
    with urllib.request.urlopen(r,timeout=30) as f:return json.load(f)
def owned_public():
    out=[]
    for page in range(1,100):
        a=api(f"/users/{OWNER}/repos?type=owner&per_page=100&page={page}")
        out += [x for x in a if not x.get("private") and x.get("owner",{}).get("login","").lower()==OWNER.lower()]
        if len(a)<100:break
    return out
def source_path(p):
    q=p.lower();return q in {"readme.md","readme.txt"} or any(q.endswith(e) for e in EXT)
def tags(text):
    L=text.lower()
    rules={
      "turing_explicit":r"turing|\bdelta\b|transition|tape|machine state",
      "godel_encoding":r"g[oö]del|godel|prime.factor|prime exponent|int\.from_bytes",
      "zeta_reference":r"riemann|\bzeta\b|ζ|mpmath\.zeta|zetazero",
      "omega_formal":r"\bomega\b|ω|colim|direct limit|inverse limit",
      "self_reference":r"quine|self.?refer|self.?encod|read.*__file__|sys\.argv\[0\]",
      "numerical_math":r"mpmath|numpy|scipy|cmath|decimal",
      "physical_language":r"schwarzschild|entropy|quantum|energy|physical|physics",
      "workflow":r"github actions|workflow_dispatch|actions/checkout"
    }
    return {k:bool(re.search(v,L)) for k,v in rules.items()}
def main():
    registry=[]
    for r in owned_public():
        name=r["name"]; branch=r.get("default_branch") or "main"; texts=[]; files=[]; err=None
        try:
            tree=api(f"/repos/{OWNER}/{name}/git/trees/{branch}?recursive=1")
            for x in tree.get("tree",[]):
                if x.get("type")!="blob" or x.get("size",0)>MAX or not source_path(x["path"]):continue
                try:
                    b=api(f"/repos/{OWNER}/{name}/git/blobs/{x['sha']}")
                    raw=base64.b64decode(b.get("content","")).decode("utf-8","replace") if b.get("encoding")=="base64" else b.get("content","")
                    texts.append(raw);files.append(x["path"])
                except Exception as e: err=(err or "")+f" file:{x['path']}:{type(e).__name__}"
        except Exception as e:err=f"tree:{type(e).__name__}"
        T="\n".join(texts); evidence=tags(T)
        registry.append({"repo":f"{OWNER}/{name}","default_branch":branch,"source_files":files,"evidence":evidence,"status":{"exact_roundtrip":"unverified","zeta_numeric":"present" if ("mpmath.zeta" in T.lower() or "zetazero" in T.lower()) else "unverified","omega_attained":False,"all_logical_worlds_enumerated":False,"metaphysical_identity_proved":False,"open":True,"final":False},"scan_error":err})
    summary={"schema":"ACCOUNT_PUBLIC_REPO_REFLECTION/v1","owner":OWNER,"scope":"owned-public-default-branches","repos":len(registry),"principle":"classify evidence; repository names are not proof","omega":"formal/open boundary, not attained by this finite scan","registry":registry}
    os.makedirs("account_reflection",exist_ok=True)
    with open("account_reflection/registry.json","w",encoding="utf8") as f:json.dump(summary,f,ensure_ascii=False,indent=2)
    counts={k:sum(x["evidence"][k] for x in registry) for k in next(iter(registry),{"evidence":{}})["evidence"]}
    with open("account_reflection/SUMMARY.md","w",encoding="utf8") as f:
        f.write(f"# Account Public Repository Reflection\n\nOwner: `{OWNER}`  \nPublic owned repositories scanned: **{len(registry)}**\n\n")
        for k,v in counts.items():f.write(f"- `{k}`: {v}\n")
        f.write("\nThese are lexical/code-evidence classifications, not proofs of mathematical, physical, or metaphysical claims. `Ω` remains a formal open boundary.\n")
    print(json.dumps({"owner":OWNER,"repos":len(registry),"counts":counts,"omega_attained":False,"open":True,"final":False},ensure_ascii=False))
if __name__=="__main__":main()
