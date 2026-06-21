import ast
import operator
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import yaml

# Separate AST operators to avoid type signature mismatches
BIN_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

UNARY_OPERATORS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

COMP_OPERATORS = {
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
}


def safe_eval(node, context):
    """Securely evaluate an AST node in the given context."""
    if isinstance(node, ast.Expression):
        return safe_eval(node.body, context)
    elif isinstance(node, ast.Constant):  # Python >= 3.8
        return node.value
    else:
        # Avoid direct lookup of deprecated/removed Num/Str classes on newer Pythons
        num_class = getattr(ast, "Num", None)
        if num_class is not None and isinstance(node, num_class):
            return node.n
        str_class = getattr(ast, "Str", None)
        if str_class is not None and isinstance(node, str_class):
            return node.s

    if isinstance(node, ast.Name):
        if node.id in context:
            return context[node.id]
        raise NameError(f"Variable '{node.id}' is not defined in context.")
    elif isinstance(node, ast.Attribute):
        value = safe_eval(node.value, context)
        if hasattr(value, node.attr):
            return getattr(value, node.attr)
        raise AttributeError(f"Attribute '{node.attr}' not found on {value}.")
    elif isinstance(node, ast.BinOp):
        left = safe_eval(node.left, context)
        right = safe_eval(node.right, context)
        op_type = type(node.op)
        if op_type in BIN_OPERATORS:
            return BIN_OPERATORS[op_type](left, right)
        raise TypeError(f"Unsupported binary operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        operand = safe_eval(node.operand, context)
        op_type = type(node.op)
        if op_type in UNARY_OPERATORS:
            return UNARY_OPERATORS[op_type](operand)
        raise TypeError(f"Unsupported unary operator: {op_type}")
    elif isinstance(node, ast.Compare):
        left = safe_eval(node.left, context)
        for op, comparator in zip(node.ops, node.comparators, strict=True):
            right = safe_eval(comparator, context)
            op_type = type(op)
            if op_type in COMP_OPERATORS:
                if not COMP_OPERATORS[op_type](left, right):
                    return False
                left = right
            else:
                raise TypeError(f"Unsupported comparison operator: {op_type}")
        return True
    elif isinstance(node, ast.BoolOp):
        values = [safe_eval(val, context) for val in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        elif isinstance(node.op, ast.Or):
            return any(values)
        raise TypeError(f"Unsupported boolean operator: {type(node.op)}")
    elif isinstance(node, ast.List):
        return [safe_eval(el, context) for el in node.elts]
    elif isinstance(node, ast.Tuple):
        return tuple(safe_eval(el, context) for el in node.elts)
    else:
        raise TypeError(f"Unsupported AST node type: {type(node)}")


def eval_expr(expr_str, context):
    """Safely parse and evaluate a mathematical or logical expression."""
    parsed = ast.parse(expr_str.strip(), mode="eval")
    return safe_eval(parsed, context)


def dict_to_namespace(d):
    """Recursively convert nested dictionaries into SimpleNamespace objects for dot access."""
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})
    elif isinstance(d, list):
        return [dict_to_namespace(x) for x in d]
    return d


def flatten_dict(d, parent_key="", sep="."):
    """Flatten a nested dictionary into dot-separated paths."""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def build_eval_context(global_state):
    """Build the namespace and variable environment for expression evaluation."""
    context = {}
    for k, v in global_state.items():
        context[k] = dict_to_namespace(v)
    # Also flatten and add leaf variables to context directly
    flat = flatten_dict(global_state)
    for k, v in flat.items():
        # Store full dotted paths (for exact lookup in expressions)
        context[k] = v
        # Also store base leaf names (e.g. "ram_gb_total" for convenience)
        leaf_name = k.split(".")[-1]
        context[leaf_name] = v
    return context


