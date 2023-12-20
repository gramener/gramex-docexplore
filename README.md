# @gramex/docexplore

A template for exploring topics in documents.

## Example

DocExplore is a visual interface to explore documents based on the topics they cover.

Here is an example that explores the abstracts of all LLM papers on arxiv.org:

[LLM Papers Explorer](llmpapers/index.html ":include")

Here is a list of examples to explore:

- [GPAI Abstracts](gpai/index.html ":ignore")
- [LLM Papers](llmpapers/index.html ":ignore")
- [The Art of War](artofwar/index.html ":ignore")

## Create the data

Create the data as a JSON file that lists the topics, documents, and matches between topics and documents.

[Here is an example](llmpapers/data.json):

```json
{
  "topics": [
    { "topic": "LLM Development & Safety", "subtopic": "Prompt Injection Security" },
    { "topic": "LLM Development & Safety", "subtopic": "LLM Application Safety" },
    ...
  ],
  "docs": [
    { "chapter": "arxiv", "section": "LLM", "para": "SOCIOFILLMORE: A Tool for ..." },
    ...
  ],
  "matches": [
    { "doc": 0, "topic": 1, "similarity": 0.86 },
    { "doc": 0, "topic": 5, "similarity": 0.92 },
    ...
  ],
}
```

- `topics` is an array of topic objects with keys:
  - `topic` (string): name of the topic
  - `subtopic` (string): name of the subtopic
- `docs` is an array of document objects with keys:
  - `chapter` (string): chapter name
  - `section` (string): section name
  - `para` (string): summary of actual text of the content
- `matches` is an array of linkages between the topics and documents with keys:
  - `doc` (number): index of the document in `docs`
  - `topic` (number): index of the topic in `topics`
  - `similarity` (number): similarity between the document and topic

An example of how to create such a dataset using ChatGPT is provided in
[llmpapers/extract.ipynb](https://code.gramener.com/cto/gramex-docexplore/-/blob/main/llmpapers/extract.ipynb).

## Build the front-end

In your project, install dependencies:

```shell
npm install @gramex/documap@2 @gramex/insighttree@3 @gramex/network@2 @gramex/ui@0.3 bootstrap@5 bootstrap-icons@1 d3@7 lit-html@2 scrollama@3
```

Copy the required files:

- [story.js](https://code.gramener.com/cto/gramex-docexplore/-/blob/main/story.js)
- [story.css](https://code.gramener.com/cto/gramex-docexplore/-/blob/main/story.css)
- [index.html](https://code.gramener.com/cto/gramex-docexplore/-/blob/main/llmpapers/index.html)

In `index.html`, you will probably want to change the following (apart from the title and description):

```js
// Point to your data file
window.data = await fetch("data.json").then((r) => r.json());
// Number of characters (letters) per pixel. Increase for smaller documap
window.charsPerPixel = 20;
```

```html
<!-- Change the value to set the default minimum similarity. Higher values show fewer matches -->
<input type="range" class="form-range ..." value="0.82" />
```

Open `index.html` in a browser to view the result.

## Release notes

- 1.0.0: 20 Dec 2023. Initial release

## Authors

- Anand S <s.anand@gramener.com>
- Aayush Thakur <aayush.thakur@gramener.com>
- Chandana Sagar <chandana.sagar@gramener.com>

## License

[MIT](https://spdx.org/licenses/MIT.html)
