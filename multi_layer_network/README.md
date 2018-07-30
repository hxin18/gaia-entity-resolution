To ease the process of getting started with the pipeline, some sample input/output files have been provided:
- `cluster_heads.json` -> output of `RPI_to_JSON.py`
- `needed_words.vec` -> input of `node_embeddings.py`
- `cluster_heads.vec` -> output of `node_embeddings.py`
- `cluster_heads.links.edges` -> output of `\*_edge_list.py`, this particular one was produced by running `links_edge_list.py`.
- `connected_components_with_links.txt` -> output of `connected_components.py`
- `evaluation_ready_filtered_RPI_shatter.tab` -> input of `EDL_output.py`

- `:Entity_strings.json` -> output of `get_strings.py`
- `:String_strings.json` -> output of `get_strings.py`
- `events_subset.json` -> output of `extract_events.py`

Don't hesitate to run each file with `-h` for more information.