def evaluate_value(val, context):
    """Recursively evaluate template expressions inside lists, dicts, or strings."""
    if isinstance(val, str):
        stripped = val.strip()
        if stripped.startswith("${") and stripped.endswith("}"):
            expr = stripped[2:-1]
            try:
                return eval_expr(expr, context)
            except Exception as e:
                raise ValueError(f"Failed to evaluate expression '{expr}': {e}") from e
        else:
            # String interpolation: replace all occurrences of ${...}
            def repl(m):
                expr = m.group(1)
                return str(eval_expr(expr, context))

            return re.sub(r"\$\{(.+?)\}", repl, val)
    elif isinstance(val, dict):
        evaluated = {}
        for k, v in val.items():
            evaluated_val = evaluate_value(v, context)
            evaluated[k] = evaluated_val
            # Dynamically update context with the new sibling's evaluated structure
            context[k] = dict_to_namespace(evaluated_val)
            if isinstance(evaluated_val, dict):
                for flat_k, flat_v in flatten_dict(evaluated_val).items():
                    context[flat_k] = flat_v
                    context[flat_k.split(".")[-1]] = flat_v
            else:
                context[k] = evaluated_val
        return evaluated
    elif isinstance(val, list):
        return [evaluate_value(item, context) for item in val]
    return val


def resolve_ref(ref_str, current_file_path, workspace_root):
    """Locate a referenced file relative to current file or workspace root."""
    p1 = (current_file_path.parent / ref_str).resolve()
    if p1.exists():
        return p1
    p2 = (workspace_root / ref_str).resolve()
    if p2.exists():
        return p2
    return None


def explain_failure(expr_str, context):
    """Examine context to print variable values involved in a failed check."""
    # Find all words (variable paths) in the expression
    vars_found = re.findall(r"[a-zA-Z_][a-zA-Z0-9_\.]*", expr_str)
    explanations = []
    for var in set(vars_found):
        # Ignore Python keywords or constants
        if var in ("True", "False", "None"):
            continue
        try:
            val = eval_expr(var, context)
            explanations.append(f"{var} = {val}")
        except Exception:
            pass
    return f"Expression '{expr_str}' failed. [{', '.join(explanations)}]"


