#!/usr/bin/env python3
#
# Usage: ./remove_links.py
# Removes links from index.html and adds page numbers in brackets instead (p. XX).

from pathlib import Path


MATCHES = {
    '<strong>For details about sorted(), min() and max() see <a href="#sortable">sortable</a>.</strong>': '<strong>For details about sorted(), min() and max() see sortable (p. 16).</strong>',
    '<strong>Module <a href="#operator">operator</a> provides functions itemgetter() and mul() that offer the same functionality as <a href="#lambda">lambda</a> expressions above.</strong>': '<strong>Module \'operator\' (p. 31) provides functions itemgetter() and mul() that offer the same functionality as lambda expressions (p. 11) above.</strong>',
    '<strong>Adding <code class="python hljs"><span class="hljs-string">\'!r\'</span></code> to the expression converts object to string by calling its <a href="#class">repr()</a> method.</strong>': '<strong>Adding <code class="python hljs"><span class="hljs-string">\'!r\'</span></code> to the expression converts object to string by calling its repr() method.</strong>',
    '<strong>It can be any <a href="#callable">callable</a>, but is usually implemented as a function that returns a <a href="#closure">closure</a>.</strong>': '<strong>It can be any callable, but is usually implemented as a function that returns a closure.</strong>',
    '<strong>Hints are used by type checkers like <a href="https://pypi.org/project/mypy/">mypy</a>, data validation libraries such as <a href="https://pypi.org/project/pydantic/">Pydantic</a> and lately also by <a href="https://pypi.org/project/Cython/">Cython</a> compiler. However, they are not enforced by CPython interpreter.</strong>': '<strong>Hints are used by type checkers like mypy, data validation libraries such as Pydantic and lately also by Cython compiler. However, they are not enforced by CPython interpreter.</strong>',
    '<strong>Objects can be made <a href="#sortable">sortable</a> with <code class="python hljs"><span class="hljs-string">\'order=True\'</span></code> and immutable with <code class="python hljs"><span class="hljs-string">\'frozen=True\'</span></code>.</strong>': '<strong>Objects can be made sortable with <code class="python hljs"><span class="hljs-string">\'order=True\'</span></code> and immutable with <code class="python hljs"><span class="hljs-string">\'frozen=True\'</span></code>.</strong>',
    '<strong>For object to be <a href="#hashable">hashable</a>, all attributes must be hashable and \'frozen\' must be True.</strong>': '<strong>For object to be hashable, all attributes must be hashable and \'frozen\' must be True.</strong>',
    '<strong>Function field() is needed because <code class="python hljs"><span class="hljs-string">\'&lt;attr_name&gt;: list = []\'</span></code> would make a list that is shared among all instances. Its \'default_factory\' argument can be any <a href="#callable">callable</a>.</strong>': '<strong>Function field() is needed because <code class="python hljs"><span class="hljs-string">\'&lt;attr_name&gt;: list = []\'</span></code> would make a list that is shared among all instances. Its \'default_factory\' argument can be any callable (p. 17).</strong>',
    '<strong>Sequence iterators returned by the <a href="#iterator">iter()</a> function, such as list_iterator and set_iterator.</strong>': '<strong>Sequence iterators returned by the iter() function, such as list_iterator and set_iterator (p.&nbsp;3).</strong>',
    '<strong>Objects returned by the <a href="#itertools">itertools</a> module, such as count, repeat and cycle.</strong>': '<strong>Objects returned by the itertools module, such as count, repeat and cycle (p. 3).</strong>',
    '<strong>Generators returned by the <a href="#generator">generator functions</a> and <a href="#comprehensions">generator expressions</a>.</strong>': '<strong>Generators returned by the generator functions (p. 4) and generator expressions (p. 11).</strong>',
    '<strong>File objects returned by the <a href="#open">open()</a> function, etc.</strong>': '<strong>File objects returned by the open() function (p. 22), etc.</strong>',
    '<strong>Use <code class="python hljs"><span class="hljs-string">\'logging.exception(&lt;message&gt;)\'</span></code> to log the passed message, followed by the full error message of the caught exception. For details see <a href="#logging">logging</a>.</strong>': '<strong>Use <code class="python hljs"><span class="hljs-string">\'logging.exception(&lt;message&gt;)\'</span></code> to log the passed message, followed by the full error message of the caught exception. For details see logging (p. 32).</strong>',
    '<strong>Functions report OS related errors by raising either OSError or one of its <a href="#exceptions-1">subclasses</a>.</strong>': '<strong>Functions report OS related errors by raising OSError or one of its subclasses (p. 23).</strong>',
    '<strong>To print the spreadsheet to the console use <a href="#table">Tabulate</a> library.</strong>': '<strong>To print the spreadsheet to the console use Tabulate library (p. 34).</strong>',
    '<strong>For XML and binary Excel files (xlsx, xlsm and xlsb) use <a href="#dataframeplotencodedecode">Pandas</a> library.</strong>': '<strong>For XML and binary Excel files (xlsx, xlsm and xlsb) use Pandas library (p. 46).</strong>',
    '<strong>Bools will be stored and returned as ints and dates as <a href="#encode">ISO formatted strings</a>.</strong>': '<strong>Bools will be stored and returned as ints and dates as ISO formatted strings (p. 9).</strong>',
    '<strong>ProcessPoolExecutor provides true parallelism but: everything sent to/from workers must be <a href="#pickle">pickable</a>, queues must be sent using executor\'s \'initargs\' and \'initializer\' parameters, and executor needs to be reachable via <code class="python hljs"><span class="hljs-string">\'if __name__ == "__main__": ...\'</span></code>.</strong>': '<strong>ProcessPoolExecutor provides true parallelism but: everything sent to/from workers must be pickable, queues must be sent using executor\'s \'initargs\' and \'initializer\' parameters, and executor needs to be reachable via <code class="python hljs"><span class="hljs-string">\'if __name__ == "__main__": ...\'</span></code>.</strong>',
    '<strong>Asyncio module also provides its own <a href="#queue">Queue</a>, <a href="#semaphoreeventbarrier">Event</a>, <a href="#lock">Lock</a> and <a href="#semaphoreeventbarrier">Semaphore</a> classes.</strong>': '<strong>Asyncio module also provides its own Queue, Event, Lock and Semaphore classes (p. 30).</strong>',
    '<strong>Install a WSGI server like <a href="https://flask.palletsprojects.com/en/latest/deploying/waitress/">Waitress</a> and a HTTP server such as <a href="https://flask.palletsprojects.com/en/latest/deploying/nginx/">Nginx</a> for better security.</strong>': '<strong>Install a WSGI server like Waitress and a HTTP server such as Nginx for better security.</strong>',
    '<strong>The "latest and greatest" profiler that can also monitor GPU usage is called <a href="https://github.com/plasma-umass/scalene">Scalene</a>.</strong>': '<strong>The "latest and greatest" profiler that can also monitor GPU usage is called Scalene.</strong>',
}


def main():
    index_path = Path('..', 'index.html')
    lines = read_file(index_path)
    out = ''.join(lines)
    for from_, to_ in MATCHES.items():
        out = out.replace(from_, to_, 1)
    write_to_file(index_path, out)


###
##  UTIL
#

def read_file(filename):
    p = Path(__file__).resolve().parent / filename
    with open(p, encoding='utf-8') as file:
        return file.readlines()


def write_to_file(filename, text):
    p = Path(__file__).resolve().parent / filename
    with open(p, 'w', encoding='utf-8') as file:
        file.write(text)


if __name__ == '__main__':
    main()
