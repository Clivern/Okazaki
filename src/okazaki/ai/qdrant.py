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

from openai import OpenAI
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct, VectorParams, Distance


class Client:
    """Qdrant Client for managing collections and embeddings."""

    def __init__(
        self,
        qdrant_url,
        qdrant_api_key,
        open_api_key,
        open_api_model="text-embedding-3-small",
    ):
        """
        Initializes the Qdrant and OpenAI clients.

        Args:
            qdrant_url (str): The URL of the Qdrant instance.
            qdrant_api_key (str): API key for accessing Qdrant.
            open_api_key (str): API key for OpenAI services.
            open_api_model (str): Model name for OpenAI embeddings.
        """
        self.qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
        )
        self.open_api_client = OpenAI(api_key=open_api_key)
        self.open_api_model = open_api_model

    def get_client(self):
        """Returns the Qdrant client instance."""
        return self.qdrant_client

    def close(self):
        """Closes the connection to the Qdrant client."""
        self.qdrant_client.close()

    def info(self):
        """Retrieves information about the Qdrant instance."""
        return self.qdrant_client.info()

    def create_collection(self, name, size=1536):
        """
        Creates a new collection in Qdrant.

        Args:
            name (str): The name of the collection.
            size (int): The dimensionality of the vectors (default is 1536).

        Raises:
            Exception: If there is an error creating the collection.
        """
        try:
            self.qdrant_client.create_collection(
                name, vectors_config=VectorParams(size=size, distance=Distance.COSINE)
            )
        except Exception as e:
            raise Exception(f"Error creating collection: {e}")

    def insert(self, collection, documents):
        """
        Inserts documents into a specified collection.

        Args:
            collection (str): The name of the collection to insert into.
            documents (list): A list of document objects to insert.

        Raises:
            Exception: If there is an error creating embeddings or inserting documents.
        """
        points = []

        for document in documents:
            payload = document.metadata
            payload["text"] = document.text

            try:
                result = self.open_api_client.embeddings.create(
                    input=document.text, model=self.open_api_model
                )
            except Exception as e:
                raise Exception(
                    f"Error creating embedding for document {document.id}: {e}"
                )

            points.append(
                PointStruct(
                    id=document.id, vector=result.data[0].embedding, payload=payload
                )
            )

        try:
            self.qdrant_client.upsert(collection, points)
        except Exception as e:
            raise Exception(f"Error inserting documents into collection: {e}")

    def search(self, collection, text, filters={}, limit=10):
        """
        Searches for similar documents in a specified collection.

        Args:
            collection (str): The name of the collection to search.
            text (str): The search query text.
            filters (dict): Optional filters to apply to the search results.
            limit (int): Maximum number of results to return (default is 10).

        Returns:
            list: Search results from the specified collection.

        Raises:
            Exception: If there is an error creating embeddings or searching.
        """
        try:
            result = self.open_api_client.embeddings.create(
                input=text, model=self.open_api_model
            )
        except Exception as e:
            raise Exception(f"Error creating embedding for search query: {e}")

        must = []

        for key, value in filters.items():
            must.append(
                models.FieldCondition(
                    key=key,
                    match=models.MatchValue(value=value),
                )
            )

        try:
            if len(must) > 0:
                return self.qdrant_client.search(
                    collection_name=collection,
                    query_vector=result.data[0].embedding,
                    query_filter=models.Filter(must=must),
                    with_payload=True,
                    limit=limit,
                )
            else:
                return self.qdrant_client.search(
                    collection_name=collection,
                    query_vector=result.data[0].embedding,
                    limit=limit,
                )
        except Exception as e:
            raise Exception(f"Error searching collection: {e}")
