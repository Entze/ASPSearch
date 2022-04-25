import clingo
from clingo import Application, ast
from clingo import Propagator


class Transformer:
    def __init__(self, builder, check):
        self._builder = builder
        self._state = "guess"
        self._check = check

    def add(self, stm):
        if stm.ast_type == ast.ASTType.Program:
            if stm.name == "check" and not stm.parameters:
                self._state = "check"
            elif stm.name in ("base", "guess") and not stm.parameters:
                self._state = "guess"
            else:
                raise RuntimeError("unexpected program part")

        else:
            if self._state == "guess":
                self._builder.add(stm)
            else:
                self._check.append(stm)


class Checker:
    def __init__(self):
        self._ctl = clingo.Control()
        self._map = []

    def backend(self):
        return self._ctl.backend()

    def add(self, guess_lit, check_lit):
        self._map.append((guess_lit, check_lit))

    def ground(self, check):
        with ast.ProgramBuilder(self._ctl) as builder:
            for stm in check:
                builder.add(stm)

        self._ctl.ground([("base", [])])

    def check(self, control):
        assignment = control.assignment

        assumptions = []
        for guess_lit, check_lit in self._map:
            if assignment.is_true(guess_lit):
                assumptions.append(check_lit)
            else:
                assumptions.append(-check_lit)

        ret = self._ctl.solve(assumptions)
        if ret.unsatisfiable is not None:
            return ret.unsatisfiable

        raise RuntimeError("Search interrupted!")


class GACApp(Application):
    def __init__(self):
        self.program_name = "guess-and-check"
        self.version = "1.0"

    def main(self, ctl: clingo.Control, files):
        check = []
        with ast.ProgramBuilder(ctl) as builder:
            trans = Transformer(builder, check)
            for file in files:
                ast.parse_string(file, trans.add)
        ctl.register_propagator(GACPropagator(check))

        ctl.ground([("base", [])])
        ctl.solve()


class GACPropagator(Propagator):
    def __init__(self, check):
        self._check = check
        self._checker = None

    def init(self, init):
        print("Init")
        checker = Checker()
        self._checker = checker

        with checker.backend() as backend:
            for atom in init.symbolic_atoms:
                guess_lit = init.solver_literal(atom.literal)
                if init.assignment.is_false(guess_lit):
                    continue

                check_lit = backend.add_atom(atom.symbol)
                if init.assignment.is_true(guess_lit):
                    backend.add_rule([check_lit], [])
                else:
                    backend.add_rule([check_lit], [], True)
                    checker.add(guess_lit, check_lit)

        checker.ground(self._check)

    def check(self, control: clingo.PropagateControl):
        print("Check")
        assignment: clingo.propagator.Assignment = control.assignment
        checker = self._checker

        if not checker.check(control):
            conflict = []
            for level in range(1, assignment.decision_level + 1):
                conflict.append(-assignment.decision(level))
            control.add_clause(conflict)
