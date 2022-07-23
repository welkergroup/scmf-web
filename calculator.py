#!/usr/bin/env python3
import dataclasses
from typing import Optional

import scmf


@dataclasses.dataclass
class CalculatedSCMF:
    seq: str
    scmf: Optional[scmf.SCMF]


def init():
    scmf.load_weights()


def calculate_sequence(seq: str) -> CalculatedSCMF:
    return CalculatedSCMF(seq=seq, scmf=scmf.calculate_spacer(seq[0:20]))


def process_input():
    import sys
    if len(sys.argv) < 1:
        print("Usage: %s <Spacer>" % (sys.argv[0]))
        sys.exit(1)
    else:
        print("Sequence,Motif,Motif Sequence Position,Efficiency Score")
        if len(sys.argv) == 1:
            for line in sys.stdin:
                spacer = line.rstrip()
                print_spacer(spacer)
        else:
            for spacer in sys.argv[1:]:
                print_spacer(spacer)


def print_spacer(sequence):
    calculated = calculate_sequence(sequence)
    if calculated.scmf:
        print("%s,%s,%s,%.4f" % (
            calculated.seq, calculated.scmf.motif, calculated.scmf.position, calculated.scmf.cleavage_efficiency))
    else:
        print("%s,,," % calculated.seq)


if __name__ == '__main__':
    init()
    process_input()
