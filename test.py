"""
title: Test tool
author: Goekdeniz Guelmez
date: 2024-06-15
version: 1.0
license: MIT
description: A pipeline to testt out tool calling capabilities.
requirements: urllib, difflib
"""
import requests
from datetime import datetime
import urllib.parse

from blueprints.function_calling_blueprint import Pipeline as FunctionCallingBlueprint

class Pipeline(FunctionCallingBlueprint):
    class Valves(FunctionCallingBlueprint.Valves):
        SEARCH_BASE: str = ""

    class Tools:
        def __init__(self, pipeline) -> None:
            self.pipeline = pipeline

        def get_current_time(
            self,
        ) -> str:
            """
            Get the current time.

            :return: The current time.
            """

            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            return f"Current Time = {current_time}"

        def generate_and_save_image(self, prompt: str) -> str:
            """
            Generate a image with Flux1.1 Pro and save that image to my files.

            :param prompt: The to generate a image to.
            Get a dictionary of all lights in my home.

            :return: A text saving wether its succesfulkl or not with the error.
            """
            prompt = prompt
            return f"Succesfully generated image woth prompt: {prompt}"

        def search_web(self, prompt: str, format: str = 'json', count: int = 3, safe: int = 3) -> str:
            """
            Search the web using SearchXNG. Use this when you need to find the latest information or if a command or question requires data beyond your current knowledge cut-off.

            :param prompt: The query or prompt describing what you want to search for on the web.
            :param format: The format in which the search engine should return the response. Default is set to 'json'.
            :param count: The number of search results to return. Default is set to 3.
            :param safe: The safe search level. Higher values indicate stricter safe search settings. Default is set to 3.
            :return: The result of the search operation.
            """
            # URL-encode the prompt to ensure it's correctly formatted for the request
            encoded_prompt = urllib.parse.quote(prompt)

            # Define the search URL with the encoded prompt
            url = f"{self.pipeline.valves.SEARCH_BASE}/search?q={encoded_prompt}&format={format}&count={count}&safe={safe}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }

            try:
                # Make a GET request to the search URL
                response = requests.get(url, headers=headers)
                
                # Check if the request was successful
                if response.status_code == 200:
                    try:
                        # Attempt to return the JSON response if available
                        return response.json()
                    except ValueError:
                        # Handle the case where response is not valid JSON
                        return {"error": "Invalid JSON response received", "content": response.text}
                else:
                    # Handle unsuccessful requests
                    return {"error": f"Search failed with status code {response.status_code}"}
            except requests.exceptions.RequestException as e:
                # Handle any requests exceptions
                return {"search_web error": f"An error occurred: {e}"}
            

    def __init__(self):
        super().__init__()
        self.name = "My Tools Pipeline"
        self.valves = self.Valves(
            **{
                **self.valves.model_dump(),
                "pipelines": ["*"],  # Connect to all pipelines
            },
        )
        self.tools = self.Tools(self)
