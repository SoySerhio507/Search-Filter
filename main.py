from __future__ import annotations
from typing import List, Optional
from csv import *

WORDS = []
# Creating the list of words from the Words.txt file
with open("Words.txt", "r") as file:
    file_list = reader(file)

    for line in file_list:
        WORDS.extend(line)


def separate(string: str) -> List[str]:
    """Returns a list containing all characters that made up <string>"""
    s = []
    for index in range(len(string)):
        s.append(string[index])
    return s


def load_words(wordlist: List[str]) -> Tree:
    """Return a Tree containing words from <wordlist>

    Preconditions: All words in <wordlist> start with <FIRST>
    """
    wordtree = Tree(None, [])
    for word in wordlist:
        word = separate(word)
        wordtree.add_word(word)
    return wordtree


def give_suggestions(wordtree: Tree, string: str) -> List[str]:
    """Return a list containing all words in <wordtree> that contain the prefix
    <string>"""
    string = separate(string)
    return wordtree.prefixed_by(string)


class Tree:
    """A tree containing letters that make up words

    _word: True if there exists a word composed of the current letter
    concatenated with its parents


    === Representation Invariants ===
      - If self._root is None then self._subtrees is an empty list.
      This setting of attributes represents an empty tree.

      Note: self._subtrees may be empty when self._root is not None.
      This setting of attributes represents a tree consisting of just one
      node.

      - 0 <= len(self.root) <= 1
    """
    _root: str
    _subtrees: List[Tree]
    _parent: Optional[Tree]
    _word: bool

    def __init__(self, root: Optional[str], subtrees: List[Tree],
                 parent: Tree = None) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If <root> is None, the tree is empty.
        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        self._parent = parent
        self._word = False

    def __eq__(self, other: Tree) -> bool:
        """Return True if <other> is equal to this Tree"""
        return self._root == other._root

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.
        """
        return self._str_indented()

    def _str_indented(self, depth: int = 0) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            s = '  ' * depth + str(self._root) + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                s += subtree._str_indented(depth + 1)
            return s

    def is_empty(self) -> bool:
        """Return whether this tree is empty.
        """
        return self._root is None

    def add_word(self, word: List[str]) -> bool:
        """Return True if the word <word> is added the Tree, return False

        Precondition:
          - Every element of <word> has length 1
          - word[0] == <FIRST>
          - self.root == Tree(FIRST, [])
        """
        if not word:
            return True
        elif len(word) == 1:
            if self._parent is None:
                # This means we never entered the recursive case
                return False
            return True
        else:  # len(word) > 1
            # We know that self.root == word[0] because either:
            #   - this is our first time recursing, in which case
            #   self._root == FIRST == word[0]
            # or
            #   - we have recursed before, in which case we called
            #   subtree.add_word(word[1:]) and recursed
            if self.is_empty():
                self._root = word.pop(0)
                self.fill(word)
                return True
            elif Tree(word[1], []) in self._subtrees:
                for subtree in self._subtrees:
                    if subtree._root == word[1]:
                        return subtree.add_word(word[1:])
            else:  # Tree(word[1], []) not in self._subtrees
                word.pop(0)
                self.fill(word)
                return True

    def fill(self, word: List[str]) -> None:
        """Create a branch in this Tree where each node contains a character
        from <word>
        """
        if not word:
            self._word = True
            return None
        branch = Tree(word.pop(-1), [])
        branch._word = True
        while word:
            branch = Tree(word.pop(-1), [branch])
        self.add_child(branch)

    def get_parent(self) -> Optional[Tree]:
        """Return this Tree's parent, or None if no parent exists"""
        return self._parent

    def _set_parent(self, parent: Tree) -> None:
        """Set <parent> as this Tree's parent"""
        self._parent = parent

    def add_child(self, child: Tree) -> None:
        """Add <child> as one of this Tree's subtrees"""
        self._subtrees.append(child)
        child._set_parent(self)

    def get_wordlist(self) -> List[str]:
        """Return a list containing all words in this Tree"""
        if self.is_empty():
            return []
        elif self._word:
            wordlist = [self._root]
            if self._subtrees:
                for subtree in self._subtrees:
                    for word in subtree.get_wordlist():
                        wordlist.append(self._root + word)
                return wordlist
            else:
                return wordlist
        else:  # not self._word
            wordlist = []
            for subtree in self._subtrees:
                for word in subtree.get_wordlist():
                    wordlist.append(self._root + word)
            return wordlist

    def prefixed_by(self, prefix: List[str]) -> List[str]:
        """Return all words in this Tree prefixed by <prefix>"""
        if not prefix or self.is_empty():
            return self.get_wordlist()
        elif prefix[0] != self._root:
            return []
        elif not self._subtrees:
            return [self._root]
        else:  # prefix[0] == self._root
            all_prefixed = []
            for subtree in self._subtrees:
                for word in subtree.prefixed_by(prefix[1:]):
                    all_prefixed.append(self._root + word)
            return all_prefixed


if __name__ == '__main__':
    words = load_words(WORDS[:])
    print(give_suggestions(words, ''))
