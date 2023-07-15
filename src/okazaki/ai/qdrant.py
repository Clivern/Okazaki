# MIT License
#
# Copyright (c) 2022 Clivern
#
# This software is licensed under the MIT License. The full text of the license
# is provided below.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from dataclasses import dataclass
from qdrant_client import QdrantClient

@dataclass
class Document:

    id: int
    text: str
    metadata: dict

class Qdrant:

    def __init__(self, url, api_key):
        self.client = QdrantClient(
            url=url,
            api_key=api_key,
        )

    def get_client(self):
        return self.client

    def info(self):
        return self.client.info()

    def insert(self, collection, documents):
        docs = []
        metadata = []
        ids = []

        for document in documents:
            docs.append(document.text)
            metadata.append(document.metadata)
            ids.append(document.id)


        return self.client.add(
            collection_name=collection,
            documents=docs,
            metadata=metadata,
            ids=ids
        )

    def search(self, collection, query_text, limit=1):
        return self.client.query(
            collection_name=collection,
            query_text=query_text,
            limit=limit
        )
