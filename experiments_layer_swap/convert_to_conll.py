import sys
import re

def process_line(line):
    match = re.match(r"<(.+?)> -> (.+)", line)
    if not match:
        raise ValueError("Line does not match expected format")

    intent = match.group(1)
    sentence = match.group(2)

    tokens = []
    for part in re.split(r"(\[.+?:.+?\])", sentence):
        if re.match(r"\[.+?:.+?\]", part):  # Tagged token
            word, tag = re.match(r"\[(.+?):(.+?)\]", part).groups()
            tokens.append((word, intent, tag))
        else:
            for word in part.split():
                if word.strip():
                    tokens.append((word, intent, "O"))

    text = " ".join([token[0] for token in tokens])
    output = [
        f"# text = {text}",
        f"# intent = {intent}",
        "# dialect =",
    ]
    for i, token in enumerate(tokens):
        output.append(f"{i+1}\t{token[0]}\t{token[1]}\t{token[2]}")

    return "\n".join(output)

def process():
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    with open(input_file, "r") as f, open(output_file, "w") as o:
        for line in f:
            o.write(f"{process_line(line)}\n\n")


if __name__ == "__main__":
    process()