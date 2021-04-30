import htmlmin

#reference code: https://github.com/jaysonsantos/jinja-assets-compressor/blob/master/jac/compressors/javascript.py

class HTMLCompressor(object):
    @classmethod
    def compile(cls, what, mimetype = "text/html", cwd = None, uri_cwd = None, debug = None):
        if debug:
            return what
        return htmlmin.minify(what)