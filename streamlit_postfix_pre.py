import streamlit as st
import matplotlib.pyplot as plt
import networkx as nx

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_tree(expression, is_postfix=True):
    stack = []
    items = reversed(expression) if not is_postfix else expression
    for char in items:
        if char.isalnum():
            stack.append(TreeNode(char))
        else:
            if len(stack) < 2:
                raise ValueError("Invalid expression structure.")
            node = TreeNode(char)
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
    if len(stack) != 1:
        raise ValueError("Invalid expression structure.")
    return stack[-1]

def evaluate(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        try:
            return int(root.value)
        except ValueError:
            raise ValueError("Leaf node contains non-numeric value.")
    left_val = evaluate(root.left)
    right_val = evaluate(root.right)
    if root.value == '+':
        return left_val + right_val
    elif root.value == '-':
        return left_val - right_val
    elif root.value == '*':
        return left_val * right_val
    elif root.value == '/':
        if right_val == 0:
            raise ZeroDivisionError("Division by zero encountered.")
        return left_val // right_val
    else:
        raise ValueError("Unsupported operator encountered.")

def visualize_tree(root):
    G = nx.DiGraph()
    pos = {}

    def add_edges(node, x=0, y=0, layer=1):
        if node:
            G.add_node(node.value)  
            pos[node.value] = (x, -y)
            if node.left:
                G.add_edge(node.value, node.left.value)
                add_edges(node.left, x - 1 / layer, y + 1, layer + 1)
            if node.right:
                G.add_edge(node.value, node.right.value)
                add_edges(node.right, x + 1 / layer, y + 1, layer + 1)

    add_edges(root)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, arrows=False, node_size=2000, node_color='lightblue', font_size=10)
    st.pyplot(plt)


st.title("Expression Tree Builder & Evaluator")
expr_type = st.radio("Choose Expression Type", ["Postfix", "Prefix"])
expr = st.text_input("Enter expression (e.g., Postfix: 23*5+ or Prefix: +*235)")

if expr:
    try:
        root = build_tree(expr, is_postfix=(expr_type == "Postfix"))
        st.subheader("Visualized Expression Tree")
        visualize_tree(root)
        result = evaluate(root)
        st.success(f"Evaluation Result: {result}")
    except ZeroDivisionError as zde:
        st.error(f"Error: {zde}")
    except ValueError as ve:
        st.error(f"Error: {ve}")
    except Exception as e:
        st.error(f"Unexpected Error: {e}")