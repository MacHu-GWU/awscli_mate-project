# -*- coding: utf-8 -*-

from chalice import Chalice
from awscli_mate.lbd import hello

app = Chalice(app_name="awscli_mate")


@app.lambda_function(name="hello")
def handler_hello(event, context):
    return hello.high_level_api(event, context)
