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

# Evaluation using the nist script
This is a sample run that goes all the way to the evaluation.
```shell
python links_edge_list.py -i cluster_heads.json -o links.edges
python connected_components.py -e links.edges -o links.ccs
python EDL_output.py -i evaluation_ready_filtered_RPI_shatter.tab -c links.ccs -n sample_run -o out.edl
```
Now we have `out.edl` that we can pass to the evaluation script. <br>
The evaluation tool can be cloned from here: https://github.com/wikilinks/neleval. The script we use is in `neleval/scripts/run_tac16_evaluation.sh`. <br>
Due to a strange error in the script that I could not resolve at the time, for every evaluation run one should change the line 29 of the script. For instance, if you want to evaluate `evaluation_ready_embeddings.tab` and store the results in `evaluation_ready_RPI.combined.tsv` then you should change the line as follows: <br>
`./nel prepare-tac15 $sysdir/evaluation_ready_embeddings.tab $options > $outdir/evaluation_ready_RPI.combined.tsv`
Once that line is changed, the evaluation script can be run like this from the neleval repository:
```shell
./scripts/run_tac16_evaluation.sh \
    /path/to/gold.tab \              # gold standard
    /system/output/directory \       # directory containing output files (out.edl in our case)
    /script/output/directory \       # directory to which results are written
    number_of_jobs                   # number of jobs for parallel mode
```
