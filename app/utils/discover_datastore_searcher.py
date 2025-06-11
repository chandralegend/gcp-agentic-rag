"""
This module provides a class to interact
with Google Discovery Engine and Datastore services
to perform searches and retrieve corresponding entities.
"""

from typing import List, Tuple, Callable, Optional, Any, Union
from google.api_core.client_options import ClientOptions
from google.cloud import discoveryengine_v1beta as discoveryengine
from google.cloud.discoveryengine_v1beta.types import SearchRequest, SearchResponse
from google.cloud.discoveryengine_v1beta.services.search_service.pagers import (
    SearchPager,
)
from google.cloud import datastore
from google.auth.credentials import Credentials
from dataclasses import dataclass
from typing import Iterator


Entity = datastore.Entity


@dataclass
class DiscoveryDatastoreSearcherConfig:
    """
    Configuration class for interacting with Google Discovery Datastore search service.

    This dataclass holds all necessary configuration parameters to connect to and
    query a Discovery Datastore in Google Cloud. It provides convenient properties
    to construct resource paths needed for various API operations.

    Attributes:
      project_id (str): The Google Cloud project ID where the datastore is located.
      location (str): The region or zone where the datastore is deployed (e.g., 'us-central1').
      data_store_id (str): The unique identifier for the specific datastore.
      datastore_kind (str): The type or category of the datastore.
      page_size (int, optional): Number of results to return per page in search queries.
        Defaults to 10.
      return_datastore_entities (bool, optional): Whether to return full datastore entities
        in search results. If False, only references might be returned. Defaults to True.

    Properties:
      data_store_resource (str): Formatted resource path for the datastore, constructed from
        project_id, location, and data_store_id.
      serving_config (str): Formatted path for the default serving configuration of the datastore.
      branch (str): Formatted path for the default branch of the datastore.
    """

    project_id: str
    location: str
    data_store_id: str
    datastore_kind: str
    page_size: int = 10
    return_datastore_entities: bool = True

    @property
    def data_store_resource(self) -> str:
        """Return the formatted resource path for the datastore."""
        return "/".join(
            [
                "projects",
                self.project_id,
                "locations",
                self.location,
                "dataStores",
                self.data_store_id,
            ]
        )

    @property
    def serving_config(self) -> str:
        """Return the formatted path for the default serving configuration of the datastore."""
        return "/".join(
            [
                "projects",
                self.project_id,
                "locations",
                self.location,
                "collections",
                "default_collection",
                "dataStores",
                self.data_store_id,
                "servingConfigs",
                "default_serving_config",
            ]
        )

    @property
    def branch(self) -> str:
        """Return the formatted path for the default branch of the datastore."""
        return "/".join(
            [
                "projects",
                self.project_id,
                "locations",
                self.location,
                "collections",
                "default_collection",
                "dataStores",
                self.data_store_id,
                "branches",
                "default_branch",
            ]
        )


