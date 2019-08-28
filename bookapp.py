import re
from bookdb import BookDB

DB = BookDB()

def resolve_path(path):
    pages = {
            "": books, 
            "book": book,
            }
    lst = path.strip('/').split('/')
    name = lst[0]
    args = lst[1:]
    try:
        func = pages[name]
    except KeyError:
        if name is not 'book':
            raise Exception
        else:
            raise NameError
    
    return func, args

def book(book_id):
    page = '''
        <h1>{title}</h1>
        <table>
            <tr>
            <tr><th>
            <tr><th>ISBN</th><td>{isbn}</td><t/tr>
            <tr><th>Publisher</th><td>{publisher}</td><t/tr>
            <tr><th>Author</th><td>{author}</td><t/tr>
        </table>
        <a href="/">Back to the list</a>
        '''
    book = DB.title_info(book_id)
    if book is None:
        raise NameError
    
    return page.format(**book)

def books():
    all_titles = DB.titles()
    listing = ['<h1> Shelf</h1>', '<ul>']
    printout = '<li><a href="/book/{id}">{title}</a></li>'
    for book in all_titles:
        listing.append(printout.format(**book))
    listing.append('</ul>')
    return '\n'.join(listing)

def application(environ, start_response):
    headers = [('Content-type', 'text/html')]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        status = "200 OK"
        func, args = resolve_path(path)
        body = func(*args)
    except NameError:
        status = "404 Error - Not Found"
        body = "<h1> 404 - Not Found </h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1> 500 - Internal Server Error </h1>"
    finally:    
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
