from jaclang.generator import Instruction
from jaclang.lexer import Token, LEFT_BRACE, RIGHT_BRACE
from jaclang.parser.branch import Branch, BranchFactory, TokenExpectedException, TokenNeededException
from jaclang.parser.expression import ExpressionFactory


class ScopeBranch(Branch):
    def __init__(self, branches: list[Branch]):
        self.branches = branches

    def printInfo(self, nested_level: int):
        print('    ' * nested_level, "scope:")
        for branch in self.branches:
            branch.printInfo(nested_level + 1)

    def generateInstructions(self) -> list[Instruction]:
        pass


class ScopeFactory(BranchFactory):
    def parseImpl(self, pos: int, tokens: list[Token]) -> (int, Branch):
        factories = [
            ExpressionFactory(),
        ]

        if pos >= len(tokens) or tokens[pos] != LEFT_BRACE:
            raise TokenExpectedException("Expected '{' at beginning of scope")
        pos += 1

        branches = []
        while tokens[pos] != RIGHT_BRACE:
            recognized = False
            for factory in factories:
                pos, branch = factory.parseDontExpect(pos, tokens)
                if branch is not None:
                    branches.append(branch)
                    recognized = True
            if pos >= len(tokens):
                raise TokenNeededException("Expected '}' at the end of scope")
            if not recognized:
                raise TokenNeededException("Did not recognize statement")
        pos += 1

        return pos, ScopeBranch(branches)
