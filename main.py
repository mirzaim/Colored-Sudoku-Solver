from typing import Callable, Any
import re
import itertools


class CSP:
    def __init__(self, variables: list[Any], neighbors: dict[Any, list[Any]], domain: dict[Any, Any],
                 constraints: dict[tuple[Any, Any], set[Callable[..., bool]]]):
        self.variables = variables
        self.domain = domain
        self.neighbors = neighbors
        self.constraints = constraints

    def degree(self, assigment: dict, var: Any):
        return len(set(self.neighbors[var]) - set(assigment.keys()))

    def mvr(self, var: Any):
        return len(self.domain[var])

    def get_best_unassigned_var(self, assigment: dict) -> str:
        return min(set(self.variables) - set(assigment.keys()),
                   key=lambda x: (self.mvr(x), -1 * self.degree(assigment, x)))

    def get_unassigned_vars(self, assigment: dict) -> set:
        return set(self.variables) - set(assigment.keys())

    def forward_checking(self, assigment: dict, var: Any, removes: dict, couple: dict = None):
        if couple is None:
            couple = {}
        # for neighbor in self.get_unassigned_vars(assigment).intersection(self.neighbors[var]):
        for neighbor in self.neighbors[var]:
            for dom in self.domain[neighbor]:
                for constraint in self.constraints[(neighbor, var)]:
                    if not constraint(dom, assigment.get(var, None), assigment.get(couple.get(neighbor, None), None),
                                      assigment.get(couple.get(var, None), None)):
                        removes.setdefault(neighbor, set()).add(dom)
            self.domain[neighbor] = self.domain[neighbor] - removes.get(neighbor, set())
            if len(self.domain[neighbor]) == 0:
                return False
        return True

    def assign(self, assignment: dict, var: Any, val):
        assignment[var] = val

    def preassign(self, preassignment: dict, couple=None):
        assign = {}
        removes = {}
        for var, val in preassignment.items():
            self.assign(assign, var, val)
            if not (self.forward_checking(assign, var, removes, couple) and (
                    couple is None or self.forward_checking(assign, couple[var], removes, couple))):
                return False
        return True

    def restore(self, assigment: dict, var: Any, removed: dict[Any, set]):
        del assigment[var]
        for var, dom in removed.items():
            self.domain[var].update(dom)


def simple_backtrack_search(csp: CSP, preassigned, couple=None):
    def backtrack(assign):
        if len(assign) == len(csp.variables):
            return assign
        var = csp.get_best_unassigned_var(assign)
        for val in csp.domain[var]:
            removed = {}
            csp.assign(assign, var, val)
            if csp.forward_checking(assign, var, removed, couple) and (
                    couple is None or csp.forward_checking(assign, couple[var], removed, couple)):
                result = backtrack(assign)
                if result is not None:
                    return result
            csp.restore(assign, var, removed)
        return None

    return backtrack(preassigned)


class Sudoku(CSP):

    def __init__(self, n: int):
        variables = list(itertools.product(range(1, n + 1), repeat=2))
        domain = {x: set(range(1, n + 1)) for x in variables}
        neighbor = {}
        for var in variables:
            neighbor[var] = [(var[0], y) for y in range(1, n + 1) if y != var[1]] + \
                            [(x, var[1]) for x in range(1, n + 1) if x != var[0]]
        constraints = {(x, y): {lambda a, b, *rest: a != b} for x in variables for y in neighbor[x]}
        super().__init__(variables, neighbor, domain, constraints)


class ColoredSudoku(CSP):

    @classmethod
    def parse(cls):
        colored_sudoku = ColoredSudoku(*reversed(list(map(int, input().split()))))
        colored_sudoku.colors_num = {}
        for i, color in enumerate(reversed(input().split()), start=1):
            colored_sudoku.colors_num[i], colored_sudoku.colors_num[color] = color, i
        assigment = {}
        for i in range(1, colored_sudoku.n + 1):
            for j, (number, color) in enumerate(re.findall("([1-9|*]+)([a-zA-Z|#]+)", input()), start=1):
                if number != '*':
                    assigment[(True, i, j)] = int(number)
                if color != '#':
                    assigment[(False, i, j)] = colored_sudoku.colors_num[color]
        colored_sudoku.preassign(assigment, colored_sudoku.couple)
        return colored_sudoku, assigment

    def print_assigment(self, assigment: dict):
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                print(
                    f"{assigment.get((True, i, j), '*')}{self.colors_num.get(assigment.get((False, i, j), None), '#')}",
                    end=' ')
            print()

    def __init__(self, n: int, m: int):
        # True for numbers, False for colors
        self.n, self.m = n, m
        variables = list(itertools.product((True, False), range(1, n + 1), range(1, n + 1)))
        domain = {**{x: set(range(1, n + 1)) for x in variables if x[0]},
                  **{x: set(range(1, m + 1)) for x in variables if not x[0]}}
        self.couple = {x: (not x[0],) + x[1:] for x in variables}
        neighbor = {}
        for var in variables:
            if var[0]:  # Numbers
                neighbor[var] = [(var[0], var[1], y) for y in range(1, n + 1) if y != var[2]] + \
                                [(var[0], x, var[2]) for x in range(1, n + 1) if x != var[1]]
            else:  # Colors
                neighbor[var] = [(var[0], var[1] + x, var[2]) for x in [-1, +1] if 0 < var[1] + x <= n] + \
                                [(var[0], var[1], var[2] + x) for x in [-1, +1] if 0 < var[2] + x <= n]
        constraints = {}
        for var in variables:
            for nb in neighbor[var]:
                constraints.setdefault((var, nb), set()).add(self.Constraints.not_equal)
                if (var[2] - nb[2], var[1] - nb[1]) in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    constraints.setdefault((var, nb), set()).add(self.Constraints.s_comp)

        self.colors_num = {}
        super().__init__(variables, neighbor, domain, constraints)

    class Constraints:

        @staticmethod
        def not_equal(a, b, *rest):
            return a != b

        @staticmethod
        def s_comp(v1, v2, vc1, vc2, *rest):
            try:
                return (not (vc1 > vc2) or (v1 > v2)) and (not (v1 > v2) or (vc1 > vc2))
            except TypeError:
                return True


def main():
    colored_sudoku, assignment = ColoredSudoku.parse()
    result = simple_backtrack_search(colored_sudoku, assignment, colored_sudoku.couple)
    print("Result: ")
    if result is not None:
        colored_sudoku.print_assigment(assignment)
    else:
        print("Unsolvable problem.")


if __name__ == '__main__':
    main()
