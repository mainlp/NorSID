import yaml
import re
from pathlib import Path
from rasa.shared.nlu.training_data.training_data import TrainingData, Message
from rasa.shared.utils.io import write_text_file

def remove_prefix_from_tag(tag):
    tag = tag.strip()
    pos = tag.find("-")
    return tag[pos+1:]

def convert_bio_to_entities(text, tokens, tags):
    entities = []
    entity_start, entity_end, entity_type = None, None, None
    curr_position = 0

    for token, tag in zip(tokens, tags):
        token_start = text.find(token, curr_position)
        token_end = token_start + len(token)
        curr_position = token_end

        # TODO doesn't cover the OB- tag (only one in data, so negligible)
        if tag.startswith("B-"):
            if entity_type is not None:
                value = text[entity_start:entity_end]
                assert value != ""
                entities.append({
                    "value": value,
                    "entity": entity_type,
                    "start": entity_start,
                    "end": entity_end
                })
            # start a new entity
            entity_start = token_start
            entity_end = token_end
            entity_type = re.sub("/", "_", remove_prefix_from_tag(tag))  # Remove 'B-' from the tag
        elif tag.startswith("I-") and entity_type == remove_prefix_from_tag(tag):
            # continue the current entity
            entity_end = token_end
        else:
            # save the previous entity if we move to "O" or another tag
            if entity_type is not None:
                value = text[entity_start:entity_end]
                assert value != ""
                entities.append({
                    "value": value,
                    "entity": entity_type,
                    "start": entity_start,
                    "end": entity_end
                })
            entity_start, entity_end, entity_type = None, None, None

    # add the last entity if there is one
    if entity_type is not None:
        value = text[entity_start:entity_end]
        assert value != ""
        entities.append({
            "value": value,
            "entity": entity_type,
            "start": entity_start,
            "end": entity_end
        })
    return entities

def build_msg(entry):
    entities = convert_bio_to_entities(entry["text"], entry["tokens"], entry["tags"])
    return Message(text=entry["text"], intent=re.sub("/", "_", entry["intent"]), entities=entities)

def remove_whitespace_before_punct(text):
    # unused, this leads to weird behaviour because of misaligned entities, would require start/end to be adjusted after
    # the fact
    text = re.sub(r'\s+([?.!,;:])', r'\1', text)
    return re.sub(r'\n', ' ', text)

def convert_to_rasa_yaml(data):
    training_examples = [build_msg(e) for e in data]
    # TODO implicit dedup here.. is this a problem?
    return TrainingData(training_examples=training_examples)

def read_nlu(path):
    # modified from xsid repository
    slots = []
    intents = []
    curr_slots = []
    curr_tokens = []
    tokens = []
    texts = []
    for line in open(path):
        line = line.strip()
        if line.startswith("#") and "text-en" in line:
            continue
        elif line.startswith('# intent'):
            text = line[10:].strip()
            if line.startswith("=") or line.startswith(":"):
                text = line[1:]
            intents.append(text)
        elif line.startswith('# text'):
            text = line[8:].strip()
            if line.startswith("=") or line.startswith(":"):
                text = line[1:]
            texts.append(text)
        elif line == '':
            assert len(curr_tokens) == len(curr_slots)
            tokens.append(curr_tokens)
            slots.append(curr_slots)
            curr_slots = []
            curr_tokens = []
        elif line[0] == '#' and len(line.split('\t')) == 1:
            continue
        else:
            curr_slots.append(line.split('\t')[-1])
            curr_tokens.append(line.split('\t')[1])
    return texts, slots, intents, tokens

def print_stats(slots, intents, split, lang):
    intents_set = {i for i in intents}
    intents_cnt = len(intents_set)

    slots_set = {remove_prefix_from_tag(s) for g in slots for s in g if s != "O"}
    slots_cnt = len(slots_set)
    print(f"Found {intents_cnt} intent classes and {slots_cnt} entity types in the {lang} {split} set.")

    return slots_set, intents_set

def print_diff(coll):
    for i in range(2):
        sets = [coll[k][i] for k in coll.keys()]
        s1, s2 = sets
        all_elements = sorted(s1 | s2)
        col_width = max([len(e) for e in all_elements]) + 1
        print(f"{'train':<{col_width}} {'val':<{col_width}}")
        print("-" * 2 * col_width)
        for element in all_elements:
            col1 = element if element in s1 else ""
            col2 = element if element in s2 else ""
            print(f"{col1:<{col_width}} {col2:<{col_width}}")

def replace_slash(text):
    return re.sub("/", "__", text)

def main():
    langs = ["nor", "en"]
    write = True
    for lang in langs:
        coll = {}
        data_dir = "../data/NoMusic/NorSID" if lang == "nor" else "../data/xsid/data/xSID-0.6"
        for split in ["train", "valid"]:
            if lang == "en":
                path = f"{data_dir}/en.{split}.conll"
            else:
                path = f"{data_dir}/nb.projectedTrain.conll.fixed" if split == "train" else f"{data_dir}/norsid_dev.conll"

            texts, slots, intents, tokens = read_nlu(path)
            slots_set, intents_set = print_stats(slots, intents, split, lang)
            coll[split] = slots_set, intents_set

            if write:
                # because Rasa reserves '/' for retrieval intents, we replace with '__', choosing the double char so
                # that it can be more easily turned back into '/' (as there are already '_' in the original sets)
                intents = [replace_slash(i) for i in intents]
                # also replace the '/' in slot types
                data = [{"text": txt, "tokens": tok, "tags": [replace_slash(s) for s in s_g], "intent": i}
                        for txt, tok, s_g, i in zip(texts, tokens, slots, intents)]
                assert len(data) == len(texts)

                rasa_nlu_data = convert_to_rasa_yaml(data)
                # TODO these asserts will fail because of implicit dedup through Rasa.. do we mind?
                # assert len(rasa_nlu_data.training_examples) == len(data)
                # assert len(rasa_nlu_data.intents) == len(intents_set)
                # assert len(rasa_nlu_data.entities) == len(slots_set)

                output_dir = "data" if split == "train" else "tests"
                output_dir = f"{lang}/{output_dir}"
                output_fname = "nlu" if split == "train" else "test_nlu"
                Path(output_dir).mkdir(parents=True, exist_ok=True)
                nlu_path = f"{output_dir}/{output_fname}.yml"
                write_text_file(rasa_nlu_data.nlu_as_yaml(), nlu_path, append=False)
                if split == "train":
                    with open(f"{lang}/domain.yml", "w") as f:
                        rasa_domain_data = {
                            "version": "3.1",
                            "intents": list(set(intents)),
                            "entities": list(set(slots_set))}
                        yaml.safe_dump(rasa_domain_data, f, sort_keys=False)

        print_diff(coll)

if __name__ == "__main__":
    main()
