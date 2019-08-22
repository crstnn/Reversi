# Cristian Corrado | 29666716

PRECEDENCE_DICT = {"+": 3, "-": 3, "*": 2, "/": 2, "^": 1}


def tokenization(expr):
    def is_number(str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    # removing whitespace
    expr = expr.replace(" ", "")

    # parsing string
    operators = list("+-*/^()")
    result_list = []
    temp_string = ""
    for i in range(len(expr)):
        e = expr[i]
        if e not in operators:
            temp_string += e
        if e in operators:
            if temp_string != "":
                result_list.append(temp_string)
                temp_string = ""
            result_list.append(e)

        if i == len(expr) - 1 and e not in operators:
            result_list.append(temp_string)

    # parsing list to integer or string
    for i in range(len(result_list)):
        if is_number(result_list[i]):
            result_list[i] = float(result_list[i])

    return result_list


def has_precedence(op1, op2):
    op1_prec, op2_prec = PRECEDENCE_DICT[op1], PRECEDENCE_DICT[op2]

    if op1_prec < op2_prec:
        return True
    return False


def evaluate_binary_operator(val1, operator, val2):
    funcs_by_op = {
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        "^": lambda a, b: a ** b,
    }
    return funcs_by_op[operator](val1, val2)


def get_index_of_highest_precedence_operator(token_list):
    operator_indexes = list(filter(lambda p: p[1] in PRECEDENCE_DICT, enumerate(token_list)))
    result = operator_indexes[0][0]
    for idx, op in operator_indexes[1:]:
        if has_precedence(op, token_list[result]):
            result = idx
    return result


def simple_evaluation(tokens):
    evaluation_list = tokens[:]

    while len(evaluation_list) > 1:
        highest_precedence_idx = get_index_of_highest_precedence_operator(evaluation_list)
        evaluated_term = evaluate_binary_operator(evaluation_list[highest_precedence_idx - 1],
                                                  evaluation_list[highest_precedence_idx],
                                                  evaluation_list[highest_precedence_idx + 1])
        evaluation_list = evaluation_list[:highest_precedence_idx - 1] + [evaluated_term] + evaluation_list[
                                                                                            highest_precedence_idx + 2:]

    return float(evaluation_list[0])


def complex_evaluation(tokens):
    def extract_one_bracket_expr(lst):
        """
        Returns a tuple of prefix, bracket_contents, suffix if any brackets exist else None.
        Brackets around bracket_contents are removed.
        """
        idx = 0
        first_brac = ""
        while idx < len(lst):
            if lst[idx] == "(":
                first_brac = idx
            if lst[idx] == ")":
                if first_brac != "":
                    return lst[:first_brac], lst[first_brac + 1:idx], lst[idx + 1:]
            idx += 1
        return None

    evaluation_list = tokens[:]

    while True:

        parts = extract_one_bracket_expr(evaluation_list)
        if parts is None:
            return simple_evaluation(evaluation_list)
        bracket_expression_value = simple_evaluation(parts[1])
        evaluation_list = parts[0] + [bracket_expression_value] + parts[2]


def evaluation(string):
    return complex_evaluation(tokenization(string))


