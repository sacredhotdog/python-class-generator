import argparse


LINE_BREAK = "\n"
INDENT = " " * 4


def parse_args():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("class_name")
    arg_parser.add_argument("attributes", help="Comma-separated list of class attributes")
    arg_parser.add_argument("--eq", dest="generate_eq", action="store_true")
    arg_parser.add_argument("--no-file", action="store_true", help="Don't create an output file")

    return arg_parser.parse_args()


def generate():
    args = parse_args()
    attributes = args.attributes.split(",")

    init_parameters = ""
    props_init = ""
    props_definitions = ""
    eq_definition = ""
    eq_attribute_comparisons = ""
    hash_definition = ""
    hash_attributes = ""

    attribute_total = len(attributes)
    attribute_count = 0

    for attribute in attributes:
        attribute_count += 1
        init_parameters += f", {attribute}"
        props_init += f"{INDENT * 2}self.{attribute} = {attribute}"

        if attribute_count < attribute_total:
            props_init += LINE_BREAK

        props_definitions += LINE_BREAK
        props_definitions += f"{INDENT}@property{LINE_BREAK}"
        props_definitions += f"{INDENT}def {attribute}(self):{LINE_BREAK}"
        props_definitions += f"{INDENT * 2}return self._{attribute}{LINE_BREAK}"
        props_definitions += LINE_BREAK
        props_definitions += f"{INDENT}@{attribute}.setter{LINE_BREAK}"
        props_definitions += f"{INDENT}def {attribute}(self, {attribute}):{LINE_BREAK}"
        props_definitions += f"{INDENT * 2}self._{attribute} = {attribute}{LINE_BREAK}"

        if args.generate_eq:
            if attribute_count > 1:
                eq_attribute_comparisons += INDENT * 4

            eq_attribute_comparisons += f"self.{attribute} == other.{attribute}"
            hash_attributes += f"{INDENT * 4}self.{attribute}"

            if attribute_count < attribute_total:
                eq_attribute_comparisons += " and \\"
                hash_attributes += ", "

            eq_attribute_comparisons += LINE_BREAK
            hash_attributes += LINE_BREAK

    output = f"class {args.class_name}:{LINE_BREAK}"
    output += LINE_BREAK
    output += f"{INDENT}def __init__(self{init_parameters}):{LINE_BREAK}"
    output += props_init
    output += LINE_BREAK

    if args.generate_eq:
        eq_definition += LINE_BREAK
        eq_definition += f"{INDENT}def __eq__(self, other):{LINE_BREAK}"
        eq_definition += f"{INDENT * 2}if not isinstance(other, {args.class_name}):{LINE_BREAK}"
        eq_definition += f"{INDENT * 3}return NotImplemented{LINE_BREAK}"
        eq_definition += LINE_BREAK
        eq_definition += f"{INDENT * 2}if other is not None:{LINE_BREAK}"
        eq_definition += f"{INDENT * 3}return {eq_attribute_comparisons}{LINE_BREAK}"
        eq_definition += LINE_BREAK
        eq_definition += f"{INDENT * 2}return False{LINE_BREAK}"

        hash_definition += LINE_BREAK
        hash_definition += f"{INDENT}def __hash__(self):{LINE_BREAK}"
        hash_definition += f"{INDENT * 2}return hash({LINE_BREAK}"
        hash_definition += f"{INDENT * 3}({LINE_BREAK}"
        hash_definition += hash_attributes
        hash_definition += f"{INDENT * 3}){LINE_BREAK}"
        hash_definition += f"{INDENT * 2}){LINE_BREAK}"

        output += eq_definition
        output += hash_definition

    output += props_definitions

    if not args.no_file:
        with open(f"{args.class_name}.py", "w", newline="") as output_file:
            output_file.write(output)

    return output


if __name__ == "__main__":
    print(generate())
