#!/usr/bin/env python3
"""Trie (prefix tree) implementation with autocomplete."""
import sys, json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
    def insert(self, word):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True
        node.count += 1
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    def starts_with(self, prefix):
        return self._find(prefix) is not None
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
            if n.is_end: results.append(prefix + path)
            for c in sorted(n.children):
                dfs(n.children[c], path + c)
        dfs(node, '')
        return results
    def size(self):
        count = [0]
        def dfs(n):
            if n.is_end: count[0] += 1
            for c in n.children.values(): dfs(c)
        dfs(self.root)
        return count[0]

if __name__ == '__main__':
    t = Trie()
    if len(sys.argv) > 1 and sys.argv[1] == '--file':
        words = open(sys.argv[2]).read().splitlines()
        for w in words: t.insert(w.strip().lower())
        print(f"Loaded {t.size()} words")
        if len(sys.argv) > 3:
            prefix = sys.argv[3]
            print(f"Autocomplete '{prefix}': {', '.join(t.autocomplete(prefix))}")
    else:
        # Load system dictionary
        try:
            for w in open('/usr/share/dict/words').read().splitlines(): t.insert(w.lower())
            print(f"Loaded {t.size()} words from dictionary")
        except: pass
        print("Commands: search <word>, complete <prefix>, add <word>, size, quit")
        while True:
            try: line = input('> ').split()
            except EOFError: break
            if not line: continue
            if line[0] == 'quit': break
            elif line[0] == 'search': print("Found" if t.search(line[1]) else "Not found")
            elif line[0] == 'complete': print(', '.join(t.autocomplete(line[1])))
            elif line[0] == 'add': t.insert(line[1]); print("Added")
            elif line[0] == 'size': print(t.size())