class DiscoveryDatastoreSearcher:
    """
    DiscoveryDatastoreSearcher provides an integration between Google Cloud's Discovery Engine and Datastore services
    to perform searches and retrieve corresponding entities.

    This class allows for searching using Discovery Engine's capabilities and then fetching the corresponding
    entities from Datastore based on the search results. It provides methods for searching, fetching entities,
    and a callable interface that combines both operations.

    Attributes:
      config (DiscoveryDatastoreSearcherConfig): Configuration parameters for the searcher.
      result_processor (Optional[Callable[[Tuple[List[SearchResponse], List[Entity]]], Any]]):
        Optional function to process search results and entities.
      discovery_client (discoveryengine.SearchServiceClient): Client for Discovery Engine API.
      datastore_client (datastore.Client): Client for Datastore API.

    Example usage:
      ```
      config = DiscoveryDatastoreSearcherConfig(
        project_id="my-project",
        location="us-central1",
        serving_config="projects/my-project/locations/us-central1/collections/default_collection/engines/my-engine/servingConfigs/default_serving_config",
        branch="0",
        page_size=10,
        return_datastore_entities=True,
        datastore_kind="Product"

      searcher = DiscoveryDatastoreSearcher(config)
      results = searcher("shoes")
      search_responses, entities = results
      ```
    """

    def __init__(
        self,
        config: DiscoveryDatastoreSearcherConfig,
        credentials: Optional[Credentials] = None,
        result_processor: Optional[
            Callable[[Tuple[List[SearchResponse], List[Entity]]], Any]
        ] = None,
    ) -> None:
        self.config = config
        self.result_processor: Optional[
            Callable[[Tuple[List[SearchResponse], List[Entity]]], Any]
        ] = result_processor

        discoveryengine_client_options = (
            ClientOptions(
                api_endpoint=f"{self.config.project_id}-discoveryengine.googleapis.com"
            )
            if self.config.location != "global"
            else None
        )
        data_store_client_options = (
            ClientOptions(api_endpoint=f"{self.project_id}-datastore.googleapis.com")
            if self.config.location != "global"
            else None
        )

        # Initialize the clients.
        self.discovery_client: discoveryengine.SearchServiceClient = (
            discoveryengine.SearchServiceClient(
                client_options=discoveryengine_client_options, credentials=credentials
            )
        )
        self.datastore_client: datastore.Client = datastore.Client(
            project=self.config.project_id,
            client_options=data_store_client_options,
            credentials=credentials,
        )

    def search(
        self, query_text: str, page_token: str = "", filter_str: str = "", **kwargs
    ) -> Iterator[SearchResponse]:
        """
        Perform a search using Discovery Engine.

        Args:
          query_text (str): The search query.
          page_token (str): Optional page token for pagination.
          filter_str (str): Optional filter string.
          **kwargs: Additional keyword arguments to pass to the search request.

        Returns:
          SearchResponse: The raw search response from Discovery Engine.
        """
        request = SearchRequest(
            serving_config=self.config.serving_config,
            branch=self.config.branch,
            query=query_text,
            page_size=self.config.page_size,
            page_token=page_token,
            filter=filter_str,
            **kwargs,
        )
        search_pager: SearchPager = self.discovery_client.search(request=request)
        return search_pager.pages

    def fetch_datastore_entities(self, doc_ids: List[str]) -> List[Optional[Entity]]:
        """
        Retrieve Datastore entities corresponding to a list of document IDs.

        Args:
          doc_ids (List[str]): List of document IDs (assumed to be key names for the given kind).

        Returns:
          List[Optional[Entity]]: List of entities retrieved from Datastore.
          If an entity is not found, None is returned for that key.
        """
        keys: List[datastore.Key] = [
            self.datastore_client.key(self.datastore_kind, doc_id) for doc_id in doc_ids
        ]
        return self.datastore_client.get_multi(keys)

    def __call__(
        self, query_text: str, page_token: str = "", filter_str: str = "", **kwargs
    ) -> Union[Tuple[List[SearchResponse], List[List[Optional[Entity]]]], Any]:
        """
        Execute a search query and return the results with optional entity retrieval.

        This method performs the main search operation flow:
        1. Executes the search using the provided query text and parameters
        2. Extracts document IDs from the search results
        3. Optionally retrieves corresponding Datastore entities if configured
        4. Returns either raw results or processed results if a result processor is provided

        Parameters:
          query_text (str): The text to search for
          page_token (str, optional): Token for retrieving a specific page of results. Defaults to "".
          filter_str (str, optional): Filter string to narrow down search results. Defaults to "".
          **kwargs: Additional keyword arguments to pass to the search method.

        Returns:
          Union[Tuple[List[SearchResponse], List[List[Optional[Entity]]]], Any]:
            - If result_processor is None: A tuple containing (search_responses_list, entities)
              where search_responses_list is a list of SearchResponse objects and
              entities is a list of optional Entity objects.
            - If result_processor is provided: The output of the result processor function
              applied to the raw results.

        Note:
          Datastore entities are only fetched if self.config.return_datastore_entities is True
          and search results contain document IDs.
        """
        # Execute the search.
        search_responses: Iterator[SearchResponse] = self.search(
            query_text, page_token, filter_str, **kwargs
        )

        # Extract document IDs from the search results.
        doc_ids: List[str] = []
        search_responses_list = list(search_responses)
        for response in search_responses_list:
            doc_ids.append([result.id for result in response.results])

        # Retrieve corresponding Datastore entities.
        entities: List[Optional[Entity]] = []
        if doc_ids and self.config.return_datastore_entities:
            entities = self.fetch_datastore_entities(doc_ids)

        raw_results: Tuple[List[SearchResponse], List[Optional[Entity]]] = (
            search_responses_list,
            entities,
        )

        # If a processing function is provided, use it.
        if self.result_processor and callable(self.result_processor):
            return self.result_processor(raw_results)
        return raw_results


# --- Example usage ---
if __name__ == "__main__":
    # Define the configuration.
    config = DiscoveryDatastoreSearcherConfig(
        project_id="your-project-id",
        location="global",  # or your region (e.g., "us-central1")
        data_store_id="your-data-store-id",
        datastore_kind="YourKind",  # The Datastore kind where detailed records are stored.
        return_datastore_entities=True,  # Set to False if you don't need Datastore entities.
    )

    # Define an optional result processing function.
    def process_results(
        results: Tuple[List[SearchResponse], List[List[Optional[Entity]]]],
    ) -> tuple[int, int]:
        """Process the search results and Datastore entities."""
        # For demonstration, lets return the total number of search results and entities.
        search_results, datastore_entities = results
        total_results = sum(len(response.results) for response in search_results)
        total_entities = sum(len(entities) for entities in datastore_entities)
        return total_results, total_entities

    # Instantiate the searcher with the optional processor.
    searcher = DiscoveryDatastoreSearcher(
        config=config, result_processor=process_results
    )

    # Use the instance as a callable.
    query: str = "example search query"
    processed_output: Any = searcher(query)

    print("=== Processed Output ===")
    for item in processed_output:
        print(item)