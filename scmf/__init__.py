#!/usr/bin/env python3

import csv
import dataclasses
import sys
import os

from typing import Optional


@dataclasses.dataclass
class SCMF:
    position: int
    motif: str
    cleavage_efficiency: float


DATA_SOURCE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'scmf.csv')

MIN_MOTIF_LENGTH = 4
MOTIFS: dict[str, SCMF] = {}


def load_weights():
    with open(DATA_SOURCE, newline='', encoding="utf-8") as csvfile:
        cs = csv.DictReader(csvfile, delimiter=',', quotechar='"')
        for row in cs:
            scmf = SCMF(
                position=int(row["Spacer position"]),
                motif=row["Motif"],
                cleavage_efficiency=float(row["MotCutEff"].replace(",", "."))
            )

            motif_id = "%d:%s" % (scmf.position, scmf.motif)
            MOTIFS[motif_id] = scmf


def calculate_spacer(spacer: str) -> Optional[SCMF]:
    found: Optional[SCMF] = None

    for i in range(0, len(spacer) - MIN_MOTIF_LENGTH + 1):
        for j in range(MIN_MOTIF_LENGTH, len(spacer) - i + 1):
            motif_id = "%d:%s" % (i + 1, spacer[i:i + j])
            if motif_id in MOTIFS and (not found or MOTIFS[motif_id].cleavage_efficiency < found.cleavage_efficiency):
                found = MOTIFS[motif_id]

    return found


def process_input():
    if len(sys.argv) < 1:
        print("Usage: %s <Sequence>" % (sys.argv[0]))
        sys.exit(1)
    else:
        for sequence in sys.argv[1:]:
            scmf = calculate_spacer(sequence)
            if scmf:
                print("%s,%s,%s,%.2f\n" % (sequence, scmf.motif, scmf.position, scmf.cleavage_efficiency))
            else:
                print("%s,,,\n" % sequence)


if __name__ == '__main__':
    load_weights()
    process_input()
