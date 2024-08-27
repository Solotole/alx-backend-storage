#!/usr/bin/env python3
""" module to list all lists """


def list_all(mongo_collection):
    """ listing all documents in a collection """
    documents = list(mongo_collection.find())

    return documents if documents else []
