# Adapted from: https://stackoverflow.com/a/1176023

import  re

# Convert a camel case string (GovernmentResponseIndex) to
# snake case (government_response_index)
def camel_case_to_snake_case(string):
    snake_case = re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

    # Collapse multiple underscores into a single underscore
    snake_case = re.sub(r'_+', '_', snake_case)

    return snake_case
