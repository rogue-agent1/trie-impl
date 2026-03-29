#!/usr/bin/env python3
"""trie_impl - Prefix tree with autocomplete."""
import sys, argparse, json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.count = 0

class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.size = 0
    def insert(self, word):
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
            node.count += 1
        if not node.is_end:
            node.is_end = True
            self.size += 1
    def search(self, word):
        node = self._find(word)
        return node is not None and node.is_end
    def starts_with(self, prefix):
        node = self._find(prefix)
        return node is not None
    def _find(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return None
            node = node.children[ch]
        return node
    def autocomplete(self, prefix, limit=10):
        node = self._find(prefix)
        if not node:
            return []
        results = []
        self._dfs(node, prefix, results, limit)
        return results
    def _dfs(self, node, prefix, results, limit):
        if len(results) >= limit:
            return
        if node.is_end:
            results.append(prefix)
        for ch in sorted(node.children):
            self._dfs(node.children[ch], prefix + ch, results, limit)

def main():
    p = argparse.ArgumentParser(description="Trie CLI")
    sub = p.add_subparsers(dest="cmd")
    ac = sub.add_parser("complete", help="Autocomplete")
    ac.add_argument("prefix")
    ac.add_argument("-w", "--words", nargs="+", required=True)
    ac.add_argument("-n", type=int, default=10)
    args = p.parse_args()
    if args.cmd == "complete":
        t = Trie()
        for w in args.words:
            t.insert(w)
        results = t.autocomplete(args.prefix, args.n)
        print(json.dumps({"prefix": args.prefix, "matches": results, "total_words": t.size}))
    else:
        p.print_help()

if __name__ == "__main__":
    main()
