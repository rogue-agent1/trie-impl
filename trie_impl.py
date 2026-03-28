#!/usr/bin/env python3
"""trie_impl - Trie with autocomplete."""
import argparse, sys

class TrieNode:
    def __init__(self): self.children = {}; self.is_end = False; self.count = 0

class Trie:
    def __init__(self): self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True; node.count += 1
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    def _find(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return None
            node = node.children[c]
        return node
    def autocomplete(self, prefix, limit=10):
        node = self._find(prefix)
        if not node: return []
        results = []
        def dfs(n, path):
            if len(results) >= limit: return
            if n.is_end: results.append((prefix + path, n.count))
            for c in sorted(n.children):
                dfs(n.children[c], path + c)
        dfs(node, "")
        return results
    def starts_with(self, prefix):
        return self._find(prefix) is not None
    def size(self):
        count = [0]
        def dfs(n):
            if n.is_end: count[0] += 1
            for c in n.children.values(): dfs(c)
        dfs(self.root); return count[0]

def main():
    p = argparse.ArgumentParser(description="Trie with autocomplete")
    p.add_argument("--demo", action="store_true", default=True)
    a = p.parse_args()
    t = Trie()
    words = ["apple","app","application","apply","apt","ape","banana","band","ban","bat","bath"]
    for w in words: t.insert(w)
    print(f"Trie: {t.size()} words")
    for prefix in ["ap","ba","ban","z"]:
        results = t.autocomplete(prefix)
        print(f"  '{prefix}' -> {[r[0] for r in results]}")

if __name__ == "__main__": main()
