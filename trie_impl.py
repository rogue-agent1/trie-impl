#!/usr/bin/env python3
"""Pure Python Trie with prefix search and autocomplete."""
class Trie:
    def __init__(self): self.root={}
    def insert(self,word):
        node=self.root
        for c in word: node=node.setdefault(c,{})
        node["$"]=True
    def search(self,word):
        node=self._find(word); return node is not None and "$" in node
    def starts_with(self,prefix):
        return self._find(prefix) is not None
    def autocomplete(self,prefix,limit=10):
        node=self._find(prefix)
        if node is None: return []
        results=[]; self._collect(node,prefix,results,limit); return results
    def _find(self,prefix):
        node=self.root
        for c in prefix:
            if c not in node: return None
            node=node[c]
        return node
    def _collect(self,node,prefix,results,limit):
        if len(results)>=limit: return
        if "$" in node: results.append(prefix)
        for c in sorted(node):
            if c!="$": self._collect(node[c],prefix+c,results,limit)
    def delete(self,word):
        def _del(node,word,i):
            if i==len(word): node.pop("$",None); return len(node)==0
            c=word[i]
            if c in node and _del(node[c],word,i+1): del node[c]; return "$" not in node and len(node)==0
            return False
        _del(self.root,word,0)
if __name__=="__main__":
    t=Trie()
    for w in ["apple","app","application","apt","bat","bath","bar"]: t.insert(w)
    assert t.search("apple"); assert not t.search("ap")
    assert t.autocomplete("ap")==["app","apple","application","apt"]
    t.delete("app"); assert not t.search("app"); assert t.search("apple")
    print("All Trie tests passed")
