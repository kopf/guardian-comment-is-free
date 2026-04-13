#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "click",
#     "transformers",
#     "torch",
# ]
# ///

import json
import random
import click

def load_and_clean_data(file_path):
    """Loads JSON data and strips trailing author names from titles."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        raise click.ClickException(f"Failed to read JSON file: {e}")
    
    titles = []
    for url, entry in data.items():
        title = entry.get('title', '')
        if title:
            # Strip the ' | Author Name' suffix to keep training data clean
            clean_title = title.split(' | ')[0].strip()
            titles.append(clean_title)
            
    return titles

class MarkovChain:
    """A simple n-gram Markov Chain text generator."""
    def __init__(self, state_size=2):
        self.state_size = state_size
        self.model = {}

    def build(self, text_list):
        for text in text_list:
            words = text.split()
            if len(words) < self.state_size:
                continue
                
            # Pad the sequence to learn start and end states
            words = ['__START__'] * self.state_size + words + ['__END__']
            for i in range(len(words) - self.state_size):
                state = tuple(words[i:i + self.state_size])
                next_word = words[i + self.state_size]
                
                if state not in self.model:
                    self.model[state] = []
                self.model[state].append(next_word)

    def generate(self):
        state = tuple(['__START__'] * self.state_size)
        output = []
        
        # Failsafe to prevent infinite loops in weird data edge cases
        max_words = 30 
        
        while len(output) < max_words:
            if state not in self.model:
                break
            next_word = random.choice(self.model[state])
            if next_word == '__END__':
                break
            output.append(next_word)
            state = tuple(list(state[1:]) + [next_word])
            
        return ' '.join(output)

def generate_with_transformer(titles, num_headlines):
    """Uses a small Hugging Face LLM and few-shot prompting to generate text."""
    click.echo("Loading Hugging Face model (distilgpt2)... This might take a moment on the first run.")
    
    # Importing here so the Markov approach doesn't pay the import penalty if selected
    from transformers import pipeline
    import logging
    logging.getLogger("transformers").setLevel(logging.ERROR) # Suppress noisy HF warnings
    
    # distilgpt2 is small enough to run quickly on CPU without eating all your RAM
    generator = pipeline('text-generation', model='distilgpt2')
    
    results = []
    for _ in range(num_headlines):
        # Sample different titles for each generation to keep prompts varied
        sample_titles = random.sample(titles, min(8, len(titles)))
        prompt = "Here are some newspaper headlines:\n"
        for t in sample_titles:
            prompt += f"- {t}\n"
        prompt += "\nWrite a new, original newspaper headline in the exact same style:\n-"
        
        # Generate text
        output = generator(
            prompt, 
            max_new_tokens=25, 
            num_return_sequences=1, 
            truncation=True, 
            pad_token_id=50256,
            temperature=0.9,
            do_sample=True
        )
        
        generated_text = output[0]['generated_text']
        # Extract just the newly generated line, cutting off at the next newline
        new_part = generated_text[len(prompt):].split('\n')[0].strip()
        
        # Clean up stray quotation marks the model might add
        new_part = new_part.strip('"\'') 
        results.append(new_part)
        
    return results

@click.command()
@click.argument('filepath', type=click.Path(exists=True, dir_okay=False))
@click.option('--method', type=click.Choice(['markov', 'transformer']), default='markov', 
              help="Choose the underlying text generation engine.")
@click.option('--count', '-c', type=int, default=5, 
              help="Number of artificial headlines to generate.")
def main(filepath, method, count):
    """
    Parses a JSON dataset of articles and generates new, artificial headlines 
    based on the linguistic style of the originals.
    """
    titles = load_and_clean_data(filepath)
    click.secho(f"Successfully loaded and cleaned {len(titles)} titles.", fg="green")

    if not titles:
        raise click.ClickException("No valid titles found in the provided dataset.")

    click.echo(f"Generating {count} headlines using the '{method}' engine...\n")

    if method == 'markov':
        markov = MarkovChain(state_size=2)
        markov.build(titles)
        for i in range(count):
            click.secho(f"{i+1}. {markov.generate()}", fg="cyan")
            
    elif method == 'transformer':
        results = generate_with_transformer(titles, count)
        for i, res in enumerate(results):
            click.secho(f"{i+1}. {res}", fg="cyan")

if __name__ == '__main__':
    main()