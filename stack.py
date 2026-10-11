import re


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node

    def pop(self):
        if self.top is None:
            return None
        popped_node = self.top
        self.top = self.top.next
        popped_node.next = None
        return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        return None

    def print_stack(self):
        if self.top is None:
            print("Stack is empty")
            return

        current = self.top
        print("Stack elements (top -> bottom):")
        while current:
            print(current.data)
            current = current.next


def infix_to_postfix(expression):
    token_pattern = re.compile(r"(?:\d+(?:\.\d*)?|\.\d+)|[A-Za-z_][A-Za-z0-9_]*|[()+\-*/^]")
    tokens = []
    position = 0
    for match in token_pattern.finditer(expression):
        if expression[position:match.start()].strip():
            raise ValueError(f"Unsupported character near position {position + 1}.")
        tokens.append(match.group())
        position = match.end()
    if expression[position:].strip():
        raise ValueError(f"Unsupported character near position {position + 1}.")
    if not tokens:
        raise ValueError("Enter an infix expression.")

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    right_associative = {'^'}
    operators = Stack()
    output = []
    steps = []
    expecting_operand = True

    def stack_values():
        values = []
        current = operators.top
        while current:
            values.append(current.data)
            current = current.next
        return values

    def record_step(token, action):
        steps.append({
            'token': token,
            'action': action,
            'operators': stack_values(),
            'output': ' '.join(output),
        })

    for token in tokens:
        if token[0].isalnum() or token[0] == '_':
            if not expecting_operand:
                raise ValueError(f"Missing operator before '{token}'.")
            output.append(token)
            expecting_operand = False
            record_step(token, f"Add operand {token} to the output.")
        elif token == '(':
            if not expecting_operand:
                raise ValueError("Add an operator before '('.")
            operators.push(token)
            record_step(token, "Push '(' onto the operator stack.")
        elif token == ')':
            if expecting_operand:
                raise ValueError("A closing parenthesis needs an operand before it.")
            while operators.peek() is not None and operators.peek() != '(':
                output.append(operators.pop())
            if operators.peek() is None:
                raise ValueError("There is no matching opening parenthesis.")
            operators.pop()
            expecting_operand = False
            record_step(token, "Pop operators through the matching '('.")
        else:
            if expecting_operand:
                raise ValueError(f"Operator '{token}' needs a left operand.")
            while operators.peek() in precedence:
                top_operator = operators.peek()
                higher_precedence = precedence[top_operator] > precedence[token]
                equal_left_associative = (
                    precedence[top_operator] == precedence[token]
                    and token not in right_associative
                )
                if not (higher_precedence or equal_left_associative):
                    break
                output.append(operators.pop())
            operators.push(token)
            expecting_operand = True
            record_step(token, f"Push operator {token} onto the operator stack.")

    if expecting_operand:
        raise ValueError("The expression cannot end with an operator.")

    while operators.peek() is not None:
        operator = operators.pop()
        if operator == '(':
            raise ValueError("There is no matching closing parenthesis.")
        output.append(operator)
        record_step(operator, f"Pop operator {operator} to the output.")

    return ' '.join(output), steps