def main() -> None:
    workspace_root = Path.cwd().resolve()
    directories = ["docs", ".agents"]
    base_paths = [Path(d).resolve() for d in directories if Path(d).exists()]

    files_metadata: dict[Path, dict] = {}
    global_errors: list[str] = []

    # 1. Scan and parse frontmatter of all md files
    for base_path in base_paths:
        for md_file in base_path.rglob("*.md"):
            try:
                content = md_file.read_text(encoding="utf-8").strip()
                if not content.startswith("---"):
                    continue
                parts = content.split("---", 2)
                if len(parts) < 3:
                    global_errors.append(
                        f"❌ {md_file.relative_to(workspace_root)}: Malformed or unclosed YAML divider boundaries."
                    )
                    continue

                try:
                    frontmatter = yaml.safe_load(parts[1])
                except yaml.YAMLError as ye:
                    global_errors.append(f"❌ {md_file.relative_to(workspace_root)}: Invalid YAML syntax: {ye}")
                    continue

                if not isinstance(frontmatter, dict) or "type" not in frontmatter:
                    global_errors.append(
                        f"❌ {md_file.relative_to(workspace_root)}: Missing the mandatory OKF 'type' metadata key."
                    )
                    continue

                files_metadata[md_file] = {
                    "frontmatter": frontmatter,
                    "body": parts[2],
                }
            except Exception as e:
                global_errors.append(
                    f"❌ {md_file.relative_to(workspace_root)}: System exception during file load: {e}"
                )

    if global_errors:
        for err in global_errors:
            print(err)
        sys.exit(1)

    # 2. Topological Dependency Sort
    visited: dict[Path, str] = {}
    eval_order: list[Path] = []

    def visit(file_path: Path) -> None:
        if visited.get(file_path) == "visiting":
            raise ValueError(f"Cyclic dependency detected involving {file_path.relative_to(workspace_root)}") from None
        if file_path not in visited:
            visited[file_path] = "visiting"
            frontmatter_data = files_metadata[file_path]["frontmatter"]
            if isinstance(frontmatter_data, dict):
                deps = frontmatter_data.get("dependencies") or []
                for dep in deps:
                    if isinstance(dep, dict):
                        dep_ref = dep.get("ref")
                        if dep_ref:
                            dep_path = resolve_ref(dep_ref, file_path, workspace_root)
                            if dep_path in files_metadata:
                                visit(dep_path)
                            else:
                                rel_file = file_path.relative_to(workspace_root)
                                global_errors.append(f"❌ {rel_file}: Broken dependency reference to '{dep_ref}'.")
            visited[file_path] = "visited"
            eval_order.append(file_path)

    try:
        for file_path in files_metadata:
            if file_path not in visited:
                visit(file_path)
    except ValueError as ve:
        print(f"💥 Cycle Error: {ve}")
        sys.exit(1)

    if global_errors:
        for err in global_errors:
            print(err)
        sys.exit(1)

    # 3. Evaluate Exports, Constraints, and Buffers sequentially
    global_state: dict = {}

    for file_path in eval_order:
        rel_path = file_path.relative_to(workspace_root)
        meta = files_metadata[file_path]
        frontmatter = meta["frontmatter"]
        if not isinstance(frontmatter, dict):
            continue
        exports = frontmatter.get("exports") or {}
        if not isinstance(exports, dict):
            global_errors.append(f"❌ {rel_path}: 'exports' block must be a dictionary.")
            continue

        # Build context from current global state
        context = build_eval_context(global_state)

        # A. Evaluate exports for this file
        try:
            evaluated_exports = evaluate_value(exports, context)
            if isinstance(evaluated_exports, dict):
                # Merge evaluated exports into global state
                for k, v in evaluated_exports.items():
                    global_state[k] = v
        except Exception as e:
            global_errors.append(f"❌ {rel_path}: Failed to evaluate exports: {e}")
            continue

        # Re-build context with newly added exports
        context = build_eval_context(global_state)

        # B. Validate dependency constraints
        deps_list = frontmatter.get("dependencies") or []
        for dep in deps_list:
            if isinstance(dep, dict):
                constraint_checks = dep.get("constraint_check") or []
                for check in constraint_checks:
                    if isinstance(check, str):
                        try:
                            result = eval_expr(check, context)
                            if not result:
                                global_errors.append(
                                    f"❌ {rel_path}: Constraint check failure: {explain_failure(check, context)}"
                                )
                        except Exception as e:
                            global_errors.append(f"❌ {rel_path}: Constraint check evaluation error: {check} ({e})")

        # C. Validate local buffer constraints
        buffers = frontmatter.get("buffer_check") or []
        for check in buffers:
            if isinstance(check, str):
                try:
                    result = eval_expr(check, context)
                    if not result:
                        global_errors.append(f"❌ {rel_path}: Buffer check failure: {explain_failure(check, context)}")
                except Exception as e:
                    global_errors.append(f"❌ {rel_path}: Buffer check evaluation error: {check} ({e})")

        # D. Validate internal Markdown link integrity
        body = meta["body"]
        if isinstance(body, str):
            markdown_links = re.findall(r"\]\(([^:\s#)]+\.md)\)", body)
            for link in markdown_links:
                linked_file = resolve_ref(link, file_path, workspace_root)
                if not linked_file or not linked_file.exists():
                    global_errors.append(
                        f"❌ {rel_path}: Broken Knowledge Graph Link: Target path '{link}' does not exist."
                    )

    if global_errors:
        print(f"\n💥 Result: Found {len(global_errors)} validation errors. OKF Upgrade Rejected.")
        for err in global_errors:
            print(f"   • {err}")
        sys.exit(1)

    print(
        "✅ OKF Conformance Check: All documentation paths, dynamic math formulas, and constraint loops are pristine."
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
