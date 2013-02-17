try:
    import ipython
except ImportError:
    ipython = False

class iPythonNB(Reader):
    enabled = bool(ipython)
    file_extensions = ['ipynb']

    def read(self, source_path):
        pub = self._get_publisher(source_path)
        parts = pub.writer.parts
        content = parts.get('body')

        metadata = self._parse_metadata(pub.document)
        metadata.setdefault('title', parts.get('title'))

        return content, metadata
