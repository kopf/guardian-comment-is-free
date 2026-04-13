## Comment is Free

The Guardian has a _Comment is Free_ article that's always stood out for its very particular style of headline. It's a wonderful newspaper and all, but something about the style of these headlines has always irritated me:

* Happy new year? Tell that to the natural world we are destroying | Philip Hoare
* My nightmare before Christmas in three words: health insurance renewal | Emma Brockes
* We need scientists to quiz Covid consensus, not act as agents of disinformation | Sonia Sodha
* Hate-filled abuse is poisoning Britain. I fought it, and ask you to do the same | Gina Miller

Those are just a few examples chosen at random from the dataset. The dataset is compiled by running `scrape.py` a couple of times daily in a github actions pipeline. It's stored as a github artifact. I'd thrown it together quickly sometime in 2016 with a view to using it to feed an automated "Headline Generator" using markov chains or something else. 

Then, more important things (literally absolutely anything else in the entire world) came along and I never got around to finishing it, i.e. writing the headline generator, which was the whole point of this stupid exercise to begin with. LLMs also came along in the meantime, the perfect solution for when code quality and correctness does not matter one iota. So here we are. 

You can generate headlines using markov chains or a small llm model from huggingface - although the markov chains are consistently more amusing, which is nice. Some choice favourites:

* Theresa May says she’s a good deal
* We celebrate the NHS’s saviour, not its cause
* no Brexit
* The Guardian view on child refugees: too little, too late
* This is a myth
* Boris Johnson still has everything to bomb us into ‘relationships’. We need to step back from Iran
* The Guardian view on the world let that happen
* Farage cannot be serious

As can be seen above, the generator might produce output that you may find distressing, tasteless or upsetting. Much like the real news, then. You've been warned. 

## Running

```
Usage: generate_headlines.py [OPTIONS] FILEPATH

  Parses a JSON dataset of articles and generates new, artificial headlines
  based on the linguistic style of the originals.

Options:
  --method [markov|transformer]  Choose the underlying text generation engine.
  -c, --count INTEGER            Number of artificial headlines to generate.
  --help                         Show this message and exit.
```

A download link for the dataset is provided in the "Archive dataset" step of [each pipeline run](https://github.com/kopf/guardian-comment-is-free/actions). 