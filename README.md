This repository has a simple script that turns the [Spoken Wikipedia Corpus](https://nats.gitlab.io/swc/) into dataframes and jsons. I created this repo because currently the data when downloaded is an XML format that is not easily human readable. I might turn this into a package since there are a couple of dependencies.

### About the script

#### Dependencies
* `click`
* `pandas`
* `xmltodict`

`parser.py` works from the top-level directory (i.e. `PATH/TO/spoken_wikipedia_corpus/.`), traverses all the directories, and creates jsons (if you want to munge the data in a different way from how I did it here) as well as dataframes containing the columns `"term"`, `"start_time"`, `"end_time"`, and `"phonemes"]`. 

These jsons and dataframes are saved in the same folders where the `aligned.swc` files are for each Wikipedia article, and are saved as `aligned.swc.json` and `aligned.swc.df`.

#### Use

To use the script, simply call `python parser.py` with an additional parameter `-fd` to specify the directory where your files are, and it will automatically traverse all directories. 

### About the dataframe schema

`start_time` and `end_time` are taken directly from the XML schema, as well as the term that is being pronounced, which is stored in the schema as `t` or maybe `n`. It's called `term` here for transparency.

The `phonemes` column contains a json blob of phone durations for each word if those existed in the annotation file. Many words have durations and not phone durations, and vice versa. Additionally, many words don't have durations or timestamps at all, presumably because of the forced aligner.

Because it is easy to lose track of the documents themselves (and indeed, even the sentences), I have also uploaded my personal version of the data (`swc_word_durations.csv`), which is a tab-delimited text file with two additional columns beyond the dataframes in each of the folders: `id`, which is a index of the article that the data come from in alphabetic order, and `duration`, which subtracts `start_time` from `end_time`. Additionally, the index (which will be loaded as a column `X` in R or as a regular index in pandas) keeps track of the location of each word or character in the document that is being read aloud.
