#!/usr/bin/env python3

import re
import os
from typing import List

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import calculator
from forms import SequenceForm

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32))

bootstrap = Bootstrap(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["60 per minute", "5 per second"],
)

calculator.init()


def render_csv(details: List[calculator.CalculatedSCMF]):
    csv = "Sequence,Motif,Motif Sequence Position,Efficiency Score\n"
    for item in details:
        if item.scmf:
            csv += "%s,%s,%s,%.2f\n" % (item.seq, item.scmf.motif, item.scmf.position, item.scmf.cleavage_efficiency)
        else:
            csv += "%s,,,\n" % item.seq

    return Response(csv, mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename="scmf.csv"'})


@app.route('/', methods=["GET", "POST"])
def scmf():
    form = SequenceForm()
    details: List[calculator.CalculatedSCMF] = []

    if form.validate_on_submit():
        for seq in re.findall(r'[ACGT]{20}', form.sequence.data.upper()):
            details.append(calculator.calculate_sequence(seq))

        if form.csv.data:
            return render_csv(details)

    return render_template('index.html', form=form, details=details, found=len([d for d in details if d.scmf]))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
