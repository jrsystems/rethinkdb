from sys import argv
from random import randint
from subprocess import call
from sys import path
path.append(".")
from test_util import RethinkDBTestServers

path.append("../../drivers/python")
import rethinkdb as r

server_build = argv[1]
if 2 in argv:
    lang = argv[2]
else:
    lang = None
with RethinkDBTestServers(server_build=server_build) as servers:
    port = servers.cpp_port
    c = r.connect(port=port)

    r.db('test').table_create('test').run(c)
    tbl = r.table('test')

    num_rows = randint(1111, 2222)

    print "Inserting %d rows" % num_rows
    tbl.insert([{'id':i} for i in xrange(0, num_rows)]).run(c)
    print "Done\n"

    if not lang or lang is 'py':
        print "Running Python"
        call(["python", "connections/cursor.py", str(port), str(num_rows)])
        print ''
    if not lang or lang is 'js':
        print "Running JS"
        call(["node", "connections/cursor.js", str(port), str(num_rows)])
        print ''