#!/usr/bin/env python

import traceback


def index():
    """ root or home page - return HTML with instructions for using program """

    page = """
        <h1>Calculator Program</h1>
        <h2>To use this program, type your desired operations into the url.</h2>
        <h2>Here are examples:</h2>
        <p></p>"""

    for item in ['add', 'subtract', 'multiply', 'divide']:
        page += f"""
        <DT style='font-size:24px'>{item} 23 and 42:</DT>
        <DD style='font-size:24px' 'margin-left:10%'>
        <a href='http://localhost:8080/{item}/23/42'>http://localhost:8080/{item}/23/42</a></DD>
        </DT>
        <p></p>
        """

    return page


def add(*args):
    """ Returns a STRING with the SUM of the arguments """

    try:
        total = sum(map(int, args))
    except ValueError:
        raise

    main_page = '<h3><a href="http://localhost:8080">home</a><h3>'

    return f'<h1>The sum is: {str(total)}</h1>' \
           f'{main_page}'


def subtract(*args):
    """ Returns a STRING with the DIFFERENCE of the arguments """

    difference = int(args[0])

    try:
        for arg in args[1:]:
            difference -= int(arg)
    except ValueError:
        raise

    main_page = '<h3><a href="http://localhost:8080">home</a><h3>'

    return f'<h1>The difference is: {str(difference)}</h1>' \
           f'{main_page}'


def multiply(*args):
    """ Returns a STRING with the PRODUCT of the arguments """

    product = int(args[0])

    try:
        for arg in args[1:]:
            product *= int(arg)
    except ValueError:
        raise

    main_page = '<h3><a href="http://localhost:8080">home</a><h3>'

    return f'<h1>The product is: {str(product)}</h1>' \
           f'{main_page}'


def divide(*args):
    """ Returns a STRING with the quotient of the arguments """

    quotient = int(args[0])

    try:
        for arg in args[1:]:
            quotient /= int(arg)
    except (ValueError, ZeroDivisionError):
        raise

    main_page = '<h3><a href="http://localhost:8080">home</a><h3>'

    return f'<h1>The quotient is: {str(quotient)}</h1>' \
           f'{main_page}'


def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
        '': index,
        'add': add,
        'multiply': multiply,
        'subtract': subtract,
        'divide': divide
    }

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]

    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args


def application(environ, start_response):
    """ wsgi conforming application class """
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = '200 OK'
    except NameError:
        status = '404 Not Found'
        body = '<h1>Not Found</h1>'
    except ValueError:
        status = '406 Not Acceptable'
        body = '<h1>Not Acceptable</h1>' \
               '<h2>Attempted math operation on a non-number</h2>'
    except ZeroDivisionError:
        status = '406 Not Acceptable'
        body = '<h1>Not Acceptable</h1>' \
               '<h2>Attempted division by zero</h2>'
    except Exception:
        status = '500 Internal Server Error'
        body = '<h1>Internal Server Error</h1>'
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
